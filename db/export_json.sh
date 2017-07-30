#!/bin/sh

psql service=govhack -P 'format=unaligned' --tuples-only -f export_json.sql -o data.json
