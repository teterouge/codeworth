# PM Effort Guide

When estimating a product run by a human team, product management is a real cost that must be estimated separately from engineering. This guide explains how to read a repository for PM effort signals and calculate PM hours.

---

## What PM Effort Covers

Product manager time breaks into several categories that are distinct from engineering:

**Discovery & research** — User interviews, competitive analysis, market research, defining the problem space. The output shows up indirectly in product decisions baked into the code.

**Specification & planning** — Writing PRDs, user stories, acceptance criteria, API contracts. Evidence: spec directories, detailed changelogs, ADRs, versioned API docs with clear behavioral descriptions.

**Stakeholder management** — Alignment meetings, executive reviews, sales engineering support, customer calls. Not visible in code but proportional to product complexity and number of user types.

**Prioritization & roadmap work** — Deciding what gets built, in what order, for whom. Every product feature represents PM decisions upstream.

**Acceptance testing & release coordination** — Validating builds against specs, coordinating launches, writing release notes. Evidence: CHANGELOG entries, release tags, migration guides.

**Post-launch analysis** — Reviewing analytics, triaging feedback, defining iterations. Evidence: multiple versions of the same feature, A/B test code, feature flags, gradual rollout logic.

---

## How to Estimate PM Hours from Repo Signals

### Step 1: Count Distinct Product Features

Walk the repo and identify distinct user-facing capabilities — not technical components, but things a user or customer would describe as "the product does X."

Examples:
- User account management (signup, login, profile, deletion)
- Dashboard with analytics widgets
- File upload and processing pipeline
- Team collaboration and sharing
- Billing and subscription management
- Admin panel for internal operators
- Public API with developer documentation

A feature like "user authentication" is one PM feature, even though it might span 10 files. A feature like "multi-currency billing with prorations and invoice generation" is meaningfully more PM work than "basic Stripe subscription."

**Rule of thumb**: 8–20 hours of PM work per distinct feature for a B2B SaaS, depending on complexity. Discovery-heavy features (novel user experiences, complex workflows) run higher. Table-stakes features (standard auth, basic CRUD) run lower.

---

### Step 2: Read the Evidence of PM Artifacts

Look for signals in the repo that indicate how much PM rigor was applied:

**High PM signal (more hours):**
- `/docs/specs/`, `/docs/prd/`, or similar directories with design documents
- Detailed ADRs (Architecture Decision Records) — these are often written or prompted by PM decisions
- Comprehensive CHANGELOG with feature descriptions, not just commit hashes
- OpenAPI/Swagger specs with detailed descriptions, examples, and error codes
- Feature flags or A/B testing infrastructure — implies experimentation and iteration
- Multiple major versions of an API or UI pattern (v1, v2, etc.) — implies planned evolution
- Separate staging/canary/production environments — implies release management
- User-facing error messages written with care — implies PM-specified copy
- Granular permissions/roles system — implies extensive PM work on user types and access models
- Onboarding flows, tooltips, empty states — implies PM designed the full user journey

**Low PM signal (fewer hours):**
- README-only documentation
- No changelogs or minimal commit messages
- Single API version with no versioning strategy
- No feature flags or experimentation code
- Basic error handling without user-facing copy
- Solo developer repo with no evidence of team coordination

---

### Step 3: Assess Product Complexity

Product complexity is not the same as technical complexity. A technically simple app can require enormous PM effort if:
- It serves multiple distinct user types (customers, admins, vendors, support agents)
- It has regulatory requirements (healthcare, finance, legal)
- It involves external stakeholders (partner integrations, enterprise customers, API consumers)
- It requires consensus across teams or business units
- It has complex pricing or packaging decisions

**Signals of high stakeholder complexity:**
- Multi-tenant architecture with organization/workspace concepts
- Role hierarchies with 4+ distinct roles
- Partner/vendor portals alongside customer-facing features
- Compliance-adjacent features (audit logs, data retention, export capabilities, GDPR tooling)
- White-labeling or multi-brand support
- Sales-assisted signup flows (enterprise tier indicators)

---

### Step 4: Apply the Right Ratio

Use the ratios from `references/rate-cards.md` as your baseline:

| Product Type | PM Hours as % of Engineering Hours |
|-------------|-------------------------------------|
| Internal tool / admin panel | 5–10% |
| Developer tool / API / SDK | 10–15% |
| B2B SaaS product | 15–25% |
| B2C consumer product | 20–30% |
| Multi-sided marketplace | 25–35% |
| Enterprise platform (complex stakeholders) | 30–40% |

**Adjust up if:**
- Multiple user types with distinct workflows
- Evidence of significant experimentation (feature flags, A/B tests)
- Complex pricing / packaging decisions baked into the code
- Regulatory compliance features (implies PM-driven compliance work)
- External-facing API with developer experience considerations

**Adjust down if:**
- Solo developer project (PM = developer themselves, already counted)
- Pure internal tool with a single user type
- Open source project where PM is community-driven

---

### Step 5: Calculate PM Cost

Once you have PM hours:

```
PM Cost = PM Hours × PM Hourly Rate
```

Use $110/hr (mid-senior PM, US) as the default unless specified otherwise. See `references/rate-cards.md` for regional rates.

**Express PM hours as a separate line item in the report**, not folded into engineering hours. This makes it easy for the user to adjust independently.

---

## Output Format for PM Section

Add this section to the report between "Recommended Team" and "Cost Estimate":

```
## Product Management Effort

**PM effort estimation basis**: [Describe what signals drove the estimate — e.g., 
"12 distinct product features identified, B2B SaaS with 3 user types, evidence 
of spec documents in /docs/"]

**Estimated PM hours**: [N] hours  
**PM-to-engineering ratio applied**: [X%] ([product type category])

| PM Activity | Estimated Hours | Evidence |
|-------------|----------------|----------|
| Discovery & user research | [N] | [what signals suggest this] |
| Specification & story writing | [N] | [what signals suggest this] |
| Stakeholder & roadmap management | [N] | [what signals suggest this] |
| Acceptance testing & release coordination | [N] | [what signals suggest this] |
| Post-launch analysis & iteration | [N] | [what signals suggest this] |
| **Total PM hours** | **[N]** | |

**PM Cost**: $[N] at $[rate]/hr ([seniority, region])
```

---

## PM Estimation Notes for Common Repo Patterns

**API-only repos (no frontend)**
PM effort is lower but not zero — API design, developer experience, documentation strategy, and versioning policy all require PM attention. Use 10–15% of engineering hours.

**Admin-only panels**
These are often built to spec for internal operators. PM effort is light — mostly requirements gathering from the internal team. Use 5–8%.

**Multi-product monorepos**
Estimate PM per product or major surface, then sum. Don't apply a single ratio to the whole monorepo — different products within it may have very different PM intensity.

**Solo developer projects**
If the repo shows all the hallmarks of a solo project (single contributor in git, no team structure in code), the developer was their own PM. Don't double-count — note that PM time is folded into the engineering estimate rather than adding it separately.

**Open source projects**
Community-driven OSS has distributed PM effort (issues, RFCs, mailing lists, contributor discussions). This is genuinely hard to estimate from the repo alone. Note the limitation and provide a range rather than a point estimate.
