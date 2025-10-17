<div align="center">
  <img src="minuet-logo.png" alt="Minuet Labs" width="180">
</div>

# Agents

The open infrastructure for AI agent discovery and interoperability.

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI Status](https://img.shields.io/github/actions/workflow/status/minuetai/agents/ci.yml?branch=main)](https://github.com/minuetai/agents/actions)

**The canonical schema** for AI agent discovery and interoperability. Enables autonomous agents to publish machine-verifiable definitions with:

* identity & model lineage  
* skills and benchmark scores  
* cost, latency, and safety grade  
* publisher verification & compliance attestations  

Standardizes agent representation across marketplaces, platforms, and ecosystems — eliminating bespoke adapters and enabling seamless interoperability.

---

## Files in this repo

| Path | Contents |
|------|----------|
| `schema.json` | **Draft-07** schema definition (comment-free, validator-ready) |
| `examples/example_individual_agent.json` | Minimal agent for a solo builder (`individual`) |
| `examples/example_corporate_agent.json`  | Agent showing optional `publisher` & `attestations` blocks |
| `examples/example_enterprise_v1.0.json` | Full v1.0 enterprise agent with pricing models & workplace tasks |
| `examples/example_legal_agent.json` | Specialized legal analysis agent |
| `examples/example_multimodal_agent.json` | Vision and document processing agent |
| `examples/example_research_agent.json` | Scientific research agent with multiple evaluations |
| `LICENSE` | MIT — applies to this repository's code & docs |
| `CONTRIBUTING.md` | How to propose changes & run validation locally |

---

## Quick start
```shell
    # clone
    git clone https://github.com/minuetai/agents.git
    cd agents

    # install validator (Node.js)
    npm install -g ajv-cli ajv-formats

    # validate the schema itself
    ajv validate \
      -s http://json-schema.org/draft-07/schema# \
      -d schema.json

    # validate the individual example
    ajv validate -c ajv-formats \
      -s schema.json \
      -d examples/example_individual_agent.json
```


*No CLI?* Paste both schema and agent definition into **<https://jsonschemavalidator.io/>** and click **Validate Schema & Data**.

▶ Browse the public registry: <https://minuetai.github.io/agents/>.

---

## Schema Versioning & URLs

**Latest Version (Recommended):**
```bash
# Use latest schema
curl -L https://minuetai.github.io/agents/schema.json

# Validate against latest
ajv validate -c ajv-formats \
  -s https://minuetai.github.io/agents/schema.json \
  -d your-agent.json
```

**Pinned Version (Production):**
```bash
# Pin to specific version via git tag
curl -L https://raw.githubusercontent.com/minuetai/agents/v1.0.0/schema.json

# Validate against pinned version
ajv validate -c ajv-formats \
  -s https://raw.githubusercontent.com/minuetai/agents/v1.0.0/schema.json \
  -d your-agent.json
```

**Versioning Policy:**
- **Latest**: Always points to current version, gets updates
- **Pinned**: Immutable, safe for production CI/CD pipelines
- **SemVer**: Major.minor.patch (1.0.0, 1.1.0, 2.0.0)

---

## 🌍 Publish your agent (24 h discovery)

[![Add your agent — 1 JSON file](https://img.shields.io/badge/Add%20your%20agent-1%20JSON%20file-brightgreen)](#publish-your-agent-24-h-discovery)

**✅ No setup required — just publish in your own repository!**

1. **Create** a file named **`agent.json`** in *your own* repository.  
2. **Fill it in** – start from [`examples/example_individual_agent.json`](examples/example_individual_agent.json).  
3. **Add topics** – Tag your repo with `agent-profile`, `ai-agent`, `autonomous-agent`, or `llm-agent`
4. **Validate locally** (optional but recommended)

    ~~~bash
    # one-time install
    npm install -g ajv-cli ajv-formats

    # validate your agent against the schema
    ajv validate -c ajv-formats \
                 -s https://minuetai.github.io/agents/schema.json \
                 -d agent.json
    ~~~

5. **Commit & push** – that's it. Our nightly crawler scans GitHub for the filename, validates your agent, and adds it to the public registry.  
6. **Check back tomorrow** – your agent should appear here → <https://minuetai.github.io/agents/>

> ℹ️ **Don't fork this repo** unless you're contributing to the schema itself. The whole point is automatic discovery from your own repository!

> ℹ️ If validation fails, the agent won't be indexed. Run the `ajv` command above to see and fix errors before pushing.

---

## Field highlights

| Field | Notes |
|-------|-------|
| `model_lineage.base_model` | Any string, e.g. `"mistral/Mixtral-8x7B-Instruct"` |
| `skills[]` | Free-form tags such as `["sql-agent","xss-scanner"]` |
| `evals[]` | Benchmark objects; include `name`, numeric `score`, `date` |
| `publisher.entity_type` | `individual`, `corporation`, `nonprofit`, `public-sector` |
| `attestations[].type` | Typical: `soc2`, `iso27001`, `pci-dss`, `insurance` |

See full field docs inside the schema file.

---

## Versioning policy

* **v1.0** — enterprise standard (stable).  
* Future versions will maintain backward compatibility where possible.  
* Each version is **immutable** once tagged; pin the exact file path for CI pipelines.

---

## Contributing

1. Fork → create a feature branch → open a PR.  
2. Run `ajv validate` before submitting.  
3. Add a real-world use-case for any new field you propose.  
4. We follow [Conventional Commits](https://www.conventionalcommits.org/) for merge messages.

Thank you for helping build an open, interoperable future for autonomous agents!

## Explore More

- [Explodential.com](https://explodential.com) – Autonomous agent newsletter

---

*Product names such as "GPT-4o" are trademarks of their respective owners and appear here for illustrative purposes only.*

© 2025 Minuet Labs LLC. Cialint™ is a trademark of Minuet Labs LLC.  
See [LEGAL.md](./LEGAL.md) for full terms.
