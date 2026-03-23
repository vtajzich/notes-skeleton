#!/usr/bin/env python3
import os
import re
import sys

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"_archived", ".git", "node_modules", ".obsidian"}

WIKILINK_ALIASED = re.compile(r'\[\[([^\]|]+)\|([^\]]+)\]\]')
WIKILINK_SIMPLE = re.compile(r'\[\[([^\]|]+)\]\]')


def should_skip(path_from_root):
    parts = path_from_root.split(os.sep)
    return any(p in EXCLUDE_DIRS for p in parts)


def add_md_ext(target):
    if not target.endswith('.md') and not target.endswith('.json'):
        return target + '.md'
    return target


def display_name_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]


def replace_aliased(m):
    target = m.group(1).strip()
    display = m.group(2).strip()
    return f'[{display}]({add_md_ext(target)})'


def replace_simple(m):
    target = m.group(1).strip()
    display = display_name_from_path(target)
    return f'[{display}]({add_md_ext(target)})'


def is_inside_code_fence(lines, line_idx):
    in_fence = False
    for i in range(line_idx):
        stripped = lines[i].lstrip()
        if stripped.startswith('```'):
            in_fence = not in_fence
    return in_fence


def convert_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    lines = original.split('\n')
    converted_lines = []
    total_replacements = 0

    for i, line in enumerate(lines):
        if is_inside_code_fence(lines, i):
            converted_lines.append(line)
            continue

        new_line = line
        new_line, n1 = WIKILINK_ALIASED.subn(replace_aliased, new_line)
        new_line, n2 = WIKILINK_SIMPLE.subn(replace_simple, new_line)
        total_replacements += n1 + n2
        converted_lines.append(new_line)

    if total_replacements > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(converted_lines))

    return total_replacements


def main():
    total_files = 0
    total_replacements = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            filepath = os.path.join(root, fname)
            rel = os.path.relpath(filepath, VAULT_ROOT)
            if should_skip(rel):
                continue

            count = convert_file(filepath)
            if count > 0:
                total_files += 1
                total_replacements += count
                print(f"  {rel}: {count} replacements")

    print(f"\nDone: {total_replacements} replacements across {total_files} files")


if __name__ == '__main__':
    main()
