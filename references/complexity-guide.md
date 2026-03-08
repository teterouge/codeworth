# Complexity Guide

This document defines the four-tier complexity taxonomy and associated multipliers used by the repo-estimator skill.

---

## Tier Definitions

### Tier 1 — Boilerplate (multiplier: 1.0×)

Work a developer largely delegates to scaffolding tools, templates, or copy-paste from documentation. Minimal judgment required. Could be reproduced by a junior developer in a short time.

**Examples:**
- Project scaffolding (create-react-app output, Rails generators, etc.)
- Config files (`.eslintrc`, `tsconfig.json`, `babel.config.js`, standard CI YAML)
- Protobuf / GraphQL / Prisma generated output (generated files only — the schema itself is higher tier)
- Standard CRUD endpoints with no custom logic (GET/POST/PUT/DELETE on a model with basic validation)
- Simple landing pages or marketing pages with no interactivity
- Boilerplate README, CONTRIBUTING, CHANGELOG files
- Package.json / requirements.txt / go.mod dependency declarations
- Standard Docker/docker-compose setup for common stacks
- `.env.example` files, standard environment configuration
- Database migrations that are purely additive (add column, add table)

**Rule of thumb**: If you could find a 1:1 tutorial for it, it's probably Tier 1.

---

### Tier 2 — Moderate (multiplier: 1.3–1.5×)

Work requiring real judgment and domain knowledge, but following well-established patterns. A mid-level developer with some experience in the relevant tech would recognize the approach immediately.

**Examples:**
- Standard session-based or JWT authentication (login, logout, token refresh, password reset)
- OAuth2 integration with a major provider (Google, GitHub, etc.) — standard flows only
- REST or GraphQL API with custom business logic (not just CRUD)
- Email notification system (templates, transactional sends via SendGrid/Postmark/etc.)
- Standard payment integration (Stripe Checkout, one payment method, no custom flows)
- Paginated data tables with filtering and sorting
- File upload with validation (S3, CloudFront, standard patterns)
- Standard admin dashboard (CRUD interface for internal users)
- Background job processing with a standard queue (Sidekiq, Celery, BullMQ, etc.)
- Webhook receiver with basic validation and dispatch
- Standard search implementation (Elasticsearch basic queries, PostgreSQL full-text search)
- Multi-language i18n with a standard library
- Standard mobile app screens with navigation and API calls
- Unit test suites for business logic
- Role-based access control with 2–5 roles, no dynamic permissions

**Rule of thumb**: If there's a well-known library or official SDK that handles 70%+ of the logic, it's probably Tier 2.

---

### Tier 3 — Complex (multiplier: 1.8–2.2×)

Work requiring significant architectural decisions, deep technical knowledge, or orchestration of multiple systems. A senior developer would need dedicated time to design this correctly. Errors here are costly to fix.

**Examples:**
- Custom OAuth2/OIDC provider implementation (not just integration — building one)
- Real-time features: live chat, collaborative editing, live dashboards (WebSockets, SSE, etc.)
- Multi-tenant architecture with data isolation (row-level security, schema-per-tenant, etc.)
- Complex state management (Redux sagas, XState machines, complex Zustand stores)
- Custom payment flows: subscriptions with trials, metered billing, invoice generation, proration
- End-to-end encryption implementation
- Custom search relevance and ranking logic
- Complex data pipeline: transformation, validation, enrichment, fan-out
- Infrastructure-as-code for non-trivial cloud architectures (multi-region, auto-scaling, etc.)
- Custom caching strategies (cache invalidation, write-through, multi-layer cache)
- Distributed tracing and observability instrumentation
- Mobile offline-first sync logic
- Custom RBAC with dynamic permissions, resource-scoping, or policy engines
- Integration with complex APIs (ERP systems, healthcare HL7/FHIR, financial data providers)
- Comprehensive integration and E2E test suites
- Custom DSL or configuration language

**Rule of thumb**: If you'd want to architect it on a whiteboard before coding, and the wrong decision would cost weeks to fix — Tier 3.

---

### Tier 4 — Specialized (multiplier: 2.5–4.0×)

Work requiring rare expertise. A typical team would need to either hire a specialist or spend substantial time doing research. This tier covers genuinely novel engineering, research-adjacent work, or systems with very few practitioners.

**Examples:**
- Custom ML model training pipelines (data loading, training loop, evaluation, serving)
- Fine-tuning LLMs on custom data (preprocessing, training infra, evaluation harness)
- Custom neural network architectures or novel ML approaches
- Low-level systems programming (custom memory allocators, kernel modules, drivers)
- Custom cryptographic primitives or protocol implementations
- Real-time bidding engines or high-frequency trading systems
- Custom compilers, parsers, or language runtimes
- Custom database engine or storage layer
- Complex rendering engines (3D, physics simulation, etc.)
- Distributed consensus algorithms (Raft, Paxos, custom CRDT implementations)
- High-throughput stream processing (custom windowing, stateful operators)
- Computer vision pipelines with custom model architectures
- Robotics control systems or embedded firmware
- Custom protocol implementations (network protocols, binary formats)

**Rule of thumb**: If the team would need to read academic papers or hire a PhD to build this — Tier 4.

---

## Multiplier Table

| Tier | Label | Base Multiplier | When to Use the High End |
|------|-------|----------------|--------------------------|
| 1 | Boilerplate | 1.0× | Never goes higher — if it needs judgment, it's not Tier 1 |
| 2 | Moderate | 1.3–1.5× | 1.5× when the integration has unusual edge cases or poor docs |
| 3 | Complex | 1.8–2.2× | 2.2× for real-time systems, multi-tenant, or first-time-for-team tech |
| 4 | Specialized | 2.5–4.0× | 4.0× for research-grade or genuinely novel engineering |

---

## Common Miscategorization Mistakes

**"It's just auth" → Tier 2 at minimum**
Authentication feels simple until you factor in: password reset flows, email verification, session invalidation, brute-force protection, MFA, OAuth provider edge cases, and security auditing. Don't assign Tier 1 to auth.

**"It's just CRUD" → Check the business logic**
If the CRUD has complex validation, computed fields, soft deletes, event sourcing, audit logging, or conditional behavior based on state — it's not just CRUD. Examine the model layer carefully.

**"They used a library for it" → Library reduces effort, not tier**
Using Stripe doesn't make a payment system Tier 1. Custom subscription logic, dunning management, and invoice reconciliation are Tier 3 regardless of which payment library is used.

**"It's just a webhook" → Check what the webhook does**
A webhook receiver that triggers a 12-step orchestration workflow is not Tier 1. Grade the receiver and the orchestration separately.

**Generated code → Exclude from effort, but count the generator config**
The generated Prisma client is Tier 1 (automated). The Prisma schema that drives it, with complex relations, multi-table constraints, and custom extensions, may be Tier 2 or 3.

---

## Uncertainty Escalation

When you're unsure which tier a component belongs in:

1. Look at the most complex file in that component. The tier of the system is often set by its hardest part.
2. If you still can't tell, assign the higher tier and note the uncertainty in the report.
3. Uncertainty is information — add a callout that says "If X is actually simpler than it appears, this component could be reduced by ~N hours."

---

## Special Cases

### Infrastructure & DevOps
Often underestimated because it looks like config files. Key complexity signals:
- Multi-region deployment → Tier 3
- Custom Kubernetes operators or Helm charts → Tier 3
- Standard Dockerfile + docker-compose → Tier 1
- Terraform for non-trivial AWS/GCP/Azure infra → Tier 2–3
- CI/CD pipelines with custom workflows → Tier 2
- Service mesh (Istio, Linkerd) → Tier 3

### Test Suites
Test code is real work. Count it separately:
- Unit tests for business logic → Tier 2 (they require understanding the system)
- Integration tests → Tier 2–3 (fixtures, factories, isolation)
- E2E tests (Playwright, Cypress) → Tier 2–3 (page objects, CI integration, flakiness management)
- Performance/load tests → Tier 3 (tooling, scenario design, analysis)

### Data Migrations
- Simple additive migration → Tier 1
- Migration with data transformation → Tier 2
- Migration requiring backfill of millions of rows with zero-downtime → Tier 3
- Migration between incompatible schemas or systems → Tier 3–4
