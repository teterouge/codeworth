---
name: repo-estimator
description: Analyze a code repository and produce a detailed human time and cost estimate for building it from scratch. Use this skill whenever the user wants to know how long it would take a human developer or team to build a codebase, how much it would cost to recreate a project, what the engineering effort of a repo is, or wants a "what's this worth?" / "how much work went into this?" type of analysis. Also trigger for requests like "estimate this project", "how many dev hours is this", "what would it cost to build this", "audit this repo for effort", "scope this codebase", or any time someone shares a repo path or GitHub URL and asks about effort, time, team size, or cost. Even if they don't use the words "estimate" or "cost" — if they share code and ask about effort or what it would take to build, use this skill.
---

# Repo Estimator

This skill produces a thorough, defensible estimate of the human time and cost required to build a codebase from scratch. It's designed for founders evaluating acquisitions, engineers scoping migrations, freelancers pricing projects, or anyone who wants to understand the real effort baked into a repository.

The output should feel like something a senior engineering consultant would hand over — not a naive line-count calculation, but a judgment-call-rich analysis that accounts for complexity, architecture, rework cycles, and team dynamics.

## What You're Estimating

You're answering: **"If a competent team started from zero today, how long would it take and what would it cost to build what's in this repo?"**

This is subtly different from:
- "How long did it take the original team?" (You don't know their pace, mistakes, or false starts)
- "How many lines of code are there?" (LOC is a famously poor proxy for effort)
- "What's the maintenance cost?" (That's a different question — don't conflate it unless asked)

Assume the hypothetical team is **competent but unfamiliar with the domain**. They need to design, build, test, and document — not just type.

---

## Step 1: Understand the Request

Before diving in, understand what the user actually needs:

- **Target**: Is this a local path, a GitHub URL, or a zip? Handle accordingly.
- **Purpose**: Are they buying/selling, scoping a rewrite, hiring, or just curious? This shapes how you frame the output.
- **Team assumption**: Should you estimate for a solo developer, a small startup team (2–4), or a mid-size engineering org? Ask if unclear — it affects hours significantly.
- **Rate card**: Do they want costs in USD? A specific region or seniority mix? Default to US market rates if unspecified (see references/rate-cards.md).

If the user provides a GitHub URL, use shell tools to clone it to a temp directory. If they provide a local path, work from there directly.

---

## Step 2: Repository Reconnaissance

Run **both** analysis scripts to gather hard data before making any judgment calls:

```bash
# Source code analysis
python scripts/analyze_repo.py <repo_path>

# Log, validation, and artifact analysis
python scripts/scan_logs_and_validation.py <repo_path>
```

The first script covers source code composition and complexity signals. The second surfaces evidence of effort that lives *outside* the code itself: test output, compliance documents, migration histories, CI/CD configs, changelogs, ADRs, and more. Both are needed for a complete picture.

Also do a **manual walkthrough** of the repo structure. The scripts catch what they can measure; you catch what requires judgment:

- Read the README, any architecture docs, and top-level config files
- Note the overall architecture pattern (monolith, microservices, monorepo, etc.)
- Identify the primary language(s) and frameworks
- Look for evidence of complexity: auth systems, payment integrations, real-time features, ML pipelines, complex state management, multi-tenancy, etc.
- Check test coverage and quality — well-tested code represents more total work than the implementation alone
- Note infrastructure-as-code, CI/CD pipelines, and DevOps configuration
- Identify any non-obvious work: data migrations, seed scripts, custom tooling, generated code
- Note whether this appears to be a product run by a human team (multiple contributors, release history, PM artifacts) vs. a solo side project

---

## Step 3: Complexity Classification + Rebuild Difficulty Rating

This step produces two distinct outputs that serve different purposes. Do both before moving on.

### 3a. Component Tier Classification

Use the complexity taxonomy in `references/complexity-guide.md` to classify each major component of the codebase.

Every component falls into one of four tiers:

| Tier | Label | Description |
|------|-------|-------------|
| 1 | Boilerplate | Standard scaffolding, CRUD, config files, generated code |
| 2 | Moderate | Custom business logic, non-trivial integrations, standard auth |
| 3 | Complex | Custom algorithms, real-time systems, complex state, multi-service orchestration |
| 4 | Specialized | ML/AI pipelines, custom protocols, novel architecture, research-grade work |

Be honest about tier assignment. The biggest estimation errors come from miscategorizing Tier 3 work as Tier 2. When in doubt, round up.

### 3b. Rebuild Difficulty Rating

**This is not the same as component complexity.** Rebuild difficulty answers: *How hard would it be for a competent team to reconstruct the knowledge encoded in this repo from scratch?*

LOC and tier classifications measure volume and technical sophistication. Rebuild difficulty measures knowledge density — the specialized understanding, institutional context, and hard-won production experience that can't be acquired by reading the code alone.

Read `references/rebuild-difficulty.md` for the full scoring model. The `analyze_repo.py` script outputs a `rebuild_difficulty` block in its JSON — use that as a starting point, but apply your own judgment based on what you observed in the manual walkthrough.

Score the repository across five dimensions:

| Dimension | What It Measures | Source |
|-----------|-----------------|--------|
| Domain Knowledge | Specialized domains (fintech, healthcare, crypto, compilers, etc.) | Script + manual review |
| Infrastructure Coupling | Depth of infra-as-code, k8s, Terraform, GitOps | Script + key files |
| Data Model Complexity | Tables, migrations, schema evolution depth | Script counts + migrations dir |
| Integration Surface Area | External API count, enterprise API weight | Script + package files |
| Operational Maturity | SLOs, runbooks, load tests, chaos engineering | Script + scan_logs output |

**Compute the composite score and assign a rating**:

| Score | Rating | Effort Multiplier |
|-------|--------|------------------|
| 0–2 | LOW | 1.0× |
| 3–4 | MODERATE | 1.1–1.2× |
| 5–7 | HIGH | 1.25–1.45× |
| 8–10 | VERY HIGH | 1.5–1.7× |
| 11–14 | EXTREME | 1.9–2.5× |
| 15+ | EXCEPTIONAL | 2.5–4.0× |

**This multiplier is applied at the end of Step 9**, after all other multipliers, as a final adjustment to total hours. It represents the knowledge ramp-up cost that component-level estimation systematically misses.

Always be specific about what drives the rating. "VERY HIGH (score: 9) — fintech payment domain (+2), Kubernetes+Terraform (+2), 67-table data model with 182 migrations (+3), 14 external integrations (+2)" is a defensible finding. "VERY HIGH" alone is not.

---

## Step 4: Component Breakdown

Decompose the codebase into logical components. Good components are things a project manager would actually track — not individual files, not vague categories like "backend."

Examples of good component granularity:
- User authentication & authorization system
- Payment processing integration (Stripe, etc.)
- Admin dashboard UI
- REST API layer
- Real-time notification system
- Data pipeline / ETL jobs
- Infrastructure & deployment configuration
- Test suite
- Documentation

For each component, estimate:
- **Tier**: 1–4 (from above)
- **Raw hours**: Core implementation time for a competent solo developer
- **Complexity multiplier**: From `references/complexity-guide.md`
- **Adjusted hours**: Raw × multiplier

Don't round aggressively. "80 hours" feels more credible than "80–120 hours" for a component you can actually analyze.

---

## Step 5: Apply Estimation Multipliers

Raw component hours are never the full story. Apply these multipliers to the total adjusted hours:

**Rework & iteration factor**: 1.3–1.6×
Real development isn't linear. Design changes, bugs, PRs, re-architecting decisions. Use 1.3× for simple projects, 1.6× for complex or novel ones.

**Testing & QA factor**: depends on test coverage observed
- No tests: add 0% (but note it in caveats — the hours are "artificially low")
- Light tests: add 15%
- Thorough unit tests: add 25%
- Full test suite with integration/e2e: add 35–40%

**Documentation & onboarding**: 5–15% of total
Higher if there's extensive docs, a public API, or SDK.

**Project management & coordination overhead**: 
- Solo developer: 0%
- 2–4 person team: add 10%
- 5+ person team: add 20–25%

**Integration & glue work**: 
Often underestimated. If the repo has 5+ third-party integrations, add 10–20%.

See `references/multipliers.md` for the full table with worked examples.

---

## Step 6: Log & Validation Artifact Effort

Review the output of `scan_logs_and_validation.py`. This script surfaces files that represent real effort often invisible in source code: CI/CD pipelines, compliance documents, migration histories, test coverage reports, performance test scripts, monitoring configs, ADRs, changelogs, and spec documents.

For each artifact category found, interpret what it implies using `references/log-validation-analysis.md`. The script provides raw hour ranges — your job is to apply judgment about whether those artifacts look genuine and proportionate.

**Key questions to ask**:
- Do the migration files look real (many, with meaningful names) or sparse/placeholder?
- Is there actual compliance documentation or just a template SECURITY.md?
- Are the CI/CD pipelines simple (one stage) or sophisticated (multi-environment, matrix testing)?
- Does the changelog have real release entries with feature descriptions, or just a few lines?

Add the validated artifact hours to the estimate as a separate breakdown, attributed by role (Engineering, DevOps, PM, QA). Do not fold them silently into engineering hours — they need to be visible so the user can understand where the numbers come from.

---

## Step 7: Product Manager Effort (if applicable)

If the repo represents a **product run by a human team** (not a solo side project or pure library), estimate PM effort separately. PMs don't appear in source code but their work is implied by every feature, API design, and user-facing decision.

Read `references/pm-effort-guide.md` for the full methodology. At a high level:

1. Count distinct product features or user-facing capabilities
2. Identify PM artifact signals (specs, ADRs, detailed changelogs, feature flags, multi-tenant roles)
3. Classify the product type (internal tool vs B2B SaaS vs consumer app vs enterprise platform)
4. Apply the appropriate PM-to-engineering ratio from `references/rate-cards.md`
5. Break down PM hours by activity: discovery, spec writing, stakeholder management, acceptance testing, post-launch

**When to skip this step**: If the repo is a solo developer project (single contributor in git history, no team structure), a pure open source library, or a developer tool with no product complexity — note it and move on.

---

## Step 8: Team Composition

Recommend a realistic team composition for building this project, based on what you observed. Consider:

- What roles are actually needed? (frontend, backend, DevOps, ML, PM, design, QA, etc.)
- What seniority mix makes sense? A complex auth system needs a senior; a landing page doesn't.
- Could a solo full-stack developer handle it, or does it require specialists?
- Does the product complexity warrant a dedicated PM, or would the tech lead cover product?

Express this as a recommended team and explain why. This helps the user reality-check the estimate.

---

## Step 9: Cost Calculation

Apply appropriate hourly rates from `references/rate-cards.md`.

Default to **US market rates, mid-seniority (3–7 years experience)** unless the user specified otherwise. Always show the rate assumptions clearly so the user can adjust.

Cost must be calculated **across all roles** identified in previous steps:
- Engineering hours × engineering blended rate
- PM hours (Step 7) × PM rate ($110/hr US default)
- DevOps / artifact hours (Step 6) × DevOps rate
- QA hours × QA rate

Sum these for a **subtotal**, then apply the **Rebuild Difficulty Multiplier** from Step 3b as a final adjustment:

```
Final Total Hours = Subtotal Hours × Rebuild Difficulty Multiplier
```

This is the correct place to apply it — after all component and artifact hours are summed, and after all the standard multipliers from Step 5. It represents the knowledge ramp-up cost that falls across the whole estimate, not within any single component.

Then apply scenario spread to the final total:
- **Low estimate**: 10th percentile (smooth execution, experienced team, limited scope creep)
- **Mid estimate**: 50th percentile (realistic)
- **High estimate**: 90th percentile (real-world friction, scope discoveries, iteration)

Flag any external cost items (penetration tests, SOC 2 audits, legal review) as separate budget line items — these are not hourly rates and should not be folded into the estimate.

The spread between low and high should feel honest. If you're collapsing it artificially, you're not being useful — you're giving false precision.

---

## Step 10: Output the Report

Use this exact report structure:

```
# Repository Estimation Report
**Repo**: [name/path]
**Analyzed**: [date]
**Estimated for**: [solo dev / small team / etc.]

---

## Executive Summary
[2–4 sentences. What is this project? What's the headline number? Any important caveats?]

**Total estimated effort**: [X–Y weeks] / [N–M person-months]
**Cost range**: $[low] – $[high] USD (all roles combined)
**Confidence**: [Low / Medium / High] — [one sentence explaining why]

---

## Repository Overview
- **Primary language(s)**:
- **Framework(s)**:
- **Architecture pattern**:
- **Lines of code (excluding generated/vendor)**:
- **Test coverage**: [None / Minimal / Moderate / Thorough]
- **Notable integrations**:
- **Product type**: [Internal tool / B2B SaaS / Consumer app / Developer tool / Enterprise platform / Solo project]

---

## Rebuild Difficulty Assessment

**Rating**: [LOW / MODERATE / HIGH / VERY HIGH / EXTREME / EXCEPTIONAL]
**Score**: [N]/15+ — **Effort multiplier**: [X–Y×] applied to final total

| Dimension | Score | Key Signals |
|-----------|-------|-------------|
| Domain Knowledge | [N] | [detected domains, e.g., "payments_fintech, healthcare"] |
| Infrastructure Coupling | [N] | [e.g., "Kubernetes + Terraform + ArgoCD"] |
| Data Model Complexity | [N] | [e.g., "67 tables, 182 migrations"] |
| Integration Surface Area | [N] | [e.g., "14 integrations including Salesforce, Stripe, Plaid"] |
| Operational Maturity | [N] | [e.g., "SLOs defined, runbooks present, load tests found"] |
| **Total** | **[N]** | |

**Why this matters**: [1–2 sentences explaining the LOC vs. rebuild difficulty gap for this specific repo. E.g., "At 25,000 LOC this appears modest, but the fintech domain, 182 schema migrations, and 14 external API contracts encode years of production knowledge that far exceeds what the line count suggests."]

---

## Component Breakdown (Engineering)

| Component | Tier | Raw Hours | Multiplier | Adjusted Hours | Notes |
|-----------|------|-----------|------------|----------------|-------|
| [name]    | [1-4]| [N]       | [1.0–2.5×] | [N]            | [key judgment calls] |
| ...       |      |           |            |                |       |
| **Total** |      | **[N]**   |            | **[N]**        |       |

---

## Estimation Adjustments (Engineering)

| Factor | Multiplier Applied | Resulting Hours |
|--------|--------------------|-----------------|
| Rework & iteration | [1.3–1.6×] | [N] |
| Testing & QA | [+N%] | [N] |
| Documentation | [+N%] | [N] |
| Team coordination | [+N%] | [N] |
| Integration glue work | [+N%] | [N] |
| **Engineering Subtotal** | | **[N] hours** |

---

## Validation & Documentation Artifact Analysis

**Artifacts found**: [comma-separated list of artifact types discovered]

| Artifact Type | Files Found | Implied Hours | Role |
|--------------|-------------|---------------|------|
| CI/CD pipeline configs | [N] | [N hrs] | DevOps / Engineering |
| Database migrations | [N] | [N hrs] | Engineering |
| Test coverage / result reports | [N] | [N hrs] | Engineering / QA |
| Load / performance test scripts | [N] | [N hrs] | Engineering |
| Compliance / security documents | [type] | [N hrs] | PM / Legal / Security |
| API contract / collection files | [N] | [N hrs] | Engineering / QA |
| Monitoring / alert configs | [N] | [N hrs] | DevOps |
| Changelog / release notes | [N versions] | [N hrs] | PM / Engineering |
| Architecture Decision Records | [N] | [N hrs] | Engineering / PM |
| Spec / PRD documents | [N] | [N hrs] | PM |
| **Artifact Subtotal** | | **[N] hours** | |

*(Only include rows where artifacts were actually found)*

---

## Product Manager Effort

**Applicable**: [Yes — [product type] / No — [reason, e.g., solo project, pure library]]

*(If not applicable, note why and skip the table below)*

**PM estimation basis**: [What signals drove the estimate — feature count, product type, artifact evidence]

| PM Activity | Estimated Hours | Evidence |
|-------------|----------------|----------|
| Discovery & user research | [N] | [signals observed] |
| Specification & story writing | [N] | [signals observed] |
| Stakeholder & roadmap management | [N] | [signals observed] |
| Acceptance testing & release coordination | [N] | [signals observed] |
| Post-launch analysis & iteration | [N] | [signals observed] |
| **PM Subtotal** | **[N]** | |

**PM-to-engineering ratio applied**: [X%] ([product type category])

---

## Recommended Team

[Describe the recommended team with all relevant roles, seniority, and rationale]

**Time to ship** (working in parallel):
- Aggressive timeline: [N weeks]
- Realistic timeline: [N weeks]
- Conservative timeline: [N weeks]

---

## Unified Cost Estimate

**Rate assumptions**: [e.g., US market rates, mid-senior mix]

| Role | Hours | Rate | Subtotal |
|------|-------|------|----------|
| Engineering (blended) | [N] | $[X]/hr | $[Y] |
| DevOps / Platform | [N] | $[X]/hr | $[Y] |
| QA / Testing | [N] | $[X]/hr | $[Y] |
| Product Management | [N] | $[X]/hr | $[Y] |
| **Total (mid scenario)** | **[N]** | | **$[Y]** |

| Scenario | Total Hours | Total Cost |
|----------|-------------|------------|
| Low (10th percentile) | [N] | $[Y] |
| Mid (50th percentile) | [N] | $[Y] |
| High (90th percentile) | [N] | $[Y] |

*(External cost items not included above — budget separately if applicable)*

---

## Key Complexity Drivers

[Bullet list of 3–6 factors that most significantly drive the estimate. Be specific:
not "complex codebase" but "custom real-time WebSocket orchestration with reconnection logic";
not "lots of PM work" but "multi-sided marketplace with 4 distinct user roles and enterprise buyer workflow"]

---

## Caveats & Assumptions

[Honest list of what could make this estimate wrong. Include:]
- What was NOT analyzed (design assets, database contents, proprietary dependencies)
- What was assumed (team seniority, clean execution, no major scope discoveries)
- What was excluded from the hourly estimate (ongoing maintenance, hosting, third-party API costs, licensing)
- Any external cost items that should be budgeted separately (pentest: $15–50K, SOC 2 audit: $30–100K, legal review: varies)
- Any red flags or uncertainty sources observed
```

---

## Quality Bar

A good estimate is:

**Specific**: "Authentication system including OAuth2, JWT, refresh tokens, and role-based access control — approximately 60 hours at Tier 2/3 boundary" beats "auth stuff — 1 week."

**Complete across roles**: Engineering hours alone undercount the true cost of building a product. Always show PM and DevOps separately so the user can see and challenge those assumptions.

**Honest about uncertainty**: If you genuinely can't tell what a directory does, say so and add it to caveats rather than guessing at high confidence.

**Defensible**: Every number should trace back to something observable. If someone asks "why 40 hours for the API layer?", you should be able to point to the number of endpoints, middleware, auth checks, and validation logic that justify it.

**Non-naive**: Don't just divide LOC by some productivity rate. That produces garbage. Complexity is the real driver. A 200-line real-time bidding system is worth more than a 2,000-line CRUD app.

---

## Edge Cases

**Monorepos**: Estimate each package/app separately, then sum. Call out shared infrastructure separately.

**Generated code**: Note it but don't count it toward effort — no one hand-wrote that Prisma schema output or protobuf generated file. Do count the schema/spec that drives generation.

**Vendor code / node_modules / vendored deps**: Exclude entirely.

**Forks with modifications**: Only count the delta from the upstream, not the full fork.

**Stale or abandoned code**: Note files/directories that appear unmaintained and exclude from estimate with a callout.

**No tests**: Flag prominently. An untested codebase will cost significantly more to rewrite safely because the team has to write tests during the rebuild, and the lack of tests suggests the original was built fast and loose — meaning more undocumented complexity.

**Solo developer projects**: If all git commits come from one person, PM time is already folded into engineering time. Do not double-count — note it explicitly in the PM section.

---

## Reference Files

Read these when you need specific guidance:

- `references/complexity-guide.md` — Full complexity tier definitions with examples and multiplier tables
- `references/rate-cards.md` — Hourly rates by role, seniority, and region (including PM and design roles)
- `references/multipliers.md` — All estimation multipliers with worked examples
- `references/pm-effort-guide.md` — PM effort estimation methodology and product type ratios
- `references/log-validation-analysis.md` — How to interpret log files, test artifacts, and validation documents
- `references/rebuild-difficulty.md` — Rebuild difficulty scoring model: five dimensions, composite score, effort multiplier table, and worked examples
