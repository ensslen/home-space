#!/bin/sh

psql service=govhack -P 'format=unaligned' --tuples-only -f data.sql -o data.json
