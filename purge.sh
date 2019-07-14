#!/usr/bin/env bash
psql -f purge.sql
rm -rf public/2019txri
