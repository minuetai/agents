# Contributing

Thank you for helping improve the Autonomous Agent Profile Schema!
We keep the workflow lightweight so fixes and enhancements land quickly but stay reliable.

## Workflow

1. Fork the repository and create a feature branch

```
git checkout -b feat/your-change
```

2. Validate locally

```
npm install -g ajv-cli ajv-formats

ajv validate -s http://json-schema.org/draft-07/schema# -d agent_profile_v0.1.json

ajv validate -s agent_profile_v0.1.json -d "examples/*.json"
```

3. Commit using Conventional Commits

```
feat(schema): add Foobar field
```

4. Open a pull request

Our GitHub Action re-runs validation; PRs must pass CI before merge.

## Adding or changing fields

- Provide a concrete use-case in the PR description
- Keep changes backward-compatible where possible
- Update at least one example profile to showcase the new field

## Versioning policy

- Files named agent_profile_v0.x.json are immutable once a release tag is cut
- Breaking changes bump minor version (v0.2, v0.3, etc)
- Major overhaul v1.0 when the community agrees the spec is stable
