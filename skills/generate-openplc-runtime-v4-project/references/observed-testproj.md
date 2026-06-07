# Observed `TestProj.zip`

## Facts

The supplied OpenPLC export contains:

| File | Role |
| --- | --- |
| `project.json` | PLC project metadata, one cyclic task, and one program instance |
| `devices/configuration.json` | Runtime v4 board selection |
| `devices/pin-mapping.json` | Empty pin mapping array |
| `pous/programs/main.ld` | One program with Boolean declarations and one ladder rung |
| `servers/opcuaServer.json` | OPC UA server configuration with three exposed Boolean nodes |

The ZIP also contains a `.git/` directory. Its initial commit stores an empty `main.ld`; the ZIP working tree stores the edited self-holding rung and adds the OPC UA server file.

## Observed Declarations

```text
PROGRAM main
  VAR_OUTPUT
    Y000 : BOOL;
  END_VAR
  VAR
    X000 : BOOL;
    X001 : BOOL;
  END_VAR
```

## Observed Rung Inventory

| Node type | Count | Purpose |
| --- | ---: | --- |
| `powerRail` | 2 | left and right rails |
| `parallel` | 2 | open and close pair for OR branch |
| `contact` | 3 | `X000`, `Y000`, and negated `X001` |
| `coil` | 1 | output `Y000` |
| edges | 8 | complete path between rails |

## Confidence Boundary

This skill is based on one Runtime v4 export sample, not an official exhaustive schema. It confidently validates the observed wrapper, metadata, node families, graph references, and OPC UA variable links. Extend it with additional exports before generating timers, counters, function blocks, non-Boolean graph snapshots, additional POU kinds, or alternate editor versions.
