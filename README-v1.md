# CodeWorth

A Claude Code skill that analyzes a code repository and produces a detailed human time and cost estimate for building it from scratch.

## What it does

Point it at any repository and get back a structured report covering:

- **Component breakdown** — every major part of the codebase classified by complexity tier (Boilerplate → Specialized)
- **Hour estimates** — per component, with applied complexity multipliers
- **Adjustment factors** — rework cycles, testing, documentation, team coordination, integration overhead
- **Team recommendation** — what roles and seniority mix would realistically build this
- **Cost range** — low/mid/high scenarios with configurable rates (US, Western Europe, Eastern Europe/Latam, South Asia)
- **Confidence rating** — honest about what's uncertain and why

## Use cases

- **Acquisition due diligence** — understand replacement cost before buying a company or codebase
- **Freelancer scoping** — price a rewrite or migration job accurately
- **Engineering leadership** — communicate the value of technical assets in business terms
- **Portfolio evaluation** — assess the substance of a candidate's work
- **Rewrite planning** — scope the effort before committing to a rebuild

## Installation

```bash
# Add the marketplace
claude plugin marketplace add <your-github-username>/codeworth

# Install the skill
claude plugin install wodeworth
```

Or clone and install locally:

```bash
git clone https://github.com/<your-github-username>/codeworth
claude plugin add ./codeworth
```

## Usage

Just ask naturally in Claude Code:

```
Estimate the cost to rebuild this repo from scratch: /path/to/repo
```

```
How many developer hours went into this codebase? github.com/someorg/somerepo
```

```
I'm buying a startup — what would their codebase cost to recreate? Eastern Europe rates.
```

The skill will:
1. Run the analysis script to gather hard data
2. Walk the repo structure to identify components and complexity
3. Apply the estimation framework
4. Output a structured report

## Structure

```
codeworth/
├── SKILL.md                      # Main skill instructions
├── scripts/
│   └── analyze_repo.py           # Repository analysis script
├── references/
│   ├── complexity-guide.md       # Four-tier complexity taxonomy
│   ├── rate-cards.md             # Hourly rates by role, seniority, region
│   └── multipliers.md            # All estimation multipliers with worked examples
└── evals/
    └── evals.json                # Test cases for skill validation
```

## Methodology

The estimation methodology is based on:

- **Complexity tiering** rather than LOC counting (lines of code is a notoriously poor proxy for effort)
- **Boehm's research** on rework and iteration overhead
- **COCOMO II** principles adapted for modern stacks
- **Empirical rate data** from QSM, industry surveys, and public compensation data
- **Component-level decomposition** matching how PMs actually track engineering work

The key insight: a 200-line real-time bidding system is worth more than a 2,000-line CRUD app. Complexity, not volume, drives cost.

## Caveats

This skill analyzes static code — it cannot see:
- The original team's productivity or velocity
- False starts, deleted code, or pre-commit work
- Design assets, database contents, or proprietary data
- Institutional knowledge and domain understanding
- Ongoing maintenance costs

The output is an estimate, not a quote. Always review with judgment before using in financial decisions.

## License

Apache 2.0
