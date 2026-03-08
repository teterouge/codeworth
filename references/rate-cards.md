# Rate Cards

Hourly rates for software engineering roles by seniority and region. Used by the repo-estimator skill to calculate cost estimates.

**Last updated**: 2025. These are market rates for employed or contracted developers — not agency rates (which run 2–3× higher) and not offshore outsourcing rates (which are noted separately).

---

## US Market Rates (Default)

When the user doesn't specify a region, use these. These are blended contract/freelance rates for independent developers. Full-time employee fully-loaded cost (salary + benefits + overhead) runs approximately 1.4–1.6× the salary equivalent per hour.

**Engineering roles:**

| Role | Junior (0–2 yrs) | Mid (3–6 yrs) | Senior (7–12 yrs) | Staff/Principal (12+ yrs) |
|------|-----------------|---------------|-------------------|--------------------------|
| Frontend Engineer | $60–80/hr | $90–130/hr | $140–180/hr | $180–250/hr |
| Backend Engineer | $65–85/hr | $95–135/hr | $145–190/hr | $190–260/hr |
| Full-Stack Engineer | $65–85/hr | $95–130/hr | $140–185/hr | $185–250/hr |
| Mobile Engineer (iOS/Android) | $70–90/hr | $100–140/hr | $150–200/hr | $200–270/hr |
| DevOps / Platform Engineer | $70–95/hr | $110–150/hr | $155–210/hr | $210–280/hr |
| Data Engineer | $70–90/hr | $105–145/hr | $150–200/hr | $200–270/hr |
| ML / AI Engineer | $80–100/hr | $120–165/hr | $170–230/hr | $230–320/hr |
| Security Engineer | $80–100/hr | $115–155/hr | $160–220/hr | $220–300/hr |
| QA / Test Engineer | $50–70/hr | $75–110/hr | $115–155/hr | $155–200/hr |

**Product, design, and operations roles:**

| Role | Junior (0–2 yrs) | Mid (3–6 yrs) | Senior (7–12 yrs) | Director / VP (12+ yrs) |
|------|-----------------|---------------|-------------------|--------------------------|
| Product Manager (PM) | $55–75/hr | $85–125/hr | $130–175/hr | $175–250/hr |
| Technical Product Manager (TPM) | $65–85/hr | $100–140/hr | $145–195/hr | $195–270/hr |
| UX / Product Designer | $55–75/hr | $85–120/hr | $125–170/hr | $170–230/hr |
| UX Researcher | $50–70/hr | $80–115/hr | $120–160/hr | $160–220/hr |
| Engineering Manager (EM) | $80–100/hr | $115–155/hr | $160–215/hr | $215–300/hr |
| Technical Writer | $45–65/hr | $70–100/hr | $105–145/hr | $145–190/hr |
| Scrum Master / Agile Coach | $55–75/hr | $80–115/hr | $120–155/hr | $155–200/hr |

**Default for generic estimates**: Use $130/hr (mid-senior full-stack) unless the tech stack clearly requires specialists. For PM overhead, use $110/hr (mid-senior PM) unless otherwise specified.

---

## Western Europe Rates

UK, Germany, Netherlands, France, Nordics. Rates in USD equivalent.

| Role | Mid (3–6 yrs) | Senior (7–12 yrs) |
|------|---------------|-------------------|
| Full-Stack Engineer | $70–100/hr | $100–140/hr |
| Backend / Frontend | $65–95/hr | $95–130/hr |
| DevOps / Platform | $75–105/hr | $105–145/hr |
| ML / AI Engineer | $85–120/hr | $120–165/hr |
| Product Manager | $65–95/hr | $95–135/hr |
| UX / Product Designer | $60–90/hr | $90–125/hr |

---

## Eastern Europe / Latam Rates

Poland, Romania, Ukraine, Argentina, Brazil, Mexico. USD equivalent.

| Role | Mid (3–6 yrs) | Senior (7–12 yrs) |
|------|---------------|-------------------|
| Full-Stack Engineer | $35–55/hr | $55–80/hr |
| Backend / Frontend | $30–50/hr | $50–75/hr |
| DevOps / Platform | $35–60/hr | $60–85/hr |
| ML / AI Engineer | $45–70/hr | $70–100/hr |
| Product Manager | $30–50/hr | $50–75/hr |
| UX / Product Designer | $28–45/hr | $45–70/hr |

---

## South/Southeast Asia Rates

India, Vietnam, Philippines, Indonesia. USD equivalent.

| Role | Mid (3–6 yrs) | Senior (7–12 yrs) |
|------|---------------|-------------------|
| Full-Stack Engineer | $20–35/hr | $35–55/hr |
| Backend / Frontend | $18–30/hr | $30–50/hr |
| DevOps / Platform | $22–38/hr | $38–60/hr |
| ML / AI Engineer | $28–45/hr | $45–70/hr |
| Product Manager | $18–30/hr | $30–48/hr |
| UX / Product Designer | $16–28/hr | $28–45/hr |

---

## Product Manager Effort Estimation

When estimating a **product run by a human team** (not just the codebase), PM effort is a real and significant cost that must be separately estimated. PMs don't appear in the repo, but their work is implied by it — every feature, API endpoint, and design decision was once a spec, a Jira ticket, a design review, or a stakeholder conversation.

**How to estimate PM hours from repo signals:**

Read `references/pm-effort-guide.md` for the full methodology. At a high level:

- Count the number of distinct product features or user-facing capabilities
- Identify evidence of planning artifacts (changelogs, ADRs, spec directories, versioned APIs)
- Assess product complexity: is this a single-user tool or a multi-stakeholder platform?
- Apply PM-to-engineering ratios typical for this type of product

**Typical PM-to-engineer ratios by product type:**

| Product Type | PM Hours as % of Engineering Hours |
|-------------|-------------------------------------|
| Internal tool / admin panel | 5–10% |
| Developer tool / API / SDK | 10–15% |
| B2B SaaS product | 15–25% |
| B2C consumer product | 20–30% |
| Multi-sided marketplace | 25–35% |
| Enterprise platform (complex stakeholders) | 30–40% |

These ratios reflect PM involvement in discovery, spec writing, prioritization, stakeholder management, and acceptance testing — not engineering management (which is counted separately under Engineering Manager).

---

## Agency / Consulting Rates

If the user asks what an agency or consulting firm would charge:

| Agency Type | Typical Rate Multiplier |
|-------------|------------------------|
| Boutique dev shop (US) | 2.0–2.5× individual contractor rates |
| Big 4 / Tier 1 consulting | 3.0–5.0× individual contractor rates |
| Offshore agency (India, etc.) | 1.5–2.0× individual offshore rates |

Note: Agency rates include overhead, project management, account management, and profit margin. The actual developer hours are the same — the cost is just higher.

---

## Typical Seniority Mix for Different Project Types

If estimating for a team (not a solo developer), use these default mixes unless the repo suggests otherwise:

**Startup / MVP** (2–4 person team):
- 1× Senior full-stack (lead): 60% of hours
- 1× Mid full-stack: 40% of hours
- Blended rate: ~$140/hr (US)

**Established product team** (4–8 engineers):
- 1× Staff/Senior lead: 20% of hours
- 2× Senior engineers: 40% of hours  
- 2× Mid engineers: 40% of hours
- Blended rate: ~$155/hr (US)

**Enterprise / agency build** (8+ engineers):
- 1× Principal/Architect: 10% of hours
- 3× Senior engineers: 40% of hours
- 4× Mid engineers: 40% of hours
- 1× Junior (supervised): 10% of hours
- Blended rate: ~$145/hr (US)

---

## Working Hours Assumptions

When converting hours to calendar time:

- A developer works approximately **6 productive coding hours per day** (accounting for meetings, code review, Slack, etc.)
- A work week is **5 days = ~30 productive hours**
- A work month is **~130 productive hours** (4.33 weeks)
- A person-year is **~1,560 productive hours**

So:
- 500 hours ÷ 30 hr/week = ~17 weeks ≈ 4 months for 1 developer
- 500 hours ÷ 3 developers = ~167 hours each ÷ 30 hr/week ≈ 5–6 weeks calendar time

Always present both **total hours** and **calendar time** (for a realistic team) in the report, since they're equally useful to different audiences.

---

## Interpreting the Estimate for Common Use Cases

**Acquisition due diligence**: Use the "Mid" scenario cost as the replacement value. Note that the original team's cost was almost certainly different (lower if they were efficient, higher if there was churn and rewriting).

**Freelancer pricing a rewrite**: Start with the "Mid" estimate and adjust for your own rate. Be honest about what you can and can't estimate from a static repo analysis.

**Evaluating a job offer / joining a project**: The total hours are more useful than cost. Compare to how many person-years the original team put in (if you know team size and tenure).

**Scoping a migration**: This estimate covers recreating from scratch — a migration may be cheaper (if the codebase is the target) or more expensive (if you're translating between platforms/languages and maintaining both simultaneously).
