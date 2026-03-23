#!/usr/bin/env python3
import os
import re
import sys
import urllib.parse

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"_archived", ".git", "node_modules", ".obsidian", "scripts"}

MD_LINK = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def should_skip(rel_path):
    parts = rel_path.split(os.sep)
    return any(p in EXCLUDE_DIRS for p in parts)


def is_internal_link(target):
    if target.startswith(('http://', 'https://', 'mailto:', '#', 'applenotes://')):
        return False
    if target.endswith(('.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
        return False
    return True


def check_file(filepath):
    broken = []
    file_dir = os.path.dirname(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_fence = False
    for line_num, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if stripped.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        for m in MD_LINK.finditer(line):
            target = m.group(2).strip()
            if not is_internal_link(target):
                continue

            target_clean = urllib.parse.unquote(target)
            target_clean = target_clean.split('#')[0]

            if not target_clean:
                continue

            if target_clean.startswith('.'):
                full_path = os.path.normpath(os.path.join(file_dir, target_clean))
            else:
                full_path = os.path.join(VAULT_ROOT, target_clean)

            if not os.path.exists(full_path):
                broken.append((line_num, target, m.group(0)))

    return broken


def main():
    all_broken = []

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in sorted(files):
            if not fname.endswith('.md') and not fname.endswith('.mdc'):
                continue
            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, VAULT_ROOT)
            if should_skip(rel):
                continue

            broken = check_file(filepath)
            if broken:
                for line_num, target, full_match in broken:
                    all_broken.append((rel, line_num, target, full_match))

    if not all_broken:
        print("All links resolve. No broken links found.")
        return

    print(f"Found {len(all_broken)} broken links:\n")
    current_file = None
    for rel, line_num, target, full_match in all_broken:
        if rel != current_file:
            current_file = rel
            print(f"\n{rel}:")
        print(f"  L{line_num}: {target}")
        print(f"         {full_match}")

    sys.exit(1)


if __name__ == '__main__':
    main()
