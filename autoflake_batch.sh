#!/bin/bash
set -e
log="autoflake_failures.log"
> "$log"
find ./AIFOLIO_KNOWLEDGE_INJECT ./frontend ./scripts ./tests -type f -name '*.py' | while read -r file; do
  if [ -f "$file" ]; then
    .venv/bin/autoflake --in-place --remove-unused-variables --remove-all-unused-imports --expand-star-imports --ignore-init-module-imports --quiet "$file" || echo "$file" >> "$log"
  fi
done
