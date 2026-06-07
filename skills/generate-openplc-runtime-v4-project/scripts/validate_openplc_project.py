#!/usr/bin/env python3
"""Validate observed OpenPLC Runtime v4 export syntax and cross-file semantics."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PROGRAM_RE = re.compile(r"(?m)^\s*PROGRAM\s+([A-Za-z_][A-Za-z0-9_]*)\s*$")
VAR_BLOCK_RE = re.compile(r"(?ms)^\s*(VAR(?:_[A-Z_]+)?)\s*$\n(.*?)^\s*END_VAR\s*$")
DECL_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:AT\s+\S+\s*)?:\s*([A-Za-z_][A-Za-z0-9_]*)\s*;\s*$",
    re.IGNORECASE,
)
SUPPORTED_NODE_TYPES = {"powerRail", "contact", "coil", "parallel"}


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def load_json(path: Path, result: Result) -> Any | None:
    if not path.is_file():
        result.error(f"missing required file: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        result.error(f"invalid JSON in {path}: {exc}")
        return None


def parse_ld(path: Path, result: Result) -> tuple[str, dict[str, str], dict[str, Any]] | None:
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        result.error(f"cannot read {path}: {exc}")
        return None

    match = PROGRAM_RE.search(raw)
    if not match:
        result.error(f"{path}: missing PROGRAM declaration")
        return None
    name = match.group(1)
    end_marker = "\nEND_PROGRAM"
    json_start = raw.find("{", match.end())
    json_end = raw.rfind(end_marker)
    if json_start < 0 or json_end < json_start:
        result.error(f"{path}: expected JSON object followed by END_PROGRAM")
        return None
    if raw[json_end + 1 :].strip() != "END_PROGRAM":
        result.error(f"{path}: trailing content after END_PROGRAM")

    declarations: dict[str, str] = {}
    declaration_region = raw[match.end() : json_start]
    for block in VAR_BLOCK_RE.finditer(declaration_region):
        for line in block.group(2).splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("(*"):
                continue
            declaration = DECL_RE.match(line)
            if not declaration:
                result.warn(f"{path}: declaration not covered by conservative parser: {stripped}")
                continue
            variable, variable_type = declaration.groups()
            if variable in declarations:
                result.error(f"{path}: duplicate declaration for {variable}")
            declarations[variable] = variable_type.upper()

    try:
        graph = json.loads(raw[json_start:json_end])
    except json.JSONDecodeError as exc:
        result.error(f"{path}: invalid ladder JSON: {exc}")
        return None
    if not isinstance(graph, dict):
        result.error(f"{path}: ladder JSON must be an object")
        return None
    return name, declarations, graph


def handle_index(node: dict[str, Any]) -> dict[str, str]:
    handles = node.get("data", {}).get("handles", [])
    if not isinstance(handles, list):
        return {}
    return {
        handle.get("id"): handle.get("type")
        for handle in handles
        if isinstance(handle, dict) and isinstance(handle.get("id"), str)
    }


def validate_rung(path: Path, rung: dict[str, Any], declarations: dict[str, str], result: Result) -> None:
    rung_id = rung.get("id", "<missing-rung-id>")
    nodes = rung.get("nodes")
    edges = rung.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        result.error(f"{path}:{rung_id}: nodes and edges must be arrays")
        return

    node_by_id: dict[str, dict[str, Any]] = {}
    left_rails: list[str] = []
    right_rails: list[str] = []
    parallel_nodes: list[dict[str, Any]] = []
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            result.error(f"{path}:{rung_id}: each node needs a string id")
            continue
        node_id = node["id"]
        if node_id in node_by_id:
            result.error(f"{path}:{rung_id}: duplicate node id {node_id}")
        node_by_id[node_id] = node
        node_type = node.get("type")
        if node_type not in SUPPORTED_NODE_TYPES:
            result.warn(f"{path}:{rung_id}: unverified node type {node_type!r} in {node_id}")
        data = node.get("data", {})
        if not isinstance(data, dict):
            result.error(f"{path}:{rung_id}: node {node_id} data must be an object")
            continue
        if node_type == "powerRail":
            if data.get("variant") == "left":
                left_rails.append(node_id)
            elif data.get("variant") == "right":
                right_rails.append(node_id)
        if node_type == "parallel":
            parallel_nodes.append(node)
        variable = data.get("variable")
        if isinstance(variable, dict) and variable.get("name"):
            variable_name = variable["name"]
            if variable_name not in declarations:
                result.error(f"{path}:{rung_id}: node {node_id} references undeclared variable {variable_name}")
            snapshot_type = variable.get("type", {}).get("value") if isinstance(variable.get("type"), dict) else None
            if snapshot_type and declarations.get(variable_name, "").lower() != str(snapshot_type).lower():
                result.error(
                    f"{path}:{rung_id}: node {node_id} snapshot type {snapshot_type} "
                    f"does not match declaration {declarations.get(variable_name)}"
                )

    if len(left_rails) != 1 or len(right_rails) != 1:
        result.error(f"{path}:{rung_id}: expected exactly one left rail and one right rail")

    edge_ids: set[str] = set()
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if not isinstance(edge, dict):
            result.error(f"{path}:{rung_id}: every edge must be an object")
            continue
        edge_id = edge.get("id")
        if not isinstance(edge_id, str):
            result.error(f"{path}:{rung_id}: every edge needs a string id")
        elif edge_id in edge_ids:
            result.error(f"{path}:{rung_id}: duplicate edge id {edge_id}")
        else:
            edge_ids.add(edge_id)
        source = edge.get("source")
        target = edge.get("target")
        if source not in node_by_id or target not in node_by_id:
            result.error(f"{path}:{rung_id}: edge {edge_id} references missing endpoint")
            continue
        source_handle = edge.get("sourceHandle")
        target_handle = edge.get("targetHandle")
        if handle_index(node_by_id[source]).get(source_handle) != "source":
            result.error(f"{path}:{rung_id}: edge {edge_id} has invalid source handle {source_handle!r}")
        if handle_index(node_by_id[target]).get(target_handle) != "target":
            result.error(f"{path}:{rung_id}: edge {edge_id} has invalid target handle {target_handle!r}")
        adjacency[source].append(target)

    if len(left_rails) == 1 and len(right_rails) == 1:
        queue = deque(left_rails)
        visited = set(left_rails)
        while queue:
            current = queue.popleft()
            for target in adjacency[current]:
                if target not in visited:
                    visited.add(target)
                    queue.append(target)
        if right_rails[0] not in visited:
            result.error(f"{path}:{rung_id}: no path from left rail to right rail")

    for node in parallel_nodes:
        data = node.get("data", {})
        parallel_type = data.get("type")
        if parallel_type == "open":
            reference_key = "parallelCloseReference"
            inverse_key = "parallelOpenReference"
            expected_type = "close"
        elif parallel_type == "close":
            reference_key = "parallelOpenReference"
            inverse_key = "parallelCloseReference"
            expected_type = "open"
        else:
            result.error(f"{path}:{rung_id}: parallel node {node['id']} needs data.type open or close")
            continue
        reference = data.get(reference_key)
        paired = node_by_id.get(reference)
        if not paired or paired.get("type") != "parallel":
            result.error(f"{path}:{rung_id}: parallel node {node['id']} references missing pair {reference!r}")
            continue
        paired_data = paired.get("data", {})
        if paired_data.get("type") != expected_type or paired_data.get(inverse_key) != node["id"]:
            result.error(f"{path}:{rung_id}: parallel node {node['id']} pair is not mutually linked")


def validate_ld(path: Path, result: Result) -> tuple[str, dict[str, str]] | None:
    parsed = parse_ld(path, result)
    if not parsed:
        return None
    name, declarations, graph = parsed
    if path.stem != name:
        result.error(f"{path}: filename {path.stem!r} does not match PROGRAM name {name!r}")
    if graph.get("name") != name:
        result.error(f"{path}: graph name {graph.get('name')!r} does not match PROGRAM name {name!r}")
    rungs = graph.get("rungs")
    if not isinstance(rungs, list):
        result.error(f"{path}: graph rungs must be an array")
        return name, declarations
    for rung in rungs:
        if not isinstance(rung, dict):
            result.error(f"{path}: every rung must be an object")
            continue
        validate_rung(path, rung, declarations, result)
    return name, declarations


def validate_project(root: Path, result: Result) -> None:
    project = load_json(root / "project.json", result)
    load_json(root / "devices" / "configuration.json", result)
    load_json(root / "devices" / "pin-mapping.json", result)

    pous: dict[str, dict[str, str]] = {}
    programs_dir = root / "pous" / "programs"
    if not programs_dir.is_dir():
        result.error(f"missing required directory: {programs_dir}")
    else:
        for path in sorted(programs_dir.glob("*.ld")):
            parsed = validate_ld(path, result)
            if parsed:
                name, declarations = parsed
                pous[name] = declarations

    if isinstance(project, dict):
        if project.get("meta", {}).get("type") != "plc-project":
            result.error("project.json: meta.type must be 'plc-project'")
        resource = project.get("data", {}).get("configuration", {}).get("resource", {})
        tasks = resource.get("tasks", [])
        instances = resource.get("instances", [])
        if not isinstance(tasks, list) or not isinstance(instances, list):
            result.error("project.json: resource tasks and instances must be arrays")
        else:
            task_names = {task.get("name") for task in tasks if isinstance(task, dict)}
            if len(task_names) != len(tasks):
                result.error("project.json: task names must be present and unique")
            for instance in instances:
                if not isinstance(instance, dict):
                    result.error("project.json: every instance must be an object")
                    continue
                if instance.get("program") not in pous:
                    result.error(f"project.json: instance {instance.get('name')!r} references missing program {instance.get('program')!r}")
                if instance.get("task") not in task_names:
                    result.error(f"project.json: instance {instance.get('name')!r} references missing task {instance.get('task')!r}")

    opcua_path = root / "servers" / "opcuaServer.json"
    if opcua_path.exists():
        opcua = load_json(opcua_path, result)
        if isinstance(opcua, dict):
            nodes = opcua.get("opcuaServerConfig", {}).get("addressSpace", {}).get("nodes", [])
            if not isinstance(nodes, list):
                result.error(f"{opcua_path}: addressSpace.nodes must be an array")
            else:
                seen_node_ids: set[str] = set()
                for node in nodes:
                    if not isinstance(node, dict):
                        result.error(f"{opcua_path}: every OPC UA node must be an object")
                        continue
                    node_id = node.get("nodeId")
                    if not isinstance(node_id, str) or not node_id:
                        result.error(f"{opcua_path}: every OPC UA node needs nodeId")
                    elif node_id in seen_node_ids:
                        result.error(f"{opcua_path}: duplicate OPC UA nodeId {node_id}")
                    else:
                        seen_node_ids.add(node_id)
                    pou_name = node.get("pouName")
                    variable_name = node.get("variablePath")
                    if pou_name not in pous:
                        result.error(f"{opcua_path}: node {node_id!r} references missing POU {pou_name!r}")
                        continue
                    declaration_type = pous[pou_name].get(variable_name)
                    if declaration_type is None:
                        result.error(f"{opcua_path}: node {node_id!r} references undeclared variable {variable_name!r}")
                    elif node.get("variableType") and node["variableType"].upper() != declaration_type:
                        result.error(
                            f"{opcua_path}: node {node_id!r} type {node['variableType']!r} "
                            f"does not match declaration {declaration_type!r}"
                        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_directory", type=Path)
    args = parser.parse_args()
    root = args.project_directory.resolve()
    result = Result()
    if not root.is_dir():
        result.error(f"project directory does not exist: {root}")
    else:
        validate_project(root, result)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    if result.errors:
        print(f"FAILED: {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
        return 1
    print(f"OK: OpenPLC project validated with {len(result.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
