#!/usr/bin/env python3
"""Create a conservative empty OpenPLC Runtime v4 project skeleton."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--pou-name", default="main")
    parser.add_argument("--task-name", default="task0")
    parser.add_argument("--instance-name", default="instance0")
    parser.add_argument("--interval", default="T#20ms")
    parser.add_argument("--with-opcua", action="store_true")
    args = parser.parse_args()

    for label, value in (
        ("POU name", args.pou_name),
        ("task name", args.task_name),
        ("instance name", args.instance_name),
    ):
        if not IDENTIFIER.fullmatch(value):
            parser.error(f"{label} must be an IEC-style identifier: {value!r}")

    output = args.output_directory.resolve()
    if output.exists() and any(output.iterdir()):
        parser.error(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    write_json(
        output / "project.json",
        {
            "meta": {"name": args.project_name, "type": "plc-project"},
            "data": {
                "pous": [],
                "dataTypes": [],
                "configuration": {
                    "resource": {
                        "tasks": [
                            {
                                "name": args.task_name,
                                "triggering": "Cyclic",
                                "interval": args.interval,
                                "priority": 1,
                            }
                        ],
                        "instances": [
                            {
                                "name": args.instance_name,
                                "program": args.pou_name,
                                "task": args.task_name,
                            }
                        ],
                        "globalVariables": [],
                    }
                },
            },
        },
    )
    write_json(
        output / "devices" / "configuration.json",
        {
            "deviceBoard": "OpenPLC Runtime v4",
            "communicationPort": "",
            "runtimeIpAddress": "",
            "compileOnly": False,
        },
    )
    write_json(output / "devices" / "pin-mapping.json", [])

    pou_path = output / "pous" / "programs" / f"{args.pou_name}.ld"
    pou_path.parent.mkdir(parents=True, exist_ok=True)
    pou_path.write_text(
        f"PROGRAM {args.pou_name}\n"
        "  VAR\n"
        "  END_VAR\n"
        "\n"
        "{\n"
        f'  "name": "{args.pou_name}",\n'
        '  "rungs": []\n'
        "}\n"
        "END_PROGRAM\n",
        encoding="utf-8",
    )

    if args.with_opcua:
        write_json(
            output / "servers" / "opcuaServer.json",
            {
                "name": "opcuaServer",
                "protocol": "opcua",
                "opcuaServerConfig": {
                    "server": {
                        "enabled": False,
                        "name": "OpenPLC OPC UA Server",
                        "applicationUri": "urn:openplc:opcua:server",
                        "productUri": "urn:openplc:runtime",
                        "bindAddress": "0.0.0.0",
                        "port": 4840,
                        "endpointPath": "/openplc/opcua",
                    },
                    "securityProfiles": [],
                    "security": {
                        "serverCertificateStrategy": "auto_self_signed",
                        "serverCertificateCustom": None,
                        "serverPrivateKeyCustom": None,
                        "trustedClientCertificates": [],
                    },
                    "users": [],
                    "cycleTimeMs": 100,
                    "addressSpace": {
                        "namespaceUri": "urn:openplc:opcua:namespace",
                        "nodes": [],
                    },
                },
            },
        )

    print(f"Created OpenPLC Runtime v4 project skeleton: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
