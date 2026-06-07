---
name: generate-openplc-runtime-v4-project
description: Generate, modify, inspect, and validate conservative OpenPLC Runtime v4 project exports, especially project.json, devices configuration, pin mappings, OPC UA server configuration, and ladder-diagram .ld files that combine IEC 61131-3 declarations with an OpenPLC JSON graph. Use when Codex must create OpenPLC code, repair an exported OpenPLC project, explain ladder logic semantics, or verify that generated OpenPLC files preserve observed syntax and cross-file references.
---

# Generate OpenPLC Runtime v4 Project

## Goal

Generate OpenPLC Runtime v4 projects conservatively from observed export syntax. Preserve schema details that are already present, validate every generated project, and do not invent JSON node shapes for ladder elements that are not covered by a trusted export sample.

## Workflow

1. Inspect the target project and read [references/export-format.md](references/export-format.md).
2. For ladder-diagram work, read [references/ladder-graph.md](references/ladder-graph.md).
3. Create a new empty project with:

   ```powershell
   python scripts/new_openplc_project.py <output-directory> --project-name <name> --pou-name main
   ```

4. Modify the generated files or an existing export. Keep POU declarations, ladder graph variable snapshots, task instances, and OPC UA nodes aligned.
5. Validate before delivery:

   ```powershell
   python scripts/validate_openplc_project.py <project-directory>
   ```

6. Report any remaining warnings as unsupported or sample-dependent behavior.

## Generation Rules

- Treat `project.json` and `devices/*.json` as strict JSON files.
- Treat each `pous/programs/*.ld` file as a hybrid format:
  - IEC-style `PROGRAM`, variable blocks, and `END_PROGRAM`.
  - One JSON object between declarations and `END_PROGRAM`.
- Preserve existing unknown keys when editing an export. The OpenPLC editor may store UI geometry and connector metadata that are not required for IEC semantics but are required for round-trip editing.
- Generate only the observed ladder node families from scratch: `powerRail`, `contact`, `coil`, and paired `parallel` nodes.
- For timers, counters, function blocks, set/reset coils, edge contacts, additional POU types, data types beyond the observed base Boolean case, or alternate device schemas, require another trusted OpenPLC export sample before generating new graph JSON.
- Prefer extending a user-supplied export over reconstructing a non-empty ladder graph by hand.
- Use fresh stable IDs when adding graph objects. Keep every edge endpoint and every parallel open/close reference synchronized.

## Semantic Rules

- Resolve `project.json.data.configuration.resource.instances[*].program` to `pous/programs/<program>.ld`.
- Resolve every instance task to a task in the same resource.
- Match the `.ld` filename, `PROGRAM` identifier, and JSON body `name`.
- Declare every non-empty ladder variable snapshot in the POU header.
- Treat contact and coil variable `class` metadata as editor snapshots, not as the source of truth. The supplied export uses different `class` values for repeated snapshots of `Y000`; declarations remain authoritative.
- Connect each rung from one left rail to one right rail.
- Pair `parallel` open and close nodes with mutual references.
- Resolve OPC UA `pouName` and `variablePath` to declared POU variables.

## Validation Scope

The validator enforces observed structural invariants and flags unknown node types as warnings. It is a guardrail for accurate generation from the supplied sample, not a replacement for importing the project into the exact OpenPLC editor/runtime version used by the user.

## References

- Read [references/export-format.md](references/export-format.md) for the project tree and JSON roles.
- Read [references/ladder-graph.md](references/ladder-graph.md) for `.ld` syntax, observed node shapes, and rung semantics.
- Read [references/observed-testproj.md](references/observed-testproj.md) for the analyzed sample and confidence boundaries.
