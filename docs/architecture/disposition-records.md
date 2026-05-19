# Disposition Records

PFEM disposition records say what happens to closed workflow artifacts.

The boundary is:

```text
closeout record     = final operational closure of a workflow
disposition record  = retain/archive/export/remove/hold decision for closed artifacts
retention policy    = standing rule basis for disposition decisions
```

## Why disposition records exist

A closeout record says:

```text
The workflow is closed with this final outcome.
```

A disposition record says:

```text
Now that it is closed, these artifacts are retained, archived, exported, removed, or held.
```

That keeps operational closure separate from records-management handling.

## Typical disposition states

A disposition record can say:

- retained
- archived
- exported
- removed
- held
- pending
- superseded
