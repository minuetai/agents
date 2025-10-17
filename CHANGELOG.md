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

## [0.2.0] - 2025-08-15

### Added
- Enterprise-ready features and capabilities
- Enhanced pricing model support
- Improved evaluation tracking
- Extended workplace task specifications
- Safety and compliance enhancements

### Changed
- Updated schema description to "enterprise-ready edition"
- Refined field definitions for production use
- Enhanced validation rules

### Technical
- Maintained backward compatibility with v0.1
- Improved JSON Schema structure
- Added enterprise example profiles

## [0.1.0] - 2025-06-01

### Added
- Initial release of Autonomous Agent Schema
- Core agent identification system with agent_id
- Basic model lineage tracking (base_model, finetune_date, checkpoint_hash)
- Skills framework with categories and proficiency levels
- Evaluation system for agent capabilities
- Publisher information and verification
- Simple pricing models
- Basic metadata structure

### Features
- Machine-readable agent résumé format
- JSON Schema Draft-07 compliance
- Required core fields: agent_id, name, model_lineage, skills, evals
- Foundation for agent discovery and interoperability

---

## Versioning Strategy

- **Patch** (x.y.Z): Clarifications, documentation, no schema changes
- **Minor** (x.Y.z): Additive fields, backward compatible
- **Major** (X.y.z): Breaking changes, migration guide required

## Schema URLs

- **Latest**: `https://minuetai.github.io/agents/schema.json`
- **Pinned**: `https://raw.githubusercontent.com/minuetai/agents/v1.0.0/schema.json`