#!/bin/bash
set -e

dup_hashes="all_duplicate_hashes_list.txt"
all_hashes="all_file_hashes.txt"
log="deduplication_cleanup.log"
> "$log"

while read -r hash; do
  # Extract file paths for this hash, handling spaces and special characters
  grep "^$hash " "$all_hashes" | sed 's/.*) = //' | while IFS= read -r file; do
    echo "$file"
  done > tmp_dup_files.txt
  count=$(wc -l < tmp_dup_files.txt)
  if [ "$count" -le 1 ]; then
    rm -f tmp_dup_files.txt
    continue
  fi
  # Find the most recently modified file
  latest=$(ls -t $(cat tmp_dup_files.txt | sed 's/^/"/;s/$/"/') 2>/dev/null | head -n 1)
  # Delete all except the latest
  while IFS= read -r f; do
    if [ "$f" != "$latest" ]; then
      rm -f "$f"
      echo "Deleted duplicate: $f (kept $latest)" >> "$log"
    fi
  done < tmp_dup_files.txt
  rm -f tmp_dup_files.txt
done < "$dup_hashes"
