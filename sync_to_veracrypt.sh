#!/bin/bash
veracrypt --text --mount /secure/volumes/AIFOLIO_CORE_VERA.hc /mnt/vera --password="YOUR_PASSWORD"
rsync -av --progress --exclude=".git" --exclude-from=".gitignore" ./AIFOLIO_FINAL_V12/ /mnt/vera/AIFOLIO_BACKUP/
veracrypt -d /mnt/vera
