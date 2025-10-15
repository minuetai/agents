# Changelog

All notable changes to the Minuet Agent Schema will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-15

### Added
- Complete enterprise-ready agent profile schema
- Support for complex pricing models (hybrid, outcome-based, usage-based)
- Workplace task specifications and interaction patterns
- Publisher verification and attestation system
- Comprehensive evaluation tracking
- Safety grade classification
- Model lineage documentation
- Professional schema versioning with $id and version fields

### Changed
- **BREAKING**: Renamed from `agent_profile_v1.0.json` to `schema.json`
- **BREAKING**: Updated schema title to "Minuet Agent Schema"
- **BREAKING**: Repository renamed from "agent-profile-schema" to "agents"
- Updated description to emphasize interoperability focus

### Technical
- Added JSON Schema $id field for proper referencing
- Implemented SemVer versioning strategy
- Updated crawler to prioritize `schema.json` with legacy compatibility
- Enhanced CI validation workflows
- Professional registry and discovery system

### Documentation
- Comprehensive README with enterprise positioning
- Registry viewer with filtering and export capabilities
- Example profiles for individual, corporate, enterprise, legal, multimodal, and research use cases

---

## Versioning Strategy

- **Patch** (x.y.Z): Clarifications, documentation, no schema changes
- **Minor** (x.Y.z): Additive fields, backward compatible
- **Major** (X.y.z): Breaking changes, migration guide required

## Schema URLs

- **Latest**: `https://minuetai.github.io/agents/schema.json`
- **Pinned**: `https://raw.githubusercontent.com/minuetai/agents/v1.0.0/schema.json`