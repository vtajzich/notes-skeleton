#!/usr/bin/env python3
"""Map Jira issues to product areas using heuristic rules and manual overrides."""

import json
import os
import re
import sys
from datetime import date

STATUS_FOLDERS = [
    "backlog",
    "in-progress",
    "on-hold",
    "selected-for-development",
    "done",
]
SKIP_FILES = {"_index.md", "project.md", "project.json", "area-map.md", "area-map.json", "area-overrides.json"}
TOP_LEVEL_TYPES = {"Epic", "Objective", "Initiative"}

AREA_DISPLAY = {
    "product-x": "Product X (API Gateway)",
    "product-y": "Product Y (Developer Portal)",
    "infrastructure": "Infrastructure",
    "security": "Security",
    "cross-cutting": "Cross-cutting",
    "unmapped": "Unmapped",
}

AREA_ORDER = [
    "product-x",
    "product-y",
    "infrastructure",
    "security",
    "cross-cutting",
    "unmapped",
]

PREFIX_RULES = [
    (r"\[API\s*Gateway\]", "product-x"),
    (r"\[Gateway\]", "product-x"),
    (r"\[Portal\]", "product-y"),
    (r"\[DevPortal\]", "product-y"),
    (r"\[Infra\]", "infrastructure"),
    (r"\[Security\]", "security"),
    (r"\[BAU\]", "cross-cutting"),
]

LABEL_RULES = {
    "api-gateway": "product-x",
    "portal": "product-y",
    "infrastructure": "infrastructure",
    "security": "security",
}

KEYWORD_RULES = [
    (r"(?i)\bAPI\s*Gateway\b", "product-x"),
    (r"(?i)\brate\s*limit", "product-x"),
    (r"(?i)\brouting\b", "product-x"),
    (r"(?i)\bDeveloper\s*Portal\b", "product-y"),
    (r"(?i)\bservice\s*catalog\b", "product-y"),
    (r"(?i)\bonboarding\b", "product-y"),
    (r"(?i)\bTerraform\b", "infrastructure"),
    (r"(?i)\bKubernetes\b", "infrastructure"),
    (r"(?i)\bCI/CD\b", "infrastructure"),
    (r"(?i)\bCVE\b", "security"),
    (r"(?i)\bvulnerabilit", "security"),
    (r"(?i)\bsecurity\s*scan", "security"),
]


def parse_issue_file(filepath, folder):
    with open(filepath) as f:
        content = f.read()
    lines = content.split("\n")

    key = os.path.basename(filepath).replace(".md", "")
    summary = ""
    itype = ""
    priority = ""
    assignee = ""
    labels = []

    for line in lines:
        if line.startswith("# ") and not summary:
            m = re.match(r"^# [A-Z]+-\d+\s+(.*)", line)
            summary = m.group(1).strip() if m else line[2:].strip()
            continue
        if line.startswith("> [") and not itype:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                itype = parts[1]
                priority = parts[2]
                assignee = parts[3]
            continue
        if line.startswith("> Labels:"):
            label_text = line.replace("> Labels:", "").strip()
            labels = [l.strip() for l in label_text.split(",") if l.strip()]
            continue

    return {
        "key": key,
        "summary": summary,
        "type": itype,
        "priority": priority,
        "assignee": assignee,
        "labels": labels,
        "folder": folder,
    }


def classify(issue, overrides):
    key = issue["key"]
    summary = issue["summary"]
    labels = issue["labels"]

    if key in overrides:
        return overrides[key], "override"

    for pattern, area in PREFIX_RULES:
        if re.search(pattern, summary):
            return area, "prefix"

    for label in labels:
        if label in LABEL_RULES:
            return LABEL_RULES[label], "label"

    for pattern, area in KEYWORD_RULES:
        if re.search(pattern, summary):
            return area, "keyword"

    return "unmapped", "none"


def load_overrides(jira_dir):
    path = os.path.join(jira_dir, "area-overrides.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def load_all_issues(jira_dir):
    issues = []
    for folder in STATUS_FOLDERS:
        folder_path = os.path.join(jira_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        for fname in sorted(os.listdir(folder_path)):
            if not fname.endswith(".md") or fname in SKIP_FILES:
                continue
            issue = parse_issue_file(os.path.join(folder_path, fname), folder)
            issues.append(issue)
    return issues


def build_area_map_json(issues, overrides):
    mapping = {}
    for issue in issues:
        area, method = classify(issue, overrides)
        mapping[issue["key"]] = {
            "area": area,
            "method": method,
            "type": issue["type"],
            "summary": issue["summary"],
            "folder": issue["folder"],
        }
    return mapping


def build_area_map_md(mapping, issues, today):
    by_area = {a: [] for a in AREA_ORDER}

    for issue in issues:
        entry = mapping[issue["key"]]
        area = entry["area"]
        if area not in by_area:
            by_area[area] = []
        by_area[area].append(issue)

    total = len(issues)
    unmapped_count = len(by_area.get("unmapped", []))

    lines = [
        "# Jira Issues by Product Area",
        "#work/team-a/jira",
        "",
        f"> Last mapped: {today} | Total: {total} | Unmapped: {unmapped_count}",
        "",
    ]

    for area in AREA_ORDER:
        area_issues = by_area.get(area, [])
        if not area_issues:
            continue

        display_name = AREA_DISPLAY.get(area, area)
        lines.append(f"## {display_name}")
        lines.append("")

        top_level = [i for i in area_issues if i["type"] in TOP_LEVEL_TYPES]
        rest = [i for i in area_issues if i["type"] not in TOP_LEVEL_TYPES]

        if top_level:
            lines.append("### Epics & Objectives")
            for iss in sorted(top_level, key=lambda x: x["key"]):
                method = mapping[iss["key"]]["method"]
                meta = f"{iss['type']}, {iss['priority']}, {iss['assignee']}"
                lines.append(
                    f"- [{iss['key']}]({iss['folder']}/{iss['key']}.md) ({meta}) — {iss['summary']} `[{method}]`"
                )
            lines.append("")

        if rest:
            lines.append("### Tasks & Stories")
            for iss in sorted(rest, key=lambda x: x["key"]):
                method = mapping[iss["key"]]["method"]
                meta = f"{iss['type']}, {iss['priority']}, {iss['assignee']}"
                lines.append(
                    f"- [{iss['key']}]({iss['folder']}/{iss['key']}.md) ({meta}) — {iss['summary']} `[{method}]`"
                )
            lines.append("")

    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: map-jira-areas.py <jira_dir>", file=sys.stderr)
        sys.exit(1)

    jira_dir = sys.argv[1].rstrip("/")
    today = date.today().isoformat()

    overrides = load_overrides(jira_dir)
    issues = load_all_issues(jira_dir)
    mapping = build_area_map_json(issues, overrides)

    json_path = os.path.join(jira_dir, "area-map.json")
    with open(json_path, "w") as f:
        json.dump(mapping, f, indent=2)
    print(f"  Wrote {json_path}")

    md_content = build_area_map_md(mapping, issues, today)
    md_path = os.path.join(jira_dir, "area-map.md")
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"  Wrote {md_path}")

    counts = {}
    for entry in mapping.values():
        area = entry["area"]
        counts[area] = counts.get(area, 0) + 1

    print(f"\n  Area distribution ({len(issues)} issues):")
    for area in AREA_ORDER:
        if area in counts:
            print(f"    {AREA_DISPLAY.get(area, area):<35} {counts[area]}")


if __name__ == "__main__":
    main()
