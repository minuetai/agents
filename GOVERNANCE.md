# Governance

**Current maintainers**  
- @phelanev (lead author)

## Decision process
1. Minor, backward-compatible changes  
   *Maintainer(s) merge after ≥1 approval review and all CI checks pass.*

2. Breaking changes (new major/minor schema file)  
   *Open a proposal issue, gather feedback ≥14 days, then merge if no blocking objections.*

3. Maintainer addition / removal  
   *Must be approved by all existing maintainers.*

_All interactions should remain respectful; see GitHub’s terms of service for unacceptable behaviour._

## Versioning
- Schema files are named `agent_profile_v<MAJOR>.<MINOR>.json`.
- Once a version is released (tagged), the file is **immutable**.
- **v1.0** is the current enterprise standard. Future versions follow semantic versioning principles.
