#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/docs/inventory.md"
cd "$ROOT"

echo "# Repo Inventory (Auto-Generated)" > "$OUT"
echo "" >> "$OUT"
echo "Generated: $(date -u +"%Y-%m-%d %H:%M:%SZ")" >> "$OUT"
echo "" >> "$OUT"

# List top-level dirs of interest
for d in apps packages services src; do
  if [ -d "$d" ]; then
    echo "## $d/" >> "$OUT"
    find "$d" -maxdepth 2 -type d | sed 's/^/- /' >> "$OUT"
    echo "" >> "$OUT"
  fi
done

echo "## Key Files" >> "$OUT"
for f in README.md package.json pyproject.toml requirements.txt docker-compose.yml; do
  if [ -f "$f" ]; then
    echo "- $f" >> "$OUT"
  fi
done
echo "" >> "$OUT"

echo "## Docs Present" >> "$OUT"
find docs -maxdepth 1 -type f -name '*.md' 2>/dev/null | sed 's/^/- /' >> "$OUT" || true
echo "" >> "$OUT"

echo "Done -> $OUT"
