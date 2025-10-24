# Contributing to Mapping Docs

Thank you for helping improve the **Minuet Agent Schema** mapping documentation!
Your contributions help maintain accuracy, transparency, and interoperability across the agent ecosystem.

---

## Mapping Documentation Standards

When creating or updating field-mapping documentation, please follow these guidelines.

### Required Frontmatter

Every mapping document must begin with the following metadata block **(frontmatter or inline)**:

    ---
    schema_version: 1.0.0
    last_full_verification: YYYY-MM-DD
    author: [Your Name or GitHub Handle]
    ---

- **schema_version**: Must match the version in `schema.json`.
- **last_full_verification**: Date when links and examples were last validated.
- **author**: Your name or GitHub handle.

---

### Versioning Rules

| Change | Action | Example |
|---------|---------|----------|
| Add/remove provider column | **PATCH** | `v1.0.1` |
| Add/deprecate schema fields | **MINOR** | `v1.1.0` |
| Breaking field rename/removal | **MAJOR** | `v2.0.0` |

Always update `/docs/mappings/CHANGELOG.md` when bumping versions.

---

### Inclusion Rules

- **Core Table**: Rows with Med+ confidence and at least one official source.
- **Pending Table**: Rows with Low/Unknown confidence or missing sources.
- No citation = no Core inclusion.

---

### Evidence Hierarchy

1. Official specs or API references
2. Official SDK types or manifests
3. Maintainer statements or example repos
4. Release notes/changelogs

---

### Link Verification

All external links (LangChain, AWS, OpenRouter, etc.) must be:
- ✅ Active and resolving
- ✅ Pointing to stable, versioned documentation (no link shorteners)
- ✅ Verified within 120 days of submission

---

### CI/CD Pipeline

Every PR that touches mapping docs automatically triggers **Mappings CI**:

1. **Link Checker** – validates all URLs.
2. **Schema Version Guard** – ensures `schema_version:` matches `schema.json`.
3. **Staleness Detector** – warns if `last_full_verification` > 120 days.

> Warnings will appear in the GitHub Actions log; critical issues may block merge.

---

### Review & Merge

- PRs are reviewed for accuracy, structure, and version compliance.
- CI must complete successfully (warnings allowed).
- After merge, update `last_full_verification` to today's date.

---

### Maintenance Cadence

Minuet AI performs a quarterly full verification sweep or upon major ecosystem updates.

---

### Questions?

Open an **Issue** or **Discussion** in this repository.
Thank you for supporting transparent, ecosystem-wide interoperability!
