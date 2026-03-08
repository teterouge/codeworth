# Codeworth Architecture

## Overview

Codeworth evaluates a repository by combining two complementary forms of analysis:

1. **Source analysis** — examining the structure and content of the codebase
2. **Artifact analysis** — inspecting supporting project artifacts such as CI pipelines, documentation, and validation outputs

These signals are then synthesized using Claude with reference guides that encode estimation heuristics.

The result is a structured rebuild-effort estimate.

---

# Architecture Diagram (ASCII)

```
User Input
("estimate this repo" / GitHub URL / local path)
          │
          ▼
+----------------------+
|   SKILL.md Trigger   |
| Claude skill entry   |
| point and workflow   |
+----------------------+
          │
          ▼
+----------------------+
| Repository Scanner   |
|----------------------|
| • language mix       |
| • LOC                |
| • architecture hints |
| • test coverage      |
| • git history        |
| • complexity signals |
+----------------------+
          │
          │
          │
          ▼
+----------------------+
| Artifact Scanner     |
|----------------------|
| • CI/CD configs      |
| • migration history  |
| • ADR / PRD docs     |
| • benchmarks         |
| • observability      |
| • validation logs    |
+----------------------+
          │
          ▼
+----------------------+
| Claude Analysis      |
|----------------------|
| Applies reference    |
| guides to interpret  |
| repository signals   |
| and classify system  |
| complexity           |
+----------------------+
          │
          ▼
+----------------------+
| Estimation Engine    |
|----------------------|
| • component tiers    |
| • rebuild difficulty |
| • engineering hours  |
| • PM effort          |
| • cost modeling      |
+----------------------+
          │
          ▼
+----------------------+
| Structured Report    |
|----------------------|
| Executive summary    |
| rebuild estimate     |
| component breakdown  |
| cost range           |
| complexity drivers   |
+----------------------+
```

---

# Step-by-Step Flow

## 1. User Input

The user provides a repository for analysis.

This can be:

- a local repository path
- a GitHub repository URL
- a repository already present in the Claude workspace

Optional parameters can refine the estimate:

- team size
- geographic rate assumptions
- analysis purpose (diligence, rewrite planning, consulting estimate)

---

## 2. Repository Source Analysis

The repository scanner inspects the codebase itself.

Signals collected include:

- language distribution
- total lines of code
- generated vs authored code
- presence of tests
- architecture files
- directory structure
- dependency patterns

These signals provide a first approximation of system complexity.

---

## 3. Artifact Analysis

Many repositories encode important engineering work in **artifacts rather than code**.

The artifact scanner detects:

- CI/CD pipelines
- schema migrations
- infrastructure definitions
- architecture decision records
- validation reports
- load tests
- compliance documentation

These artifacts frequently reveal hidden engineering effort.

---

## 4. Claude Reasoning Layer

Claude evaluates the signals produced by both scanners using reference guides stored in the repository.

These guides include:

- rebuild difficulty models
- engineering rate cards
- complexity multipliers
- PM effort estimation heuristics

Claude synthesizes the signals into a structured understanding of the system.

---

## 5. Estimation Engine

Using the interpreted signals, Codeworth constructs a rebuild estimate.

Steps include:

- decomposing the repository into system components
- assigning complexity tiers
- applying rebuild difficulty multipliers
- estimating engineering hours
- estimating PM effort
- converting hours into cost ranges

---

## 6. Structured Report Output

The final result is a report suitable for technical diligence or engineering planning.

Typical report contents include:

- executive summary
- repository overview
- rebuild difficulty rating
- component breakdown
- engineering effort estimate
- PM effort estimate
- recommended team composition
- unified cost range
- complexity drivers and caveats

The goal is not perfect precision, but a **reasoned estimate grounded in architecture rather than raw LOC**.

---

# Key Principle

Rebuild effort is rarely proportional to code size.

Codeworth focuses on the real drivers of engineering effort:

- architecture
- domain complexity
- integration surfaces
- operational maturity
- product rigor

These factors determine replacement cost far more than raw code volume.