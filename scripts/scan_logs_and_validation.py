#!/usr/bin/env python3
"""
scan_logs_and_validation.py — Scans a repository for log files, test artifacts,
validation documents, compliance materials, and other non-source evidence of
engineering and PM effort.

Usage:
    python scripts/scan_logs_and_validation.py <repo_path> [--output <output.json>]

Output:
    JSON summary of discovered artifacts and implied effort signals.
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Artifact pattern definitions
# Each entry: (category, label, glob patterns, implied_role, effort_signal)
# ---------------------------------------------------------------------------

ARTIFACT_CATEGORIES = [
    {
        "category": "test_coverage",
        "label": "Test Coverage Reports",
        "role": "Engineering",
        "patterns": [
            r"coverage\.xml$", r"lcov\.info$", r"coverage\.json$",
            r"\.nyc_output", r"coverage/lcov", r"cobertura\.xml$",
            r"clover\.xml$", r"jacoco\.xml$", r"\.coverage$",
        ],
        "dirs": ["coverage", ".nyc_output", "htmlcoverage", ".coverage"],
    },
    {
        "category": "test_results",
        "label": "Test Result / JUnit Reports",
        "role": "Engineering / QA",
        "patterns": [
            r"junit.*\.xml$", r"test-results.*\.xml$", r"\.trx$",
            r"test_output\.log$", r"rspec.*\.xml$", r"\.tap$",
            r"pytest.*\.xml$", r"mocha.*\.json$",
        ],
        "dirs": ["test-results", "test_results", "junit-reports"],
    },
    {
        "category": "ci_cd",
        "label": "CI/CD Pipeline Configs",
        "role": "DevOps / Engineering",
        "patterns": [
            r"\.github/workflows/.*\.ya?ml$", r"\.circleci/config\.ya?ml$",
            r"Jenkinsfile$", r"\.buildkite/.*\.ya?ml$", r"\.gitlab-ci\.ya?ml$",
            r"azure-pipelines\.ya?ml$", r"cloudbuild\.ya?ml$",
            r"\.travis\.ya?ml$", r"appveyor\.ya?ml$", r"bitbucket-pipelines\.ya?ml$",
        ],
        "dirs": [".github/workflows", ".circleci", ".buildkite"],
    },
    {
        "category": "load_testing",
        "label": "Load / Performance Test Reports",
        "role": "Engineering",
        "patterns": [
            r"k6.*\.js$", r"locustfile.*\.py$", r"\.jmx$",
            r"loadtest.*\.log$", r"perf[-_]report", r"benchmark.*\.json$",
            r"flamegraph.*\.svg$", r"artillery.*\.ya?ml$", r"gatling.*\.scala$",
            r"wrk.*\.sh$", r"ab[-_]results",
        ],
        "dirs": ["k6", "locust", "loadtest", "performance-tests", "perf"],
    },
    {
        "category": "compliance",
        "label": "Compliance / Security Documents",
        "role": "PM / Legal / Security",
        "patterns": [
            r"SECURITY\.md$", r"COMPLIANCE\.md$", r"AUDIT\.md$",
            r"pentest[-_]report", r"soc2", r"soc_2", r"hipaa", r"gdpr",
            r"iso27001", r"pci[-_]dss", r"fedramp", r"ccpa",
            r"data[-_]processing[-_]agreement", r"dpa\.md$",
            r"privacy[-_]policy", r"vulnerability[-_]disclosure",
            r"bug[-_]bounty", r"security[-_]policy",
        ],
        "dirs": ["compliance", "security", "audit", "legal"],
    },
    {
        "category": "api_contracts",
        "label": "API Contract / Collection Files",
        "role": "Engineering / QA",
        "patterns": [
            r"\.postman_collection\.json$", r"\.postman_environment\.json$",
            r"\.insomnia$", r"openapi.*\.(json|ya?ml)$",
            r"swagger.*\.(json|ya?ml)$", r"\.pact\.json$",
            r"pact/.*\.json$", r"api[-_]spec\.(json|ya?ml)$",
            r"contract[-_]tests?/",
        ],
        "dirs": ["pact", "contract-tests", "api-specs", "postman"],
    },
    {
        "category": "database_migrations",
        "label": "Database Migrations",
        "role": "Engineering",
        "patterns": [
            r"migrations/.*\.(sql|py|rb|js|ts)$",
            r"db/migrate/.*\.rb$",
            r"alembic/versions/.*\.py$",
            r"flyway/.*\.sql$",
            r"\d{14}_.*\.(rb|py|js|ts)$",  # timestamped migration pattern
            r"V\d+__.*\.sql$",              # Flyway naming convention
        ],
        "dirs": ["migrations", "db/migrate", "alembic/versions", "flyway/sql", "database/migrations"],
    },
    {
        "category": "monitoring",
        "label": "Monitoring / Alert Configurations",
        "role": "DevOps / Engineering",
        "patterns": [
            r"alerts?/.*\.ya?ml$", r"dashboards?/.*\.json$",
            r"grafana/.*\.(json|ya?ml)$", r"prometheus/.*\.ya?ml$",
            r"datadog/.*\.ya?ml$", r"newrelic\.ya?ml$",
            r"cloudwatch/.*\.json$", r"pagerduty/.*\.ya?ml$",
            r"runbook.*\.md$", r"playbook.*\.md$", r"slo.*\.ya?ml$",
        ],
        "dirs": ["alerts", "dashboards", "grafana", "prometheus", "monitoring", "runbooks"],
    },
    {
        "category": "changelog",
        "label": "Changelog / Release Notes",
        "role": "PM / Engineering",
        "patterns": [
            r"CHANGELOG\.md$", r"CHANGELOG\.rst$", r"CHANGELOG\.txt$",
            r"CHANGES\.md$", r"HISTORY\.md$", r"RELEASES\.md$",
            r"NEWS\.md$", r"docs/releases/.*\.md$",
        ],
        "dirs": ["docs/releases", "changelogs"],
    },
    {
        "category": "seed_data",
        "label": "Seed / Fixture Data",
        "role": "Engineering / PM",
        "patterns": [
            r"seeds?\.(rb|js|ts|py|sql)$", r"fixtures/.*\.(ya?ml|json|sql)$",
            r"factories/.*\.(rb|js|ts|py)$", r"db/seeds/",
            r"testdata/.*\.(json|ya?ml|csv)$", r"demo[-_]data/",
        ],
        "dirs": ["seeds", "fixtures", "factories", "testdata", "demo-data"],
    },
    {
        "category": "adr",
        "label": "Architecture Decision Records (ADRs)",
        "role": "Engineering / PM",
        "patterns": [
            r"adr[-_]\d+.*\.md$", r"docs/adr/.*\.md$",
            r"decisions/.*\.md$", r"architecture/.*decisions.*\.md$",
            r"\d{4}[-_].*decision.*\.md$",
        ],
        "dirs": ["docs/adr", "adr", "decisions", "architecture/decisions"],
    },
    {
        "category": "specs_prds",
        "label": "Spec / PRD Documents",
        "role": "PM",
        "patterns": [
            r"docs/specs?/.*\.(md|txt|pdf)$",
            r"docs/prd/.*\.(md|txt|pdf)$",
            r"specs?/.*\.md$", r"requirements/.*\.md$",
            r"rfcs?/.*\.md$",
        ],
        "dirs": ["docs/spec", "docs/specs", "docs/prd", "specs", "requirements", "rfcs"],
    },
    {
        "category": "observability_logs",
        "label": "Application / Error Log Files",
        "role": "Engineering",
        "patterns": [
            r"app\.log$", r"error\.log$", r"access\.log$",
            r"production\.log$", r"development\.log$",
            r"application\.log$", r"server\.log$",
            r"logs?/.*\.log$",
        ],
        "dirs": ["logs", "log"],
    },
]

# ---------------------------------------------------------------------------
# Effort signal mapping: category -> implied hours range
# ---------------------------------------------------------------------------

EFFORT_SIGNALS = {
    "test_coverage": {
        "description": "CI integration + coverage tooling setup",
        "hours_low": 20,
        "hours_high": 40,
        "per_additional": 0,
    },
    "test_results": {
        "description": "CI test pipeline integration",
        "hours_low": 10,
        "hours_high": 30,
        "per_additional": 0,
    },
    "ci_cd": {
        "description": "CI/CD pipeline setup and maintenance",
        "hours_low": 20,
        "hours_high": 60,
        "per_additional": 10,  # per additional pipeline file beyond first
    },
    "load_testing": {
        "description": "Load test design, execution, and analysis",
        "hours_low": 20,
        "hours_high": 80,
        "per_additional": 0,
    },
    "compliance": {
        "description": "Compliance program and documentation",
        "hours_low": 40,
        "hours_high": 500,
        "per_additional": 0,
        "note": "External audit costs (pentest, SOC2) should be flagged separately",
    },
    "api_contracts": {
        "description": "API contract testing and collection maintenance",
        "hours_low": 10,
        "hours_high": 80,
        "per_additional": 5,
    },
    "database_migrations": {
        "description": "Database migration effort",
        "hours_low": 1,
        "hours_high": 4,
        "per_additional": 2,  # per migration file
        "mode": "per_file",
    },
    "monitoring": {
        "description": "Monitoring, alerting, and runbook creation",
        "hours_low": 10,
        "hours_high": 60,
        "per_additional": 5,  # per dashboard/alert file
    },
    "changelog": {
        "description": "Release management and changelog maintenance",
        "hours_low": 2,
        "hours_high": 4,
        "per_additional": 2,  # per estimated release
        "mode": "per_release",
    },
    "seed_data": {
        "description": "Seed/fixture data design and maintenance",
        "hours_low": 5,
        "hours_high": 20,
        "per_additional": 0,
    },
    "adr": {
        "description": "Architecture decision documentation",
        "hours_low": 2,
        "hours_high": 6,
        "per_additional": 3,  # per ADR file
        "mode": "per_file",
    },
    "specs_prds": {
        "description": "Product specification and PRD writing",
        "hours_low": 8,
        "hours_high": 20,
        "per_additional": 10,  # per spec doc
        "mode": "per_file",
    },
    "observability_logs": {
        "description": "Application logging instrumentation",
        "hours_low": 5,
        "hours_high": 20,
        "per_additional": 0,
    },
}


def count_changelog_releases(filepath: Path) -> int:
    """Estimate number of releases in a changelog by counting version headings."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        # Match ## [1.2.3] or ## 1.2.3 or ## v1.2.3 or ## 2024-01-01 patterns
        patterns = [
            r"^#{1,3}\s+\[?v?\d+\.\d+",       # ## [1.2.3] or ## v1.2.3
            r"^#{1,3}\s+\d{4}-\d{2}-\d{2}",   # ## 2024-01-15
            r"^#{1,3}\s+Release\s+\d+",         # ## Release 3
        ]
        count = 0
        for line in content.split("\n"):
            for pattern in patterns:
                if re.match(pattern, line):
                    count += 1
                    break
        return count
    except Exception:
        return 0


def scan_artifacts(repo_path: Path) -> dict:
    """Scan a repository for log/validation/artifact files."""
    repo_path = repo_path.resolve()
    
    results = {
        "repo_path": str(repo_path),
        "categories": {},
        "summary": {
            "total_artifact_files": 0,
            "categories_found": [],
            "total_implied_hours_low": 0,
            "total_implied_hours_high": 0,
            "by_role": defaultdict(lambda: {"hours_low": 0, "hours_high": 0}),
        },
        "notable_findings": [],
        "external_cost_flags": [],
    }

    # Compile patterns
    compiled_categories = []
    for cat in ARTIFACT_CATEGORIES:
        compiled = {
            **cat,
            "compiled_patterns": [re.compile(p, re.IGNORECASE) for p in cat["patterns"]],
            "found_files": [],
        }
        compiled_categories.append(compiled)

    # Walk the repo
    skip_dirs = {"node_modules", ".git", "vendor", "venv", ".venv", "__pycache__", "dist", "build"}
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_root = os.path.relpath(root, repo_path)
        
        for filename in files:
            rel_path = os.path.join(rel_root, filename).replace("\\", "/")
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
            
            for cat in compiled_categories:
                for pattern in cat["compiled_patterns"]:
                    if pattern.search(rel_path):
                        full_path = Path(root) / filename
                        size = 0
                        try:
                            size = full_path.stat().st_size
                        except Exception:
                            pass
                        cat["found_files"].append({
                            "path": rel_path,
                            "size_bytes": size,
                        })
                        break

    # Process results per category
    for cat in compiled_categories:
        if not cat["found_files"]:
            continue
        
        category_key = cat["category"]
        signal = EFFORT_SIGNALS.get(category_key, {})
        file_count = len(cat["found_files"])
        
        # Calculate hours
        hours_low = signal.get("hours_low", 0)
        hours_high = signal.get("hours_high", 0)
        mode = signal.get("mode", "fixed")
        per_additional = signal.get("per_additional", 0)
        
        # Special handling
        release_count = 0
        if category_key == "changelog":
            # Count actual releases in changelog
            for f in cat["found_files"]:
                full_path = repo_path / f["path"]
                release_count = count_changelog_releases(full_path)
                if release_count > 0:
                    hours_low = release_count * 2
                    hours_high = release_count * 4
                    break
        elif mode == "per_file":
            hours_low = hours_low + (file_count - 1) * per_additional
            hours_high = hours_high + (file_count - 1) * per_additional
        elif mode == "fixed" and per_additional > 0 and file_count > 1:
            hours_low += (file_count - 1) * per_additional
            hours_high += (file_count - 1) * per_additional

        # Cap migration hours at reasonable max
        if category_key == "database_migrations":
            hours_low = min(file_count * signal["hours_low"], 400)
            hours_high = min(file_count * signal["hours_high"], 600)

        role = cat["role"]
        
        results["categories"][category_key] = {
            "label": cat["label"],
            "role": role,
            "file_count": file_count,
            "sample_files": [f["path"] for f in cat["found_files"][:5]],
            "implied_hours_low": hours_low,
            "implied_hours_high": hours_high,
            "description": signal.get("description", ""),
            "release_count": release_count if category_key == "changelog" else None,
            "note": signal.get("note"),
        }
        
        results["summary"]["total_artifact_files"] += file_count
        results["summary"]["categories_found"].append(category_key)
        results["summary"]["total_implied_hours_low"] += hours_low
        results["summary"]["total_implied_hours_high"] += hours_high
        
        # Role breakdown (split compound roles evenly)
        role_parts = [r.strip() for r in role.split("/")]
        per_role_low = hours_low / len(role_parts)
        per_role_high = hours_high / len(role_parts)
        for r in role_parts:
            results["summary"]["by_role"][r]["hours_low"] += per_role_low
            results["summary"]["by_role"][r]["hours_high"] += per_role_high

        # Notable findings
        if category_key == "compliance":
            for f in cat["found_files"]:
                fname = f["path"].lower()
                if any(term in fname for term in ["pentest", "soc2", "soc_2", "hipaa", "iso27001", "pci"]):
                    results["external_cost_flags"].append({
                        "file": f["path"],
                        "type": "External compliance/audit",
                        "note": "This likely represents an external contract cost (not hourly engineering time). Typical costs: pentest $15K–$50K, SOC 2 audit $30K–$100K, HIPAA assessment $20K–$60K."
                    })

        if category_key == "database_migrations" and file_count > 100:
            results["notable_findings"].append(
                f"Large migration history ({file_count} migrations) suggests a long-running, actively evolved product."
            )

        if category_key == "adr" and file_count >= 5:
            results["notable_findings"].append(
                f"{file_count} Architecture Decision Records found — strong signal of engineering discipline and deliberate technical planning."
            )

        if category_key == "specs_prds":
            results["notable_findings"].append(
                f"{file_count} spec/PRD document(s) found — confirms PM investment in written requirements, not just verbal handoffs."
            )

        if category_key == "load_testing":
            results["notable_findings"].append(
                "Load/performance test artifacts found — implies performance SLAs were defined and validated."
            )

    # Convert defaultdict to regular dict for JSON serialization
    results["summary"]["by_role"] = dict(results["summary"]["by_role"])

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Scan a repository for log/validation/artifact files and estimate implied effort."
    )
    parser.add_argument("repo_path", help="Path to the repository to scan")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    result = scan_artifacts(Path(args.repo_path))
    output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Scan written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
