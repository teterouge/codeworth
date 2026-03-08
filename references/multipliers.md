# Estimation Multipliers

This document defines all the adjustment factors applied after the initial component-level estimates. These multipliers are grounded in empirical software estimation research (Cone of Uncertainty, COCOMO II, industry studies by QSM and others) and practical consulting experience.

---

## The Multipliers at a Glance

| Factor | Range | Applied to |
|--------|-------|-----------|
| Rework & iteration | 1.3–1.6× | Subtotal of adjusted component hours |
| Testing & QA | +0–40% | Subtotal after rework |
| Documentation & onboarding | +5–15% | Subtotal |
| Team coordination overhead | +0–25% | Subtotal |
| Integration & glue work | +0–20% | Subtotal |

Apply these in sequence, not all at once, so each builds on the last. Alternatively, you can compute them separately and add the deltas — either approach is fine as long as you're transparent.

---

## 1. Rework & Iteration Factor

**Range**: 1.3–1.6×  
**Applied to**: Raw adjusted component hours

Why this matters: Software development is never linear. Developers write code, discover it doesn't quite fit, refactor, get code review feedback, discover integration issues, and iterate. Barry Boehm's research and subsequent empirical studies consistently show that rework accounts for 30–60% of total development effort.

| Project Characteristics | Multiplier |
|------------------------|-----------|
| Simple, well-defined scope, experienced team, established stack | 1.3× |
| Typical web/mobile application with some unknowns | 1.4× |
| Complex product, some novel tech or unclear requirements | 1.5× |
| Highly novel, research-adjacent, or rapidly changing requirements | 1.6× |

**Signals to use the high end**:
- Multiple major architecture layers (separate frontend, API, workers, infra)
- Significant third-party integrations (each integration is a coordination point for bugs)
- Real-time or distributed systems (harder to test, more edge cases)
- No existing tests (harder to refactor safely → more rework time)
- Novel tech stack the team hasn't used before

---

## 2. Testing & QA Factor

**Range**: +0–40%  
**Applied to**: Hours after rework factor

This factor represents the effort required to build and maintain a quality assurance system for the codebase. If the repo already has a test suite, count those test files as part of the component breakdown (they're real work) — this multiplier is then reduced. If the repo has no tests, a rebuild would need to add them, so you add the cost here.

| Test Coverage Observed | Additive Percentage | Notes |
|------------------------|--------------------|----|
| No tests at all | +25% | A rebuild should have tests. Add the cost. |
| Minimal tests (< 20% coverage) | +15% | Some testing culture exists, extend it |
| Moderate tests (20–60% coverage) | +10% | Core paths covered, gaps exist |
| Thorough tests (60–80% coverage, integration tests present) | +5% | Already well-counted in components |
| Comprehensive tests (80%+, E2E, load tests) | +0% | Already fully counted in component breakdown |

**Additionally**: If there's evidence of manual QA processes (QA team, bug reports, staging environments), add 5% for QA coordination.

---

## 3. Documentation & Onboarding Factor

**Range**: +5–15%  
**Applied to**: Running subtotal

Documentation is often invisible in code review but very visible in total project cost.

| Documentation Scope | Additive Percentage |
|--------------------|---------------------|
| No docs (README only or nothing) | +5% (minimal docs still need writing) |
| Basic docs (README, setup guide, some inline comments) | +7% |
| Developer docs (architecture decisions, API docs, runbooks) | +10% |
| Public-facing docs (user guides, SDK docs, API reference site) | +15% |
| Both developer and public docs | +15–18% |

**Look for**:
- `/docs` directories
- Wiki links in the README
- OpenAPI/Swagger specs (these take time to write and maintain)
- Storybook or component documentation
- Architecture Decision Records (ADRs)
- Runbooks or operational guides

---

## 4. Team Coordination Overhead

**Range**: +0–25%  
**Applied to**: Running subtotal

The more people involved, the more time goes to coordination: standups, code reviews, design discussions, PR back-and-forth, onboarding, and knowledge transfer.

| Team Size | Additive Percentage |
|-----------|---------------------|
| Solo developer | +0% |
| 2 developers | +5% |
| 3–4 developers | +10% |
| 5–8 developers | +18% |
| 9+ developers | +25% |

**Note**: These overheads apply to the total project. A 5-person team completes work faster (lower calendar time) but the total hours are higher than a 2-person team would be. That's normal and expected — coordination is real work.

If the project clearly required multiple specialized teams (frontend team, backend team, infra team), use the high end of the range. If it looks like a tightly-knit small team could execute it, use the low end.

---

## 5. Integration & Glue Work Factor

**Range**: +0–20%  
**Applied to**: Running subtotal

Third-party integrations look simple in the code (a few API calls) but hide significant hidden costs: reading documentation, handling rate limits and errors, testing against sandbox environments, managing credentials and secrets, dealing with API changes, and writing robust retry logic.

| Integration Complexity | Additive Percentage |
|-----------------------|---------------------|
| No external integrations (fully self-contained) | +0% |
| 1–2 simple integrations (e.g., SendGrid, basic S3) | +3% |
| 3–5 integrations (payment, email, auth, storage, analytics) | +8% |
| 6–10 integrations, some complex (ERP, CRM, healthcare APIs) | +15% |
| 10+ integrations or highly complex/underdocumented APIs | +20% |

**Signals for high integration cost**:
- Financial data providers (Plaid, Stripe Connect, etc.)
- Healthcare APIs (HL7/FHIR, EHR integrations)
- Enterprise ERP systems (Salesforce, SAP, NetSuite)
- Government / public sector data APIs
- Multiple payment gateways
- Legacy SOAP/XML APIs

---

## Cumulative Example

Here's how the multipliers compound for a moderately complex SaaS application:

**Raw component hours**: 450 hours  

| Step | Factor Applied | Running Total |
|------|---------------|--------------|
| Component tier multipliers | Applied per-component | 450 hrs (adjusted) |
| Rework & iteration | ×1.4 | 630 hrs |
| Testing & QA (moderate tests) | +10% | 693 hrs |
| Documentation (developer docs) | +10% | 762 hrs |
| Team coordination (3-person team) | +10% | 838 hrs |
| Integration glue (5 integrations) | +8% | 905 hrs |
| **Grand Total** | | **~905 hours** |

At $130/hr (US mid-senior blended): **$117,650**  
At a 3-person team, 30 hrs/week each: ~10 weeks calendar time

---

## What's Not Included (Common Scope Exclusions)

Be explicit in the report about what these estimates do NOT cover:

**Ongoing costs (not one-time)**:
- Hosting, infrastructure, and cloud costs
- Third-party API subscription fees
- License costs for commercial libraries
- Ongoing maintenance and bug fixes

**Pre-code work**:
- Product discovery and requirement definition
- UI/UX design (if no design files are in the repo)
- Business analysis and technical scoping
- Architecture review / technical design

**Post-launch work**:
- User onboarding and support tooling
- Analytics and monitoring setup
- Performance tuning under real load
- Security audits

**Organizational costs**:
- Recruiting and hiring (if the team doesn't exist)
- Contractor management overhead
- Legal / compliance review
- Project management (if not counted in team overhead above)

---

## Uncertainty Range Guide

| Confidence Level | Spread to Use | When Appropriate |
|-----------------|--------------|-----------------|
| High | ±15% | Simple, well-understood codebase with good docs |
| Medium | ±25–30% | Typical application, some unknowns |
| Low | ±40–50% | Large/complex codebase, missing context, unfamiliar domain |
| Very Low | ±60%+ | Major gaps in analysis (missing source, no docs, novel tech) |

The report should state confidence level and the reason. An honest ±50% range is more useful than a falsely precise ±10% one.
