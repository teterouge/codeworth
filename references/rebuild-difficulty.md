# Rebuild Difficulty Model

**The core insight**: LOC measures volume. Rebuild difficulty measures knowledge.

A 12,000-line ML research repo and a 12,000-line CRUD SaaS are not the same problem.
The ML repo might take 10× longer to rebuild — not because there's more code,
but because the code encodes specialized knowledge that takes years to acquire.

This reference defines how CodeWorth converts raw complexity signals into a
**Rebuild Difficulty Rating** that surfaces what the hours estimate can't say alone.

---

## The Five Difficulty Dimensions

Each dimension is scored independently, then combined into a composite rating.
Claude scores each dimension after reviewing the script output and repo structure.

---

### Dimension 1: Domain Knowledge Complexity

**What it measures**: How much specialized, non-googleable expertise is baked in.

This is the single biggest source of estimation errors. A 5,000-line payments
system can take longer to rebuild than a 50,000-line e-commerce storefront —
because the payments system encodes years of PCI compliance knowledge, edge cases
in financial protocols, idempotency requirements, and regulatory understanding that
no library or tutorial will hand you.

| Domain Signal | Difficulty Contribution | Why |
|---------------|------------------------|-----|
| Payments / fintech (PCI, fraud detection, settlement) | Very High | Regulatory + financial correctness requirements, error = money lost |
| Healthcare (HL7, FHIR, HIPAA, EHR integration) | Very High | Protocol complexity + regulatory liability |
| Cryptography (custom implementations, HSM integration) | Extreme | Subtle bugs have catastrophic security consequences |
| Distributed consensus (Raft, Paxos, custom CRDTs) | Extreme | Correctness proofs required; academic-level knowledge |
| Real-time trading / high-frequency systems | Extreme | Microsecond constraints + financial correctness |
| Signal processing / DSP | Very High | Mathematical domain knowledge required |
| Compilers / language runtimes | Very High | Formal language theory + optimization |
| Robotics / embedded control systems | Very High | Hardware coupling + safety requirements |
| Blockchain / smart contracts | High | Immutability + security audit requirements |
| Tax calculation (multi-jurisdiction) | High | Regulatory complexity across jurisdictions |
| ML model training / research | High | Mathematics + compute infrastructure expertise |
| Multi-tenant SaaS isolation | Moderate-High | Data safety requirements + design patterns |
| Standard web application | Low | Well-documented patterns widely available |

**Scoring**:
- 0 standard domains only → +0
- 1 moderate domain → +1
- 1 high/very high domain → +2
- 1 extreme domain OR 2+ high domains → +3
- Multiple extreme domains → +4

---

### Dimension 2: Infrastructure Coupling

**What it measures**: How deeply the software is fused with its operational environment.

Infrastructure-coupled codebases are expensive to rebuild not because the infrastructure
is complex to configure once — but because the software makes hundreds of assumptions
about its environment. Rebuilding requires reconstructing all those assumptions, debugging
them against real cloud behavior, and managing the blast radius when something breaks in production.

| Signal | Difficulty Contribution |
|--------|------------------------|
| No infra-as-code, simple deployment | Low |
| Dockerfile + basic CI only | Low-Moderate |
| docker-compose with multiple services | Moderate |
| GitHub Actions / CircleCI with multi-stage pipelines | Moderate |
| Terraform or CloudFormation for cloud resources | Moderate-High |
| Kubernetes (Helm charts, custom operators, service mesh) | High |
| Multi-cloud or hybrid cloud architecture | High |
| ArgoCD / GitOps + advanced k8s | Very High |
| Custom Kubernetes operators or CRDs | Very High |

**Scoring**:
- No infra-as-code → +0
- Basic Docker/CI → +0.5
- Terraform or moderate k8s → +1
- Advanced k8s / multi-cloud → +2
- Custom operators / GitOps at scale → +3

---

### Dimension 3: Data Model Complexity

**What it measures**: The intellectual property encoded in the data structure.

The data model is often the hardest part of a system to recreate. Schema design decisions
represent years of domain understanding. The more tables, migrations, and complex relationships —
the more accumulated product thinking is baked in. Data models are also uniquely hard to rebuild
because mistakes have permanent consequences: you can't easily refactor a production schema
with millions of rows the way you can refactor a React component.

| Signal | Difficulty Contribution |
|--------|------------------------|
| < 10 tables / models | Low |
| 10–30 tables | Moderate |
| 30–60 tables | High |
| 60–100 tables | Very High |
| 100+ tables | Extreme |
| < 20 migrations | Low (young schema) |
| 20–100 migrations | Moderate (evolved product) |
| 100–300 migrations | High (mature, complex evolution) |
| 300+ migrations | Very High (long-running, heavily evolved) |
| Complex polymorphic relations, JSONB columns, custom types | +1 level |
| Event sourcing / CQRS / append-only patterns | +2 levels |

**Scoring** (tables + migrations combined):
- Simple (few tables, few migrations) → +0
- Moderate → +1
- Complex → +2
- Very complex → +3

---

### Dimension 4: Integration Surface Area

**What it measures**: The number of external contracts the system depends on.

Every external integration is a hidden complexity sink. It requires: reading API docs,
handling auth, writing error recovery, dealing with rate limits, testing against sandboxes,
managing credentials, and staying current as the external API evolves. Most integrations
also have subtle behavioral quirks that only reveal themselves in production.

The integration count is directly observable from the repo. The implied effort per
integration varies by API quality.

| Integration Count | Base Difficulty |
|------------------|----------------|
| 0–2 integrations | Low |
| 3–5 integrations | Moderate |
| 6–10 integrations | High |
| 11–15 integrations | Very High |
| 16+ integrations | Extreme |

**Complexity modifiers per integration type**:
- Simple REST APIs with good docs (Stripe, Twilio, SendGrid): standard
- Enterprise APIs (Salesforce, SAP, NetSuite): +1 level each
- Healthcare/financial APIs (EHR systems, FIX protocol, SWIFT): +2 levels each
- Poorly documented or legacy APIs: +1 level each
- Webhooks requiring signature verification and retry logic: +0.5 each

**Scoring**:
- 0–2 integrations → +0
- 3–5 → +1
- 6–10 → +2
- 11+ → +3
- Any enterprise/healthcare/financial APIs → +1 additional

---

### Dimension 5: Operational Maturity

**What it measures**: How production-hardened the system is.

There's an enormous difference between "code that works" and "code that runs reliably in production
under real load, with incident response, monitoring, and the operational discipline to recover from
failures." Operationally mature systems embed years of hard-won reliability engineering. The
infrastructure that makes them resilient took real humans a long time to design, implement, tune, and maintain.

The `scan_logs_and_validation.py` script surfaces most of these signals directly.

| Signal | Difficulty Contribution |
|--------|------------------------|
| No monitoring, no alerts, no runbooks | Low (prototype-grade) |
| Basic error tracking (Sentry) | Low-Moderate |
| Application metrics + dashboards | Moderate |
| SLO definitions + alerting thresholds | High |
| Runbooks + incident playbooks | High |
| Load tests + performance benchmarks | High |
| Chaos engineering / fault injection | Very High |
| Multi-region failover + DR procedures | Very High |
| Full observability (traces + metrics + logs correlated) | Very High |

**Scoring**:
- No observability → +0
- Basic monitoring → +0.5
- Metrics + dashboards + alerts → +1
- SLOs + runbooks + load tests → +2
- Chaos tests + multi-region + full observability → +3

---

## Composite Rebuild Difficulty Score

Sum the five dimension scores:

| Total Score | Rebuild Difficulty Rating | Typical Profile |
|-------------|--------------------------|-----------------|
| 0–2 | **LOW** | Simple CRUD app, standard stack, no specialized domains |
| 3–4 | **MODERATE** | Established web product, some integrations, moderate data model |
| 5–7 | **HIGH** | Multiple integrations, complex data model, some domain knowledge |
| 8–10 | **VERY HIGH** | Specialized domain + mature infrastructure + complex data model |
| 11–14 | **EXTREME** | Multiple extreme domains, heavy infra coupling, large data model |
| 15+ | **EXCEPTIONAL** | Rare; typically only in fintech, healthcare, or distributed systems infrastructure |

---

## Difficulty-to-Effort Multiplier

The rebuild difficulty rating feeds a final multiplier applied **after** all other
estimation adjustments. This is the layer the user's note correctly identified as missing:

| Rebuild Difficulty | Effort Multiplier |
|-------------------|------------------|
| LOW | 1.0× (no adjustment) |
| MODERATE | 1.15× |
| HIGH | 1.35× |
| VERY HIGH | 1.6× |
| EXTREME | 2.0–2.5× |
| EXCEPTIONAL | 2.5–4.0× |

This multiplier is applied to the **grand total hours** (after all other multipliers).
It represents the compounding effect of domain knowledge ramp-up time, institutional
knowledge reconstruction, and the inevitable discovery of hidden complexity during rebuild.

**Important**: Be explicit in the report about what drives the difficulty rating.
"VERY HIGH (score: 9) — driven by fintech payment domain (+2), Kubernetes + Terraform (+2),
67-table data model with 182 migrations (+3), 14 external integrations (+2)" is a defensible
finding. "VERY HIGH" alone is not.

---

## Example Profiles

### CRUD SaaS (e-commerce storefront)
- Domain: Standard web → +0
- Infra: Docker + GitHub Actions → +0.5
- Data: 25 tables, 45 migrations → +1
- Integrations: Stripe, SendGrid, S3 (3) → +1
- Operational: Sentry + basic dashboards → +0.5
- **Score: 3 → MODERATE → 1.15× multiplier**

### Fintech Payments Infrastructure
- Domain: Payments + fraud detection → +2
- Infra: Kubernetes + Terraform + multi-region → +2
- Data: 80 tables, 300 migrations → +3
- Integrations: 14 (banks, card networks, FX providers, compliance APIs) → +3+1
- Operational: SLOs + runbooks + load tests → +2
- **Score: 13 → EXTREME → 2.0–2.5× multiplier**

### ML Research Repository (12k LOC)
- Domain: ML training + custom model architecture → +3
- Infra: Docker only → +0.5
- Data: Few tables, simple schema → +0
- Integrations: Cloud storage, HuggingFace → +1
- Operational: Minimal → +0
- **Score: 4.5 → HIGH → 1.35× multiplier**
*(Note: LOW LOC but HIGH difficulty — exactly the case where LOC lies)*

### Enterprise Monolith (300k LOC)
- Domain: Standard enterprise software → +1
- Infra: CI/CD + basic cloud → +1
- Data: 150 tables, 500 migrations → +3
- Integrations: 8 (ERP, CRM, SSO, email, storage) including Salesforce → +2+1
- Operational: Moderate monitoring → +1
- **Score: 9 → VERY HIGH → 1.6× multiplier**
*(Note: HIGH LOC but VERY HIGH difficulty, not EXTREME — domain knowledge is moderate)*
