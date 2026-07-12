# bundle-policy

A dependency-free Python CLI for enforcing route, asset-type, and third-party bundle budgets in CI.

## Quick start

```bash
python bundle_policy.py manifest.json policy.json --format markdown
```

`manifest.json` contains `{"assets":[{"name":"app.js","bytes":12000,"route":"/"}]}`. Set policy budgets using scoped keys such as `total`, `route:/checkout`, `type:script`, and `third-party:cdn.example`.

The command returns exit code 1 for budget violations and emits JSON by default for CI integrations.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
