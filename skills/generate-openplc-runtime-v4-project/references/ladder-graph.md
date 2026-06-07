# Ladder Diagram Hybrid Format

## File Wrapper

Observed `.ld` files combine IEC-style declarations with an OpenPLC JSON graph:

```text
PROGRAM main
  VAR_OUTPUT
    Y000 : BOOL;
  END_VAR
  VAR
    X000 : BOOL;
    X001 : BOOL;
  END_VAR

{
  "name": "main",
  "rungs": []
}
END_PROGRAM
```

Keep the filename, `PROGRAM` identifier, and JSON `name` equal.

## Rung Shape

Observed rung keys:

```json
{
  "id": "rung_main_<uuid>",
  "comment": "",
  "defaultBounds": [300, 100],
  "reactFlowViewport": [445, 174],
  "nodes": [],
  "edges": [],
  "selectedNodes": []
}
```

`nodes` store both IEC-relevant symbols and editor layout metadata. `edges` form the executable ladder path.

## Observed Node Families

### Rails

- Node `type`: `powerRail`
- Left ID prefix: `left-rail-rung_`
- Left variant: `data.variant = "left"`
- Left handle: `left-rail`, `type = "source"`
- Right ID prefix: `right-rail-rung_`
- Right variant: `data.variant = "right"`
- Right handle: `right-rail`, `type = "target"`

Each rung must connect from one left rail to one right rail.

### Contacts

- Node `type`: `contact`
- ID prefix: `CONTACT_`
- Handles: target `input`, source `output`
- Observed variants: `default`, `negated`
- Variable snapshot: `data.variable.name`, `.type.definition`, `.type.value`, `.class`, `.location`, `.documentation`, `.debug`

Semantics:

- `default`: normally open contact, true when its Boolean variable is true.
- `negated`: normally closed contact, true when its Boolean variable is false.

### Coils

- Node `type`: `coil`
- ID prefix: `COIL_`
- Handles: target `input`, source `output`
- Observed variant: `default`
- Variable snapshot uses the same core fields as contacts.

Semantics:

- `default`: write the rung Boolean result to the referenced Boolean variable.

### Parallel Branches

- Node `type`: `parallel`
- Open ID prefix: `PARALLEL_OPEN_`
- Close ID prefix: `PARALLEL_CLOSE_`
- Open node: `data.type = "open"` and `data.parallelCloseReference = <close-id>`
- Close node: `data.type = "close"` and `data.parallelOpenReference = <open-id>`

Observed two-branch handles:

| Node | Input handles | Output handles |
| --- | --- | --- |
| open | `input`, `input-top` | `output-right`, `output-down` |
| close | `input`, `input-down` | `output-right`, `output-top` |

The analyzed sample uses `open.output-right` for the upper branch, `open.output-down` for the lower branch, `close.input` for the upper merge, and `close.input-down` for the lower merge.

## Edge Shape

Observed shape:

```json
{
  "id": "e_<source>_<target>__<sourceHandle>_<targetHandle>",
  "source": "<node-id>",
  "sourceHandle": "<source-handle-id>",
  "target": "<node-id>",
  "targetHandle": "<target-handle-id>"
}
```

Require source handles with `type = "source"` and target handles with `type = "target"`.

## Sample Logic

The supplied rung resolves to:

```text
(X000 OR Y000) AND NOT X001 -> Y000
```

This is a seal-in circuit:

- `X000` starts the output.
- The `Y000` contact maintains the circuit after the start input drops.
- Negated `X001` opens the path when the stop input becomes true.
- Coil `Y000` stores the rung result.

## Boundaries

Only generate the observed node families from scratch. Preserve existing unknown nodes during edits, but require another trusted OpenPLC export before adding unobserved element shapes.
