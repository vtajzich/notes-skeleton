#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SECURE_FILE="${REPO_ROOT}/.secure"

if [[ -z "${NOTES_ENCRYPT_KEY:-}" ]]; then
  echo "ERROR: NOTES_ENCRYPT_KEY is not set. Run scripts/setup.sh first." >&2
  exit 1
fi

if [[ ! -f "$SECURE_FILE" ]]; then
  exit 0
fi

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

is_in_matched_dir() {
  local filepath="$1"
  local dir="$(dirname "$filepath")"
  while [[ "$dir" != "$REPO_ROOT" && "$dir" != "/" ]]; do
    if dir_matches "$(basename "$dir")"; then
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

decrypted_count=0
failed_count=0

while IFS= read -r enc_file; do
  [[ -z "$enc_file" ]] && continue
  if is_in_matched_dir "$enc_file"; then
    original="${enc_file%.enc}"
    rel_path="${original#"${REPO_ROOT}/"}"

    mkdir -p "$(dirname "$original")"
    tmp_file="${original}.tmp.$$"
    if openssl enc -d -aes-256-cbc -pbkdf2 \
         -pass env:NOTES_ENCRYPT_KEY \
         -in "$enc_file" \
         -out "$tmp_file" 2>/dev/null; then
      mv "$tmp_file" "$original"
      decrypted_count=$((decrypted_count + 1))
    else
      rm -f "$tmp_file"
      echo "WARN: Failed to decrypt ${rel_path}.enc (wrong key?)" >&2
      failed_count=$((failed_count + 1))
    fi
  fi
done <<< "$(find "$REPO_ROOT" -name '*.enc' -type f -not -path '*/.git/*')"

if [[ $decrypted_count -gt 0 || $failed_count -gt 0 ]]; then
  echo "decrypt: ${decrypted_count} decrypted, ${failed_count} failed"
fi
