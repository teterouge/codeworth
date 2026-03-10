  Repository Estimation Report

  Repo: AI-Powered Culture Assessment Platform
  Analyzed: 2026-03-09
  Estimated for: Solo developer or small startup team (1–2 engineers)

  ---
  Executive Summary

  This repo is a Next.js 14 MVP that evaluates job candidates against company leadership principles using Claude AI. It features a two-version assessment pipeline: V1 (single scenario evaluation) and V2 (three-call orchestration with scenario + Big Five reasoning + weighted combined recommendation). The codebase is lean and well-architected —
  ~3,300 lines of application TypeScript/TSX — but the real value is in the prompt engineering, evaluation rubrics, and the considerable product thinking encoded in 20+ specification documents. Most of the cost to rebuild is engineering + iteration time, not volume.

  Total estimated effort: 6–13 weeks / 0.2–0.4 person-years
  Cost range: $40,000 – $67,000 USD (all roles combined)
  Confidence: High — the codebase is small and well-scoped; uncertainty is in rework and iteration cycles, not hidden complexity.

  ---
  Repository Overview

  - Primary language(s): TypeScript / TypeScript-React (TSX)
  - Framework(s): Next.js 14 (App Router), React 18, Tailwind CSS
  - Architecture pattern: Monolith Next.js app, API Routes for backend, file-based JSONL persistence
  - Lines of code (excluding generated/vendor/docs): ~3,300 lines of application code (TypeScript + TSX + CSS + config); 7,926 attributed to tests (includes README and fixture inflation)
  - Test coverage: Light — 3 real test files (unit: AgentDB, Claude API; integration: evaluation flow) plus fixtures and utilities
  - Notable integrations: Anthropic Claude SDK (claude-sonnet-4-20250514), Vercel Analytics
  - Product type: Developer portfolio / demo tool (solo project)

  ---
  Rebuild Difficulty Assessment

  Rating: LOW
  Score: 1.5/15 — Effort multiplier: 1.0× (no upward adjustment)

  ┌──────────────────────────┬───────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │        Dimension         │ Score │                                                                        Key Signals                                                                         │
  ├──────────────────────────┼───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Domain Knowledge         │ 1     │ HR/talent assessment domain with LLM prompt engineering; moderate specialized knowledge (evaluation rubric design, Big Five methodology, weighted scoring) │
  ├──────────────────────────┼───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Infrastructure Coupling  │ 0     │ No Dockerfile, no Kubernetes, no Terraform, no CI/CD pipelines; plain Vercel deployment                                                                    │
  ├──────────────────────────┼───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Data Model Complexity    │ 0     │ No database schema, no migrations; ~5 TypeScript interfaces, JSONL flat-file storage                                                                       │
  ├──────────────────────────┼───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Integration Surface Area │ 0     │ 1 external integration (Anthropic API); well-documented SDK                                                                                                │
  ├──────────────────────────┼───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Operational Maturity     │ 0.5   │ Light test suite present; no production monitoring, SLOs, runbooks, or load tests                                                                          │
  ├──────────────────────────┼───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Total                    │ 1.5   │                                                                                                                                                            │
  └──────────────────────────┴───────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Note on script false-positives: The analyze_repo.py script flagged domains like payments_fintech, distributed_consensus, and blockchain — these are false positives from the demo scenario content (a fintech payment bug story) and docs, not the actual product domain. The real domain is HR/talent assessment, which is standard web application
  territory.

  Why this matters: At ~3,300 LOC this is exactly what it appears to be. There is no hidden institutional knowledge gap — a competent team rebuilding this would find it exactly as complex as it looks.

  ---
  Component Breakdown (Engineering)

  ┌──────────────────────────────────────────┬──────┬───────────┬────────────┬────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │                Component                 │ Tier │ Raw Hours │ Multiplier │ Adjusted Hours │                                                    Notes                                                     │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Project scaffolding & config             │ 1    │ 4         │ 1.0×       │ 4              │ Next.js, Tailwind, PostCSS, TypeScript                                                                       │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Landing page & marketing UI              │ 2    │ 12        │ 1.25×      │ 15             │ HeroSection, ProblemExplanation, PrinciplesOverview, EducationalBlock — polished copy + layout               │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Multi-step assessment flow               │ 2    │ 16        │ 1.3×       │ 21             │ question-1/2/results pages, ProgressIndicator, NavigationButtons, local state management                     │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ V1 Evaluation API + Claude integration   │ 2    │ 16        │ 1.4×       │ 22             │ Single Claude call, JSON parsing with code-block stripping, error handling, validation                       │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ V2 Evaluation API (3-call orchestration) │ 3    │ 20        │ 1.8×       │ 36             │ 3 sequential Claude calls, 65/35 weighted scoring, misalignment detection, 3-min timeout                     │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ LLM Prompt engineering                   │ 3    │ 16        │ 1.8×       │ 29             │ 3 system prompts with nuanced rubrics, 5-dimension scoring guides, cross-evaluation consistency checks       │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Results display components               │ 2    │ 20        │ 1.3×       │ 26             │ ResultsView, BigFiveEvaluationSection, CombinedRecommendation, CollapsibleSection, ScenarioEvaluationSection │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ AgentDB file-based storage               │ 2    │ 6         │ 1.3×       │ 8              │ JSONL persistence, singleton pattern, filter/query, best-effort error handling                               │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ TypeScript types & shared library        │ 1    │ 8         │ 1.0×       │ 8              │ types.ts (16 interfaces), scenarios.ts, state-management.ts                                                  │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Test suite                               │ 2    │ 15        │ 1.3×       │ 20             │ Unit tests for AgentDB + Claude API, integration test for evaluation flow, fixtures, test helpers            │
  ├──────────────────────────────────────────┼──────┼───────────┼────────────┼────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Total                                    │      │ 133       │            │ 189            │                                                                                                              │
  └──────────────────────────────────────────┴──────┴───────────┴────────────┴────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  ---
  Estimation Adjustments (Engineering)

  ┌───────────────────────┬─────────────────────────────────────────────┬─────────────────┐
  │        Factor         │             Multiplier Applied              │ Resulting Hours │
  ├───────────────────────┼─────────────────────────────────────────────┼─────────────────┤
  │ Rework & iteration    │ 1.35× (MVP with documented v1→v2 evolution) │ 255             │
  ├───────────────────────┼─────────────────────────────────────────────┼─────────────────┤
  │ Testing & QA          │ +20% (light but real test suite)            │ 306             │
  ├───────────────────────┼─────────────────────────────────────────────┼─────────────────┤
  │ Documentation         │ +8% (substantial: 20+ docs, 2 full PRDs)    │ 330             │
  ├───────────────────────┼─────────────────────────────────────────────┼─────────────────┤
  │ Team coordination     │ +0% (solo developer project)                │ 330             │
  ├───────────────────────┼─────────────────────────────────────────────┼─────────────────┤
  │ Integration glue work │ +5% (1 external API, minimal)               │ 347             │
  ├───────────────────────┼─────────────────────────────────────────────┼─────────────────┤
  │ Engineering Subtotal  │                                             │ 347 hours       │
  └───────────────────────┴─────────────────────────────────────────────┴─────────────────┘

  ---
  Validation & Documentation Artifact Analysis

  Artifacts found: Spec/PRD documents, fixture data

  ┌──────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────┬───────────────┬──────────────────┐
  │    Artifact Type     │                                        Files Found                                        │ Implied Hours │       Role       │
  ├──────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┼───────────────┼──────────────────┤
  │ Spec / PRD documents │ 3 (prd.md 1,426 lines, MVP_v2_PRD.md 1,349 lines, fix_build_error.md) │ 34 hrs        │ PM               │
  ├──────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┼───────────────┼──────────────────┤
  │ Seed / fixture data  │ 1 (sampleAssessments.json)                                                                │ 8 hrs         │ Engineering / QA │
  ├──────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┼───────────────┼──────────────────┤
  │ Artifact Subtotal    │                                                                                           │ 42 hours      │                  │
  └──────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────┴───────────────┴──────────────────┘

  ---
  Product Manager Effort

  Applicable: Partially — solo developer project (single committer across 10 commits, Nov–Dec 2025)

  Since the developer was their own PM, PM time is largely folded into the engineering estimate. However, the two full PRDs (~2,775 lines combined) represent significant upfront product thinking that a rebuild team would need to recreate: evaluation rubric design, scoring rationale, v1→v2 migration analysis, Big Five methodology justification,
  and weighted recommendation logic.

  PM estimation basis: 6 distinct product features, solo developer role, 2 full PRDs with detailed specs confirmed in artifact scan. PM time folded into engineering per solo-developer convention — artifact hours above capture the most visible PM deliverables.

  PM-to-engineering ratio applied: ~12% (developer tool / demo — PM role absorbed by engineer)
  Estimated standalone PM hours if team-built: ~42 hours (covered by artifact subtotal above)

  ┌─────────────────────────────────┬─────────────────┬──────────────────────────────────────────────────────────────────────────────────────┐
  │           PM Activity           │ Estimated Hours │                                       Evidence                                       │
  ├─────────────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Discovery & problem framing     │ 8               │ PRD problem statement section, competitive framing vs. personality tests             │
  ├─────────────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Specification & story writing   │ 20              │ 2 full PRDs with user flows, feature specs, V1→V2 analysis                           │
  ├─────────────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Evaluation rubric design        │ 8               │ Big Five scoring guide, weighting rationale (65/35 split), recommendation thresholds │
  ├─────────────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Acceptance testing coordination │ 4               │ IMPLEMENTATION_COMPLETE.md, NEXT_STEPS.md                                            │
  ├─────────────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ Post-launch iteration framing   │ 2               │ V2_IMPLEMENTATION_SUMMARY.md                                                         │
  ├─────────────────────────────────┼─────────────────┼──────────────────────────────────────────────────────────────────────────────────────┤
  │ PM Subtotal                     │ 42              │ (artifact-sourced; not double-counted in engineering hours)                          │
  └─────────────────────────────────┴─────────────────┴──────────────────────────────────────────────────────────────────────────────────────┘

  ---
  Recommended Team

  A single senior full-stack engineer with LLM integration experience could build this solo in a focused sprint. Optionally pair with a mid-level engineer to parallelize UI and API work.

  - Senior full-stack (lead): Next.js, TypeScript, LLM prompt engineering, API design — 70% of hours
  - Mid full-stack: React components, UI polish, test writing — 30% of hours
  - No dedicated DevOps, QA, or design role needed (Vercel handles deployment, Tailwind handles styling, tests are self-contained)

  Time to ship (2-person team working in parallel):
  - Aggressive timeline: 5 weeks
  - Realistic timeline: 7 weeks
  - Conservative timeline: 10 weeks

  ---
  Unified Cost Estimate

  Rate assumptions: US market rates, startup/MVP seniority mix ($150/hr senior + $110/hr mid = ~$140/hr blended)

  ┌─────────────────────────────────────┬───────┬─────────┬──────────┐
  │                Role                 │ Hours │  Rate   │ Subtotal │
  ├─────────────────────────────────────┼───────┼─────────┼──────────┤
  │ Engineering (blended, senior + mid) │ 347   │ $140/hr │ $48,580  │
  ├─────────────────────────────────────┼───────┼─────────┼──────────┤
  │ PM / spec artifacts                 │ 42    │ $110/hr │ $4,620   │
  ├─────────────────────────────────────┼───────┼─────────┼──────────┤
  │ Total (mid scenario)                │ 389   │         │ $53,200  │
  └─────────────────────────────────────┴───────┴─────────┴──────────┘

  ┌────────────────────────┬─────────────┬────────────┐
  │        Scenario        │ Total Hours │ Total Cost │
  ├────────────────────────┼─────────────┼────────────┤
  │ Low (10th percentile)  │ 308         │ $40,000    │
  ├────────────────────────┼─────────────┼────────────┤
  │ Mid (50th percentile)  │ 389         │ $53,000    │
  ├────────────────────────┼─────────────┼────────────┤
  │ High (90th percentile) │ 493         │ $67,000    │
  └────────────────────────┴─────────────┴────────────┘

  Rebuild difficulty multiplier: 1.0× (LOW) — no adjustment applied.

  ---
  Key Complexity Drivers

  - Three-call LLM orchestration in V2: The evaluate-v2 route chains three Claude calls sequentially — scenario eval → Big Five reasoning eval → combined recommendation — with a 3-minute timeout and error handling at each stage. Getting this right requires careful async design and meaningful prompt iteration.
  - Prompt engineering as product IP: The three system prompts are the core value of this product. The Big Five rubric (90 lines), Combined Recommendation logic (weighted 65/35 scoring, misalignment detection), and scenario evaluation rubric represent real iterative design work that can't be reproduced by reading documentation.
  - V1→V2 migration already encoded: The repo contains both V1 and V2 APIs running in parallel, plus a full analysis doc (ARCHITECTURE_ANALYSIS_V1_TO_V2.md). A rebuild starting from scratch gets this design clarity for free — but would need to make these same architectural decisions independently.
  - Documentation-to-code ratio: ~18,891 lines of Markdown vs ~3,300 lines of application code (~5.7:1). This reflects a solo developer who thought carefully before coding — a meaningful proportion of the total effort was in product design, not implementation.

  ---
  Caveats & Assumptions

  What was NOT analyzed:
  - Design assets (none present — UI is Tailwind CSS only)
  - Database contents (data/evaluations.jsonl is production data, not analyzed)
  - Actual LLM prompt iteration history (Claude API call counts, token costs, prompt refinement cycles)

  What was assumed:
  - US market rates, mid-senior seniority mix
  - The rebuild team is familiar with Next.js and the Anthropic SDK
  - Clean execution: no major scope changes mid-build
  - Prompt engineering hours assume the evaluation rubrics are being designed from scratch, not adapted from existing frameworks

  What is excluded from the hourly estimate:
  - Ongoing Anthropic API costs (~$0.01–0.05 per evaluation at Sonnet pricing)
  - Vercel hosting (free tier likely sufficient for demo traffic)
  - Any future features described in docs/NEXT_STEPS.md (ATS integration, multi-scenario, admin dashboard)
  - .hive-mind/ and .claude-flow/ AI orchestration artifacts — these appear to be development tooling used during the build, not part of the product itself