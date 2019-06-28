#!/usr/bin/env bash
sudo -u postgres psql -f purge.sql
python3 -m ReMatch
