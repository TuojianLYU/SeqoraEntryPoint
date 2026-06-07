# OpenPLC Runtime v4 Export Format

## Observed Tree

```text
project.json
devices/
  configuration.json
  pin-mapping.json
pous/
  programs/
    <program>.ld
servers/
  opcuaServer.json        # optional
```

An exported project may also contain a `.git/` directory. Do not copy, rewrite, or remove it unless the user explicitly requests Git operations.

## `project.json`

Observed shape:

```json
{
  "meta": {
    "name": "testproj",
    "type": "plc-project"
  },
  "data": {
    "pous": [],
    "dataTypes": [],
    "configuration": {
      "resource": {
        "tasks": [
          {
            "name": "task0",
            "triggering": "Cyclic",
            "interval": "T#20ms",
            "priority": 1
          }
        ],
        "instances": [
          {
            "name": "instance0",
            "program": "main",
            "task": "task0"
          }
        ],
        "globalVariables": []
      }
    }
  }
}
```

Observed semantics:

- `meta.type` is `plc-project`.
- `tasks[*].interval` uses IEC duration notation such as `T#20ms`.
- `instances[*].program` resolves to `pous/programs/<program>.ld`.
- `instances[*].task` resolves to a task name.
- The supplied export keeps `data.pous` empty even though `pous/programs/main.ld` exists. Preserve this behavior unless another trusted export demonstrates a different editor contract.

## Device Files

Observed Runtime v4 device configuration:

```json
{
  "deviceBoard": "OpenPLC Runtime v4",
  "communicationPort": "",
  "runtimeIpAddress": "",
  "compileOnly": false
}
```

Observed `devices/pin-mapping.json` value:

```json
[]
```

Earlier Git history in the supplied ZIP contains a different `communicationConfiguration.modbusRTU` shape. Treat device configuration as export-version dependent and preserve an existing shape while editing.

## OPC UA Server

`servers/opcuaServer.json` is optional. In the supplied export:

- Top-level `name` is `opcuaServer`.
- Top-level `protocol` is `opcua`.
- `opcuaServerConfig.addressSpace.nodes[*].pouName` resolves to a POU.
- `variablePath` resolves to a declared POU variable.
- `variableType` matches the declaration type.
- `nodeId` values are unique.

Preserve security settings from an existing project. Do not silently enable insecure profiles in a new production-targeted project.
