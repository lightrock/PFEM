# PFEM Examples

Examples are tiny runnable PFEM design-pattern instances.

Start with:

```bat
python tools\run_pfem_example.py examples\field-radio-node
```

or run all tests:

```bat
run_tests.bat
```

Current examples:

- `field-radio-node` — uses the manual observer report adapter to turn a raw report into normalized observation output.
- `civil-dashboard-node` — shows a dashboard-only profile shape with no local source adapter.
- `infrastructure-site-node` — shows a site-oriented profile shape with adapter slots configured by deployment.
