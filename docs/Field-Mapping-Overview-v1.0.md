# Field-Mapping Overview (Minuet Agent Schema ↔ Ecosystem Equivalents)
version: 2025-10-11  
schema_version: 1.0.0  
last_full_verification: TBD  
next_full_review: 2026-01-15  
scope: Conceptual equivalence only. Mappings shown **only** where backed by official sources (docs / SDK / examples).  

## Legend  
Type = Direct | Computed | Composite | N/A | Unknown  
Confidence = High | Med | Low | Unknown  

> **Note on Confidence:**  
> Some ecosystems currently provide only partial or preview documentation of their agent metadata.  
> Rather than omit these mappings entirely, Minuet assigns a **Confidence** level to indicate how strongly each equivalence is supported by public evidence as of the last verification.  
> This approach maintains transparency while ensuring readers can distinguish between confirmed, conceptual, and evolving mappings across ecosystems.

---

## Core Fields (Verified Mappings)

| **Minuet Field** | **LangChain [ L1 ]** | **OpenRouter [ O1 ]** | **AWS Bedrock AgentCore [ A1 ]** | **Type** | **Confidence** | **Notes / Sources** |
|------------------|-----------------------|-----------------------|----------------------------------|-----------|----------------|----------------------|
| `name` | `name` (agent class) | — | “Agent Name” concept | Direct | Med | [L1] LangChain agent API docs (2025-10), [A1] AWS AgentCore developer guide. |
| `description` | `description` attribute | — | “Summary” field concept | Direct | Low | Confirmed in LangChain core docs; AWS reference in preview docs only. |
| `tools[] / capabilities` | `tools` array (agent tools) | — | “Functions” / Gateway integration concept | Composite | Med | [L1] LangChain agents API; [A1] AWS AgentCore Gateway docs. |
| `runtime.environment` | — | — | “Runtime” section concept in AgentCore | Direct | Low | [A1] Bedrock AgentCore overview page. |
| `endpoint.url` | — | — | “InvokeUri” field in Gateway definition | Direct | Med | [A1] Bedrock AgentCore Gateway spec. |

---

## Sources  
- **[ L1 ]** LangChain Agents API documentation (https://docs.langchain.com/oss/python/langchain/agents)  
- **[ O1 ]** OpenRouter public API docs (https://openrouter.ai/docs) — no explicit agent schema as of 2025-10.  
- **[ A1 ]** AWS Bedrock AgentCore developer guide (https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)  

---

## Pending Verification (Fields Without Public Mappings)

| **Minuet Field** | **Reason Pending** | **Next Action** |
|------------------|--------------------|-----------------|
| `deployment_type` | No published field name in LangChain / OpenRouter / AWS docs. | Monitor AWS AgentCore updates and LangChain runtime metadata. |
| `token_cost_per_1k` | Conceptual in OpenRouter pricing API, but no explicit key. | Confirm once OpenRouter releases pricing schema. |
| `uptime.last_30_days` | Operational metric not present in any public schemas. | Propose as optional field for future version. |

---

## Appendix – Providers Pending Verification
| **Provider** | **Reason for Pending Status** | **Next Action** |
|---------------|-------------------------------|-----------------|
| **Google Cloud Agent Marketplace** | No public manifest or agent metadata schema available. | Monitor developer docs and SDK releases. |
| **Microsoft Copilot / Agent Store** | No accessible schema or field list published to date. | Review Microsoft Partner Center / Copilot API docs once available. |

---

## Coverage Summary
- Verified coverage exists only for LangChain (core metadata fields) and AWS Bedrock AgentCore (preview docs).  
- OpenRouter has conceptual alignment but no formal schema yet.  
- Google and Microsoft remain pending until manifest formats are public.  
- Next review trigger: any major SDK release or spec update from these ecosystems.  

---

## Open Research Note
This document is published as part of Minuet Labs’ ongoing open research into emerging standards for AI-agent interoperability.  
Its purpose is to encourage transparency and convergence across the ecosystem, not to imply exclusivity or competition.  
By maintaining a public cross-mapping of existing agent frameworks, Minuet aims to accelerate compatibility work and reduce duplication of effort industry-wide.  
Any provider or contributor is welcome to reference, extend, or improve these mappings in the spirit of shared infrastructure.

---

**Maintenance schedule:** This mapping is reviewed quarterly or whenever a major provider publishes updated agent specifications.  

**Disclaimer:**  
This mapping represents Minuet AI's’ independent research as of 2025-10-11.  
The providers listed are **not** affiliated with Minuet Labs, and no official endorsement or partnership is implied.  

---

**status:** active  
**last_review:** 2025-10-11  
**intended_consumer:** reasoning AI or technical reviewer verifying schema interoperability mapping.  
-- END --