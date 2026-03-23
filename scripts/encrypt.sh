#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SECURE_FILE="${REPO_ROOT}/.secure"
GITIGNORE="${REPO_ROOT}/.gitignore"

if [[ -z "${NOTES_ENCRYPT_KEY:-}" ]]; then
  echo "ERROR: NOTES_ENCRYPT_KEY is not set. Run scripts/setup.sh first." >&2
  exit 1
fi

if [[ ! -f "$SECURE_FILE" ]]; then
  exit 0
fi

hash_cmd() {
  if command -v gsha256sum &>/dev/null; then
    gsha256sum "$1" | cut -d' ' -f1
  else
    shasum -a 256 "$1" | cut -d' ' -f1
  fi
}

patterns=()
while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line%%#*}"
  line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [[ -z "$line" ]] && continue
  patterns+=("$line")
done < "$SECURE_FILE"

[[ ${#patterns[@]} -eq 0 ]] && exit 0

dir_matches() {
  local dirname="$1"
  for p in "${patterns[@]}"; do
    # shellcheck disable=SC2254
    case "$dirname" in
      $p) return 0 ;;
    esac
  done
  return 1
}

matched_dirs=()
while IFS= read -r dir; do
  [[ -z "$dir" ]] && continue
  dirname="$(basename "$dir")"
  if dir_matches "$dirname"; then
    rel_dir="${dir#"${REPO_ROOT}/"}"
    matched_dirs+=("$rel_dir")
  fi
done <<< "$(find "$REPO_ROOT" -type d -not -path '*/.git/*' -not -path '*/.git')"

[[ ${#matched_dirs[@]} -eq 0 ]] && exit 0

enc_files=()
sha_files=()
plaintext_files=()
encrypted_count=0
skipped_count=0

for dir in "${matched_dirs[@]}"; do
  abs_dir="${REPO_ROOT}/${dir}"
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    [[ "$file" == *.enc ]] && continue
    [[ "$file" == *.sha256 ]] && continue

    rel_path="${file#"${REPO_ROOT}/"}"
    enc_path="${file}.enc"
    sha_path="${file}.sha256"
    rel_enc="${rel_path}.enc"
    rel_sha="${rel_path}.sha256"

    current_hash="$(hash_cmd "$file")"

    if [[ -f "$sha_path" && -f "$enc_path" ]]; then
      stored_hash="$(cat "$sha_path")"
      if [[ "$current_hash" == "$stored_hash" ]]; then
        skipped_count=$((skipped_count + 1))
        enc_files+=("$rel_enc")
        sha_files+=("$rel_sha")
        plaintext_files+=("$rel_path")
        continue
      fi
    fi

    openssl enc -aes-256-cbc -pbkdf2 -salt \
      -pass env:NOTES_ENCRYPT_KEY \
      -in "$file" \
      -out "$enc_path"

    printf '%s' "$current_hash" > "$sha_path"

    enc_files+=("$rel_enc")
    sha_files+=("$rel_sha")
    plaintext_files+=("$rel_path")
    encrypted_count=$((encrypted_count + 1))
  done <<< "$(find "$abs_dir" -type f)"
done

gitignore_changed=false
ensure_gitignored() {
  local entry="$1"
  if ! grep -qxF "$entry" "$GITIGNORE" 2>/dev/null; then
    echo "$entry" >> "$GITIGNORE"
    gitignore_changed=true
  fi
}

touch "$GITIGNORE"
ensure_gitignored '!**/*.enc'
ensure_gitignored '!**/*.sha256'
for dir in "${matched_dirs[@]}"; do
  ensure_gitignored "${dir}/**"
done

if [[ "$gitignore_changed" == true ]]; then
  git -C "$REPO_ROOT" add -- .gitignore
fi

if [[ ${#enc_files[@]} -gt 0 ]]; then
  git -C "$REPO_ROOT" add -- "${enc_files[@]}" "${sha_files[@]}"
fi

for pf in "${plaintext_files[@]}"; do
  if git -C "$REPO_ROOT" ls-files --error-unmatch "$pf" &>/dev/null 2>&1; then
    git -C "$REPO_ROOT" rm --cached --quiet -- "$pf"
  fi
done

if [[ $encrypted_count -gt 0 || $skipped_count -gt 0 ]]; then
  echo "encrypt: ${encrypted_count} encrypted, ${skipped_count} unchanged"
fi
