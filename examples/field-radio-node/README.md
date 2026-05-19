# Field Radio Node Example

This example uses:

- profile: `field-radio-node`
- adapter: `manual-observer-report`
- input: `input/manual-report.json`
- expected output: `expected/normalized-observation.json`

Run:

```bat
python tools\run_pfem_example.py examples\field-radio-node
```

This proves the smallest useful PFEM path:

```text
manual report -> raw evidence candidate -> normalized observation candidate
```
