# Log & Validation Document Analysis

Repositories often contain evidence of effort that isn't visible in source code alone: log files, test output records, validation reports, audit trails, CI/CD artifacts, and compliance documentation. These files are signal-rich — they tell you how rigorously the product was built and operated, which directly translates into effort that must be estimated.

This guide explains how to find, read, and quantify the effort implied by these artifacts.

---

## What to Look For

Run the log scanner script to surface these files automatically:

```bash
python scripts/scan_logs_and_validation.py <repo_path>
```

Then interpret the results using the guidance below.

---

## File Type Categories and What They Imply

### 1. Test Output & Coverage Reports

**File patterns**: `*.log`, `coverage.xml`, `lcov.info`, `coverage/`, `test-results/`, `junit*.xml`, `*.tap`, `*.trx`, `.nyc_output/`

**What they tell you**:
- The existence of coverage reports implies a team that tracked quality over time — this is PM and engineering culture investment, not just code
- Detailed JUnit/xUnit XML output implies CI/CD integration, which required someone to set up and maintain
- Coverage data at 80%+ implies deliberate effort to write tests against every meaningful path — not incidental

**Effort signals**:

| Signal | Implied Effort |
|--------|----------------|
| Coverage report exists | CI integration was built and maintained (add 20–40 eng hours) |
| Coverage > 80% | Deliberate test discipline (coverage already counted in test multiplier, but flag as high-effort signal) |
| Multiple historical coverage reports | Long-running test culture, likely required test gates in CI |
| Flaky test logs or retry reports | Team invested in test reliability (add 10–20 eng hours per major test suite) |

---

### 2. CI/CD Pipeline Logs & Artifacts

**File patterns**: `.github/workflows/*.yml` output artifacts, `build.log`, `deploy.log`, `pipeline.log`, `.circleci/`, `Jenkinsfile`, `*.buildkite`

**What they tell you**:
- Number of pipeline stages = complexity of release process
- Evidence of environment-specific pipelines (dev/staging/prod) implies release management discipline
- Artifact retention (build outputs checked in) implies versioned release process

**Effort signals**:

| Signal | Implied Effort |
|--------|----------------|
| Multi-stage pipeline (build → test → lint → deploy) | 20–60 eng hours to build and maintain |
| Matrix testing (multiple OS/language versions) | 10–30 additional eng hours |
| Environment-specific pipelines (dev/stage/prod) | 20–40 additional eng hours |
| Deployment rollback configuration | 15–30 eng hours |
| Canary/blue-green deployment logic | 30–60 eng hours |

---

### 3. Validation & Compliance Documents

**File patterns**: `VALIDATION.md`, `SECURITY.md`, `COMPLIANCE.md`, `AUDIT.md`, `*.audit`, `pentest-report*`, `soc2*`, `hipaa*`, `gdpr*`, `*.pdf` (in docs/), `validation/`, `compliance/`

**What they tell you**:
- Any compliance documentation implies a compliance process was run, managed, and documented — this is mostly PM, legal, and security time, not engineering
- Penetration test reports imply external security audits were conducted (typically $15K–$50K contracts, not counted in hourly estimates — flag separately)
- SOC 2 / HIPAA / GDPR documentation implies ongoing compliance programs

**Effort signals**:

| Document Type | Implied PM/Compliance Hours | Notes |
|--------------|----------------------------|-------|
| SECURITY.md with disclosure policy | 5–10 PM hours | Routine, mostly template |
| Internal security audit report | 20–60 PM + security eng hours | Depends on scope |
| External pentest report | Note separately — external contract cost | Don't count in hourly estimate |
| SOC 2 Type I preparation evidence | 100–300 PM + eng hours | Major initiative |
| SOC 2 Type II readiness | 200–500+ hours across teams | Multi-month effort |
| HIPAA compliance documentation | 150–400 hours | Legal + technical + PM |
| GDPR implementation evidence | 80–200 hours | Privacy engineering + PM |
| ISO 27001 documentation | 300–600+ hours | Major compliance program |

---

### 4. Load & Performance Test Reports

**File patterns**: `k6/`, `locust/`, `*.jmx`, `loadtest*.log`, `perf-report*`, `benchmark*.json`, `flamegraph*`

**What they tell you**:
- Performance testing is a deliberate engineering investment — someone designed scenarios, ran them, analyzed results, and made changes in response
- Flamegraphs and profiling output imply performance optimization work beyond just running tests

**Effort signals**:

| Signal | Implied Effort |
|--------|----------------|
| Any load test scripts exist | 20–40 eng hours to design, run, and interpret |
| Multiple load test scenarios (ramp, spike, soak) | 40–80 eng hours |
| Flame graphs / profiling output | 20–60 eng hours of performance optimization |
| Documented performance SLAs | 10–20 PM hours to define, plus eng hours to achieve |

---

### 5. API & Contract Test Artifacts

**File patterns**: `*.postman_collection.json`, `*.insomnia`, `openapi*.json`, `swagger*.json`, `pact/`, `*.pact.json`, `contract-tests/`

**What they tell you**:
- Postman/Insomnia collections imply QA or developer advocacy work to document and validate API behavior
- Pact files (consumer-driven contract testing) imply a mature microservices testing strategy — significant investment
- Multiple OpenAPI spec versions imply API evolution was managed deliberately

**Effort signals**:

| Signal | Implied Effort |
|--------|----------------|
| Postman/Insomnia collection | 10–30 QA/eng hours |
| Full OpenAPI spec (not generated) | 20–60 eng + PM hours |
| Pact consumer-driven contract tests | 40–80 eng hours |
| API versioning with migration guides | 20–40 PM + eng hours per major version |

---

### 6. Database Validation & Migration Logs

**File patterns**: `migrations/`, `db/migrate/`, `seeds/`, `*.sql` dumps, `schema_migrations` table references, `alembic/versions/`, `flyway/`

**What they tell you**:
- Migration count is one of the best proxies for product iteration depth — each migration represents a shipped change to the data model
- Complex migrations (data backfills, schema transformations) represent significant one-time engineering effort
- Seed data files imply thought put into demo/onboarding data, which is PM and engineering time

**Effort signals**:

| Signal | Implied Effort |
|--------|----------------|
| < 10 migrations | Early-stage product, minimal migration effort |
| 10–50 migrations | Active product development, 40–120 eng hours in migrations |
| 50–200 migrations | Mature product, 100–400 eng hours in migrations |
| 200+ migrations | Long-running product, migration management as an ongoing discipline |
| Data backfill migrations | Add 20–80 eng hours per major backfill |
| Zero-downtime migration patterns | Add 30–60 eng hours per complex migration |

---

### 7. Monitoring & Observability Artifacts

**File patterns**: `alerts/*.yaml`, `dashboards/*.json`, `grafana/`, `datadog/`, `newrelic.yml`, `prometheus/`, `*.alert`

**What they tell you**:
- Alert definitions imply someone designed and maintains an on-call process
- Dashboard definitions imply ongoing investment in operational visibility
- Runbooks imply operational maturity — someone wrote documentation for incident response

**Effort signals**:

| Signal | Implied Effort |
|--------|----------------|
| Any alert config exists | 10–30 eng + PM hours to define SLOs and alerting thresholds |
| Grafana/DataDog dashboard definitions | 20–60 eng hours per major dashboard |
| Runbooks in docs/ | 5–15 PM/eng hours per runbook |
| SLO definitions | 15–30 PM + eng hours to define and instrument |

---

### 8. Changelog & Release Notes

**File patterns**: `CHANGELOG.md`, `CHANGELOG.rst`, `HISTORY.md`, `RELEASES.md`, `docs/releases/`

**What they tell you**:
- A detailed changelog is evidence of a PM-driven release process
- Count the number of releases/versions and the depth of entries
- Changelogs with user-facing feature descriptions (not just commit hashes) imply PM wrote or reviewed them

**Effort signals**:

| Signal | Implied Effort |
|--------|----------------|
| Changelog exists with 5–20 versions | 2–4 PM hours per major release for changelog maintenance |
| Changelog with 20–100 versions | Ongoing PM discipline; 50–200 PM hours total across product history |
| Changelog entries with feature descriptions | PM involvement confirmed; use as feature count source |
| Semantic versioning with detailed breaking change docs | 10–20 PM + eng hours per major version |

---

## Output Format for Log & Validation Analysis

Add this section to the report after the Repository Overview:

```
## Validation & Documentation Artifact Analysis

**Artifacts found**: [comma-separated list of artifact types discovered]

| Artifact Type | Files Found | Implied Effort | Role |
|--------------|-------------|----------------|------|
| Test coverage reports | [N files] | [N hours] | Engineering |
| CI/CD pipeline configs | [N stages] | [N hours] | DevOps / Engineering |
| Load/performance test reports | [yes/no] | [N hours] | Engineering |
| Compliance documents | [type] | [N hours] | PM / Legal / Security |
| API contract tests | [yes/no] | [N hours] | Engineering / QA |
| Database migrations | [N migrations] | [N hours] | Engineering |
| Monitoring/alert configs | [yes/no] | [N hours] | DevOps / Engineering |
| Changelog entries | [N versions] | [N hours] | PM / Engineering |

**Total additional hours from artifact analysis**: [N hours]  
**Breakdown by role**: Engineering: [N] hrs | PM: [N] hrs | DevOps: [N] hrs | QA: [N] hrs

**Notable findings**:
- [Any specific high-effort artifacts worth calling out]
- [Any compliance requirements that should be flagged separately]
```

---

## Important Caveats for Artifact Analysis

**Artifacts may not be from the repo's production history.** A repo might contain sample coverage reports, example Grafana dashboards, or placeholder compliance docs that were never actually used. Use judgment — if the artifact looks templated or sparse, note that caveat.

**External cost items must be flagged separately.** Penetration tests, SOC 2 audits, and legal reviews have market rates that aren't hourly engineering rates. Flag these as separate line items (e.g., "SOC 2 Type II audit: typically $30,000–$100,000 external cost, not included in hourly estimate").

**Migration count can be inflated.** Some frameworks create a migration file for every minor change. Look at the complexity and size of migrations, not just the count.
