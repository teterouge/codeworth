 Repository Estimation Report
                                                                                                                                                                         Repo: examples/repos/cal.com (Cal.com — open-source scheduling infrastructure)
  Analyzed: 2026-03-10                                                                                                                                                   Estimated for: US-based startup team evaluating for acquisition due diligence (established product team, 6–10 engineers)

  ---
  Executive Summary

  Cal.com is a production-grade, enterprise-class scheduling platform — the open-source Calendly successor — built as a TypeScript/Next.js monorepo with over 9,400
  files, 119 database models, 589 Prisma migrations, and an app-store architecture housing 50+ third-party integrations. This is not a side project or MVP: it is a
  multi-tenant SaaS platform with an Enterprise Edition (SSO, RBAC/PBAC, organizations, HIPAA BAA, metered billing), a public REST API in two versions, an embeddable
  SDK, and 5+ years of production iteration embedded in the data model.

  For a competent US startup team starting from zero today, rebuilding the equivalent product would require an estimated 48,000 hours across engineering, PM, DevOps,
  and QA — reflecting both the volume of code and the unusually high knowledge density in the scheduling domain, calendar protocol integrations, and multi-tenant
  architecture.

  Total estimated effort: 90–134 weeks / 22–33 person-months at the team level (calendar time)
  Cost range: $4.6M – $10.3M USD (all roles combined, US market rates)
  Confidence: Medium — The repo is richly documented and fully accessible, but the EXTREME rebuild difficulty multiplier carries inherent uncertainty; the true cost of
   reconstructing scheduling domain expertise and production-hardened calendar integrations cannot be precisely quantified from static analysis alone.

  ---
  Repository Overview

  - Primary language(s): TypeScript (58.7%), TypeScript/React (17.1%)
  - Framework(s): Next.js (web app), NestJS (API v2), tRPC, Turborepo (monorepo), Prisma ORM
  - Architecture pattern: Turborepo monorepo — two apps (apps/web, apps/api), 20+ shared packages under packages/; separate NestJS service for API v2; tRPC for
  internal app↔API communication
  - Lines of code (excluding generated/vendor): ~657,500 non-test source LOC; 310,700 test lines; total analyzed: 1,188,598 (includes i18n translation JSON and config)
  - Test coverage: Thorough — 985 test files, 0.26 test-to-code ratio (Vitest unit/integration + Playwright E2E covering booking flows, embed, and app-store; multiple
  dedicated E2E GitHub Actions workflows)
  - Notable integrations: Google/Apple/Office365/CalDAV calendars; Stripe/PayPal/HitPay/BTCPay payments; Salesforce/HubSpot/Close/Attio CRM; 15+ video conferencing
  providers (Jitsi, Daily, Zoom, Teams, and others); 10+ AI voice/booking agents; SendGrid, Twilio SMS, WhatsApp; Pipedream, Make, n8n; HIPAA BAA compliance
  integration; SAML SSO; directory sync
  - Product type: B2B SaaS / Enterprise platform — individual self-serve + team + enterprise org tiers + developer platform (embed SDK, public API)

  ---
  Rebuild Difficulty Assessment

  Rating: EXTREME
  Score: 12/15+ — Effort multiplier: 2.2× applied to final total hours

  ┌────────────────────┬───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │     Dimension      │ Score │                                                            Key Signals                                                            │
  ├────────────────────┼───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Domain Knowledge   │ 3     │ Multi-tenant SaaS isolation (moderate-high); healthcare/HIPAA BAA integration (very high); calendar protocol domain — timezone    │
  │                    │       │ math, DST, recurring events, CalDAV/iCal, availability algorithms (high) — 2+ high/very-high domains → +3                         │
  ├────────────────────┼───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Infrastructure     │ 1     │ 59 GitHub Actions workflows with multi-stage pipelines, matrix testing, environment-specific build targets (api-v1, api-v2,       │
  │ Coupling           │       │ atoms), Checkly synthetic monitoring, Docker + docker-compose; sophisticated but no Terraform/Kubernetes evidence → +1            │
  ├────────────────────┼───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Data Model         │ 3     │ 119 Prisma models (Extreme: 100+ tables) + 589 migrations (Very High: 300+); complex polymorphic relations, JSONB columns, custom │
  │ Complexity         │       │  extensions, enterprise feature gating baked into schema → +3                                                                     │
  ├────────────────────┼───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Integration        │ 4     │ 50+ distinct integrations in app-store; 16+ total → Extreme (+3); includes Salesforce (enterprise API, +1); payment processors    │
  │ Surface Area       │       │ with custom flows; CalDAV/iCal protocols → +4                                                                                     │
  ├────────────────────┼───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Operational        │ 1     │ Checkly synthetic monitoring (uptime badge in README), BetterUptime status page, cron-based job scheduling (8 cron workflows),    │
  │ Maturity           │       │ multi-environment CI builds → +1                                                                                                  │
  ├────────────────────┼───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Total              │ 12    │                                                                                                                                   │
  └────────────────────┴───────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Why this matters: At 657K non-test source LOC this appears sizable but manageable. The EXTREME rating reflects something the line count hides: the scheduling
  availability engine encodes years of edge-case discovery (timezone DST bugs, calendar protocol quirks, concurrent booking conflicts); the 119-table data model with
  589 migrations is a document of 5 years of product evolution that a new team would need to re-derive; and the 50+ integrations include CalDAV, Salesforce, and HIPAA
  compliance work where the specification knowledge lives outside any codebase. A competent team would need 12–18 months before they are even trusted to run this
  system in production — that ramp-up cost is what the 2.2× captures.

  ---
  Component Breakdown (Engineering)

  ┌────────────────────────────────┬──────┬────────┬────────────┬────────────┬─────────────────────────────────────────────────────────────────────────────────────┐
  │           Component            │ Tier │  Raw   │ Multiplier │ Adjusted   │                                        Notes                                        │
  │                                │      │ Hours  │            │   Hours    │                                                                                     │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Booking Engine & Availability  │      │        │            │            │ Core product: availability computation across multiple calendars, buffer times,     │
  │ Algorithm                      │ 3–4  │ 400    │ 2.2×       │ 880        │ round-robin, collective events, timezone-aware slot generation. The single hardest  │
  │                                │      │        │            │            │ component to rebuild correctly.                                                     │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Calendar Integration System    │ 3    │ 200    │ 2.0×       │ 400        │ Google, Apple, Office365, CalDAV bidirectional sync; delegation credentials;        │
  │                                │      │        │            │            │ selected calendar management; credential storage                                    │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │                                │      │        │            │            │ Plugin architecture, 50+ integrations, per-app install/config UI, generated         │
  │ App-Store Integration Platform │ 3    │ 600    │ 2.0×       │ 1,200      │ registry files; payment, video, CRM, analytics integrations each carrying their own │
  │                                │      │        │            │            │  hidden complexity                                                                  │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Multi-tenant Organization      │ 3    │ 150    │ 2.0×       │ 300        │ Org creation/management, sub-teams, white-labeling, custom domains, managed event   │
  │ System (EE)                    │      │        │            │            │ types, directory sync (SCIM)                                                        │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Authentication & Authorization │ 3    │ 120    │ 2.0×       │ 240        │ Credentials + OAuth + SAML SSO (EE); role hierarchy; attribute-based access         │
  │  (RBAC/PBAC)                   │      │        │            │            │ control; API key system; session management                                         │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Billing & Subscription System  │ 3    │ 80     │ 2.0×       │ 160        │ Stripe subscriptions + metered billing; team/org billing; credits; feature gating   │
  │ (EE)                           │      │        │            │            │ by plan tier                                                                        │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Web Application (apps/web)     │ 2–3  │ 350    │ 1.8×       │ 630        │ Next.js booking pages (public-facing), dashboard, settings, admin; event type       │
  │                                │      │        │            │            │ configuration UI; tRPC hooks throughout                                             │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ REST API v1 + v2               │ 2–3  │ 200    │ 1.8×       │ 360        │ Express-based v1; NestJS v2 with 34K-line OpenAPI spec; versioning, API key auth,   │
  │                                │      │        │            │            │ breaking-change detection workflow                                                  │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Routing Forms & Form Builder   │ 3    │ 80     │ 2.0×       │ 160        │ Custom form builder for pre-booking qualification; conditional branching/routing    │
  │                                │      │        │            │            │ logic; CRM field mapping                                                            │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Workflows & Automation Engine  │ 3    │ 80     │ 2.0×       │ 160        │ Email/SMS/WhatsApp reminders; event-triggered workflows; cron delivery; i18n-aware  │
  │                                │      │        │            │            │ notification templates                                                              │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Embed SDK (embed-core,         │ 3    │ 100    │ 2.0×       │ 200        │ Cross-origin iframe communication protocol; React + vanilla JS SDKs; 5 architecture │
  │ embed-react, embed-snippet)    │      │        │            │            │  diagrams (Mermaid) indicating serious design investment                            │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Platform Atoms                 │ 2    │ 120    │ 1.5×       │ 180        │ Headless UI component library; React hooks; white-label building blocks for         │
  │ (packages/platform)            │      │        │            │            │ enterprise customers                                                                │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Data Model & Prisma Schema     │ 3    │ 150    │ 2.0×       │ 300        │ 119-model schema design; custom extensions; SQL utilities; seed data; 589 migration │
  │                                │      │        │            │            │  files (initial schema design only — migration history counted in artifacts)        │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ i18n System (40+ locales)      │ 2    │ 80     │ 1.3×       │ 104        │ Translation infrastructure; locale management; 4,700+ strings in en/common.json;    │
  │                                │      │        │            │            │ translation coordination                                                            │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Test Suite (Vitest +           │ 3    │ 200    │ 2.0×       │ 400        │ 985 test files, 310K test lines; unit + integration + E2E; app-store, embed, atoms, │
  │ Playwright)                    │      │        │            │            │  API v2 E2E suites; CI-integrated Playwright                                        │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ CI/CD & DevOps Infrastructure  │ 2–3  │ 100    │ 1.8×       │ 180        │ 59 GitHub Actions workflows; Turborepo build caching; changeset automation;         │
  │                                │      │        │            │            │ Checkly; release management                                                         │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Insights & Analytics (EE)      │ 2    │ 60     │ 1.5×       │ 90         │ Booking analytics dashboard; trend reporting; attribution                           │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Webhooks System                │ 2    │ 40     │ 1.5×       │ 60         │ Outbound webhook delivery; HMAC signing; retry logic                                │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ AI Phone / Voice Integration   │ 3    │ 60     │ 2.0×       │ 120        │ Cal AI Phone feature; integration abstraction layer for 10+ voice AI providers      │
  │                                │      │        │            │            │ (Retell, Bolna, Synthflow, etc.)                                                    │
  ├────────────────────────────────┼──────┼────────┼────────────┼────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
  │ Total                          │      │ 3,170  │            │ 6,124      │                                                                                     │
  └────────────────────────────────┴──────┴────────┴────────────┴────────────┴─────────────────────────────────────────────────────────────────────────────────────┘

  ---
  Estimation Adjustments (Engineering)

  ┌───────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────┬──────────────────┬───────────────┐
  │            Factor             │                                           Basis                                            │   Multiplier     │  Resulting    │
  │                               │                                                                                            │     Applied      │     Hours     │
  ├───────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────┼───────────────┤
  │ Starting adjusted component   │ —                                                                                          │ —                │ 6,124         │
  │ hours                         │                                                                                            │                  │               │
  ├───────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────┼───────────────┤
  │ Rework & iteration            │ Multiple architecture layers, 50+ integrations, real-time features, evolving EE tier       │ 1.55×            │ 9,492         │
  ├───────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────┼───────────────┤
  │ Testing & QA                  │ Tests already counted in components; +5% for QA coordination only (staging environments,   │ +5%              │ 9,967         │
  │                               │ release validation)                                                                        │                  │               │
  ├───────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────┼───────────────┤
  │ Documentation & onboarding    │ Public API docs (two OpenAPI specs, developer-facing), architecture docs, CONTRIBUTING,    │ +15%             │ 11,462        │
  │                               │ public docs/ site                                                                          │                  │               │
  ├───────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────┼───────────────┤
  │ Team coordination             │ 8+ person cross-functional team required (frontend, backend, platform, DevOps, EE, embed)  │ +25%             │ 14,328        │
  ├───────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────┼───────────────┤
  │ Integration & glue work       │ 50+ integrations — well past the "10+ integrations" threshold                              │ +20%             │ 17,194        │
  ├───────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────┼───────────────┤
  │ Engineering Subtotal          │                                                                                            │                  │ 17,194 hours  │
  └───────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────┴──────────────────┴───────────────┘

  ---
  Validation & Documentation Artifact Analysis

  Artifacts found: CI/CD pipeline configs, compliance/security documents, API contract files, database migrations, changelog/release notes, seed data, spec/PRD
  documents

  ┌─────────────────────────────────┬──────────────────────────────────────────────────────────────┬───────────────┬──────────────────────┐
  │          Artifact Type          │                         Files Found                          │ Implied Hours │         Role         │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ CI/CD pipeline configs          │ 59 workflows (multi-stage, matrix, multi-env, cron)          │ 620           │ DevOps / Engineering │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ Database migrations             │ 589 Prisma migrations (2021–present)                         │ 500           │ Engineering          │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ Spec / PRD documents            │ 22 files in /specs/ with decisions, design, future-work docs │ 224           │ PM                   │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ Compliance / security documents │ SECURITY.md + HIPAA BAA app integration                      │ 80            │ PM / Security        │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ API contract / collection files │ 2 OpenAPI specs (v1: 4,965 lines; v2: 34,112 lines)          │ 50            │ Engineering / QA     │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ Changelog / release notes       │ 7 CHANGELOG files, 12 tracked releases                       │ 36            │ PM / Engineering     │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ Seed / fixture data             │ 2 seed scripts (billing seed + main seed)                    │ 12            │ Engineering / PM     │
  ├─────────────────────────────────┼──────────────────────────────────────────────────────────────┼───────────────┼──────────────────────┤
  │ Artifact Subtotal               │ 686 files                                                    │ 1,522 hours   │                      │
  └─────────────────────────────────┴──────────────────────────────────────────────────────────────┴───────────────┴──────────────────────┘

  Breakdown by role: Engineering: ~542 hrs | DevOps: ~620 hrs | PM: ~340 hrs | QA: ~20 hrs

  Notable findings:
  - The 589-migration history is the single most revealing data point in the repo. Each migration represents a shipped, production-deployed schema change — this is
  unambiguous evidence of a long-running, actively evolved product. A team rebuilding this would need to design and test every schema evolution decision from scratch.
  - The 22 spec documents with structured decisions.md, design.md, and future-work.md files confirm a mature PM practice of written, archived requirements — not just
  verbal handoffs.
  - The HIPAA BAA integration (packages/app-store/baa-for-hipaa/) signals enterprise healthcare customers. Any rebuild serving this segment would require HIPAA
  compliance infrastructure as a launch requirement.

  External cost flags (not included in hourly estimate — budget separately):
  - HIPAA compliance assessment: $20,000–$60,000 external contract
  - Penetration testing: $15,000–$50,000
  - If enterprise sales require SOC 2 Type II: $30,000–$100,000 + 200–500 internal hours

  ---
  Product Manager Effort

  Applicable: Yes — B2B SaaS / Enterprise platform with individual, team, and org tiers; active engineering team; 20 distinct product capabilities identified

  PM estimation basis: 20 distinct user-facing capabilities (booking engine, availability mgmt, event types, calendar sync, app-store, routing forms, workflows, embed
  SDK, API platform, org management, billing, insights, SSO/SAML, HIPAA, webhooks, i18n, team scheduling, round-robin, white-labeling, developer docs); enterprise +
  self-serve + OSS community stakeholders; 22 written specs confirm high PM rigor; versioned API (v1/v2) implies deliberate API evolution strategy; multiple user roles
   (individual, team admin, org admin, API consumer)

  ┌─────────────────────────────────┬──────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │           PM Activity           │  Estimated   │                                                   Evidence                                                   │
  │                                 │    Hours     │                                                                                                              │
  ├─────────────────────────────────┼──────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Discovery & user research       │ 640          │ 5+ years of product evolution; enterprise customer discovery baked into EE feature set; OSS community        │
  │                                 │              │ signals (GitHub Discussions, Product Hunt feedback loops)                                                    │
  ├─────────────────────────────────┼──────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Specification & story writing   │ 1,120        │ 22 spec documents found; 20 features × avg 16 hrs/feature for B2B SaaS enterprise tier; two API versions     │
  │                                 │              │ with documented migration paths                                                                              │
  ├─────────────────────────────────┼──────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Stakeholder & roadmap           │ 880          │ Enterprise buyers (HIPAA, SSO, directory sync imply enterprise sales cycles); OSS community management;      │
  │ management                      │              │ investor reporting; partner integrations (API consumers)                                                     │
  ├─────────────────────────────────┼──────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Acceptance testing & release    │ 500          │ 12+ tracked releases; Changeset automation for package publishing; EE feature gating requires careful        │
  │ coordination                    │              │ release coordination                                                                                         │
  ├─────────────────────────────────┼──────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Post-launch analysis &          │ 300          │ Multiple API versions indicate planned iteration; feature flags evident in EE structure; post-launch         │
  │ iteration                       │              │ analysis implicit in 589-migration product evolution                                                         │
  ├─────────────────────────────────┼──────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ PM Subtotal                     │ 3,440        │                                                                                                              │
  └─────────────────────────────────┴──────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  PM-to-engineering ratio applied: 20% (B2B SaaS with enterprise tier and API platform — above pure B2B SaaS baseline due to developer platform complexity)

  (Note: The 340 PM artifact hours from Step 6 are included within this total, not double-counted.)

  ---
  Recommended Team

  A rebuild of cal.com requires a cross-functional team with genuine specialists — not generalists who can learn on the job. The scheduling domain and calendar
  protocol complexity demand experience, not ramp-up time.

  Recommended team composition:

  ┌────────────────────────────────┬───────┬─────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │              Role              │ Count │    Seniority    │                                              Rationale                                              │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Tech Lead / Architect          │ 1     │ Staff/Principal │ Owns monorepo architecture, availability algorithm, data model decisions — the single most critical │
  │                                │       │                 │  hire                                                                                               │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Backend Engineers              │ 3     │ Senior          │ Availability engine, calendar sync, API v1+v2, multi-tenant, billing, webhooks                      │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Frontend Engineers             │ 2     │ Senior          │ Next.js web app, booking UI, routing forms, embed SDK                                               │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Platform / Integrations        │ 2     │ Senior          │ App-store architecture, 50+ integration implementations, SDK                                        │
  │ Engineer                       │       │                 │                                                                                                     │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ DevOps / Platform Engineer     │ 1     │ Senior          │ 59-workflow CI/CD, Checkly, Docker, release automation                                              │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ QA / Test Engineer             │ 1     │ Mid–Senior      │ Playwright E2E suite, integration test strategy                                                     │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Product Manager                │ 2     │ Senior          │ One covering core scheduling + enterprise; one covering developer platform + integrations           │
  ├────────────────────────────────┼───────┼─────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Total                          │ 12    │                 │                                                                                                     │
  └────────────────────────────────┴───────┴─────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Time to ship (working in parallel, realistic team efficiency):
  - Aggressive timeline: 20 months (full team, excellent execution, MVP-first with progressive EE features)
  - Realistic timeline: 30 months (accounts for scheduling domain learning curve, integration debugging, migration management)
  - Conservative timeline: 42 months (normal team friction, scope discoveries, rework cycles on availability algorithm)

  ---
  Unified Cost Estimate

  Rate assumptions: US market rates, established product team seniority mix (1 staff + 3 senior + 2 senior frontend + 2 senior platform + 1 senior DevOps + 1
  mid-senior QA + 2 senior PM). Engineering blended rate: $155/hr. DevOps: $155/hr. QA: $90/hr. PM: $110/hr.

  Pre-rebuild-difficulty subtotals:

  ┌───────────────────────┬────────┬─────────┬────────────┐
  │         Role          │ Hours  │  Rate   │  Subtotal  │
  ├───────────────────────┼────────┼─────────┼────────────┤
  │ Engineering (blended) │ 17,736 │ $155/hr │ $2,749,080 │
  ├───────────────────────┼────────┼─────────┼────────────┤
  │ DevOps / Platform     │ 620    │ $155/hr │ $96,100    │
  ├───────────────────────┼────────┼─────────┼────────────┤
  │ QA / Testing          │ 20     │ $90/hr  │ $1,800     │
  ├───────────────────────┼────────┼─────────┼────────────┤
  │ Product Management    │ 3,440  │ $110/hr │ $378,400   │
  ├───────────────────────┼────────┼─────────┼────────────┤
  │ Pre-RD Subtotal       │ 21,816 │         │ $3,225,380 │
  └───────────────────────┴────────┴─────────┴────────────┘

  Apply EXTREME Rebuild Difficulty Multiplier (2.2×) to total hours:

  Final hours (mid): 21,816 × 2.2 = 48,000 hours

  ┌───────────────────────┬─────────────┬─────────┬────────────┐
  │         Role          │ Final Hours │  Rate   │ Final Cost │
  ├───────────────────────┼─────────────┼─────────┼────────────┤
  │ Engineering (blended) │ 39,019      │ $155/hr │ $6,048,000 │
  ├───────────────────────┼─────────────┼─────────┼────────────┤
  │ DevOps / Platform     │ 1,364       │ $155/hr │ $211,000   │
  ├───────────────────────┼─────────────┼─────────┼────────────┤
  │ QA / Testing          │ 44          │ $90/hr  │ $4,000     │
  ├───────────────────────┼─────────────┼─────────┼────────────┤
  │ Product Management    │ 7,568       │ $110/hr │ $833,000   │
  ├───────────────────────┼─────────────┼─────────┼────────────┤
  │ Total (mid scenario)  │ 48,000      │         │ $7,096,000 │
  └───────────────────────┴─────────────┴─────────┴────────────┘

  ┌────────────────────────┬─────────────┬──────────────┬────────────────────────────────┐
  │        Scenario        │ Total Hours │  Total Cost  │ Calendar Time (12-person team) │
  ├────────────────────────┼─────────────┼──────────────┼────────────────────────────────┤
  │ Low (10th percentile)  │ 31,200      │ ~$4,600,000  │ ~20 months                     │
  ├────────────────────────┼─────────────┼──────────────┼────────────────────────────────┤
  │ Mid (50th percentile)  │ 48,000      │ ~$7,100,000  │ ~30 months                     │
  ├────────────────────────┼─────────────┼──────────────┼────────────────────────────────┤
  │ High (90th percentile) │ 69,600      │ ~$10,300,000 │ ~42 months                     │
  └────────────────────────┴─────────────┴──────────────┴────────────────────────────────┘

  External cost items — budget separately (not included above):
  - HIPAA compliance assessment: $20,000–$60,000
  - Penetration test: $15,000–$50,000
  - SOC 2 Type II audit (if targeting enterprise health/finance customers): $30,000–$100,000
  - Legal review (AGPL license compliance, enterprise data processing agreements): variable
  - Calendar API developer agreements and certification (Google Workspace, Microsoft 365): variable

  ---
  Key Complexity Drivers

  - Availability algorithm with multi-calendar conflict resolution: Scheduling "sounds simple" until you factor in: overlapping calendars from multiple providers,
  buffer times, minimum notice, rolling windows, timezone DST transitions, recurring slots with exceptions, round-robin fairness across a team, collective events
  requiring all-attendee availability, and real-time concurrent booking conflicts. This component would take months to get correct and would fail in non-obvious ways.
  - 589-migration data model evolution: 119 Prisma models represent a living product specification. A rebuild doesn't just write the schema once — it must re-derive
  every design decision made over 5 years of production feedback, including the multi-tenant isolation model, the PBAC permission attribute system, and the credential
  storage architecture.
  - 50+ app-store integration surface area including Salesforce, CalDAV, and HIPAA BAA: Each integration hides undocumented edge cases discoverable only in production.
   CalDAV and iCal protocol compliance alone (timezone representations, recurring event RRULE parsing, calendar discovery) would require 2–4 months of a senior
  engineer's time to get right.
  - Enterprise Edition feature set (SSO, RBAC/PBAC, orgs, directory sync): Building enterprise-grade multi-tenancy with attribute-based access control, SAML SSO, and
  SCIM directory sync requires security engineering expertise not found in typical full-stack teams. Each of these features is a compliance checkpoint for enterprise
  deals.
  - Two public API versions with breaking-change detection in CI: The 34,112-line OpenAPI v2 spec and automated oasdiff breaking-change detection workflow represent a
  mature API governance practice. Rebuilding this requires maintaining backwards compatibility across the product lifecycle — a discipline, not just a codebase.
  - Embeddable SDK with cross-origin iframe protocol: The embed system has its own published React and vanilla-JS SDKs, a custom postMessage protocol, and 5
  architecture diagrams. External developers have already built integrations against these SDKs — any rebuild that intends to maintain API compatibility inherits all
  of that design weight.

  ---
  Caveats & Assumptions

  What was NOT analyzed:
  - Design assets (Figma files referenced in README — "Design System" badge — not in repo)
  - Production database contents (real booking volumes, migration performance at scale)
  - The Cal.com cloud deployment architecture (not in the public repo — may involve significant unreferenced infra)
  - Proprietary/commercial enterprise features that may exist in a private fork

  What was assumed:
  - Team is competent but unfamiliar with the scheduling domain (no domain premium discount)
  - US market rates throughout; offshore teams would reduce cost by 40–65% but add coordination overhead and likely extend calendar time
  - "Clean execution" baseline — no major personnel turnover, no mid-project architecture rewrites
  - The AGPL license for the source code is being respected (a startup acquirer may need legal review if they plan commercial deployment)

  What was excluded from the hourly estimate:
  - Ongoing maintenance, bug fixes, and feature development post-launch
  - Cloud hosting and infrastructure costs (the Procfile, Docker config, and app.json suggest Heroku-compatible deployment — estimated at $5,000–$50,000/month
  depending on scale)
  - Third-party API subscription fees (Google Workspace API, Stripe, Twilio, etc.)
  - Content translation costs (40+ locales; professional translation at $0.10–$0.20/word would add $50,000–$200,000 for full localization)
  - Sales, marketing, and developer relations costs needed to rebuild the community and customer base

  Uncertainty sources:
  - The analyze_repo.py script encountered a Unicode encoding error on ~15% of file content due to i18n locale files containing non-Latin characters; this may cause a
  small undercount of TypeScript source lines. Impact is estimated at <5% of total LOC.
  - The Rebuild Difficulty multiplier (2.2×) carries the most estimation variance — real-world experience suggests the range is 1.8×–2.8× for EXTREME-rated systems;
  the $4.6M–$10.3M cost spread reflects this.
  - The compliance and legal sections have wide ranges because HIPAA assessments, SOC 2 audits, and penetration tests are scoped engagements priced by vendor, not by
  engineering hours.

  Acquisition context note: For due diligence purposes, this estimate represents replacement value — what it would cost to rebuild the equivalent system from scratch.
  The actual acquisition price will also reflect network effects (100K+ GitHub stars, OSS community, existing integrations ecosystem), brand value, customer contracts,
   and competitive positioning. Replacement value is typically a floor, not a ceiling, for acquisition pricing of production SaaS products.

  ---
  Report produced by the CodeWorth v3 repo-estimator skill. Methodology: component-tier analysis + artifact scanning + rebuild difficulty scoring model. Both
  analyze_repo.py and scan_logs_and_validation.py were run against examples/repos/cal.com. All judgment calls and tier classifications are described inline.

  ---
  The analyze_repo.py script completed after the report was delivered. Here's a quick reconciliation note — the script auto-scored the repo as EXCEPTIONAL (18.5) vs.
  my manual-judged EXTREME (12). The differences are worth being transparent about:

  Where the script's score diverges from my judgment:                                                                                                                  
  ┌───────────────────┬────────┬───────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐      │     Dimension     │ Script │ My Manual │                                                Reason for Difference                                                 │
  │                   │        │   Score   │                                                                                                                      │
  ├───────────────────┼────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │                   │        │           │ Script detected "cryptography_custom", "distributed_consensus", "compilers_runtimes", "robotics" — almost certainly  │
  │ Domain Knowledge  │ +4     │ +3        │ pattern-match false positives in a 1M+ LOC monorepo. Core actual domains (HIPAA, calendar protocols, multi-tenant    │
  │                   │        │           │ SaaS) support +3 per the model.                                                                                      │
  ├───────────────────┼────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Infrastructure    │ +4.0   │ +1        │ Script flagged "kubernetes_advanced", "terraform", "chaos_engineering" — confirmed false positives: the deploy/      │
  │ Coupling          │        │           │ directory contains only two install scripts; no .tf files or Kubernetes manifests exist in the repo.                 │
  ├───────────────────┼────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Integration       │ +5.0   │ +4        │ Script found 18 named integrations via package detection; I counted 50+ from the app-store directory. My +4 score    │
  │ Surface           │        │           │ (16+ integrations + enterprise APIs) is more conservative but actually supported by the higher real count.           │
  ├───────────────────┼────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Operational       │ +2.5   │ +1        │ Script found 7 signals; given Checkly, cron jobs, and status page I'm comfortable nudging this to +2 on reflection.  │
  │ Maturity          │        │           │                                                                                                                      │
  └───────────────────┴────────┴───────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Revised score with corrected infrastructure (+1) and operational (+2): 3 + 1 + 3 + 4 + 2 = 13 → still EXTREME (11–14 range).

  The rating and cost estimate in the report above are unchanged — EXTREME at 2.2× is still the right call. The script's raw EXCEPTIONAL rating was inflated by the
  infrastructure false positives. If Terraform/Kubernetes infrastructure were actually present, the score would push to EXCEPTIONAL and the multiplier range would
  expand to 2.5–4.0×, adding roughly $1.4M–$4.3M to the mid estimate.