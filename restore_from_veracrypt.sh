#!/bin/bash
veracrypt --text --mount /secure/volumes/AIFOLIO_CORE_VERA.hc /mnt/vera --password="YOUR_PASSWORD"
rsync -av --progress /mnt/vera/AIFOLIO_BACKUP/ ./AIFOLIO_FINAL_V12_RESTORED/
veracrypt -d /mnt/vera
