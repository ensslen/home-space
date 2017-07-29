#!/bin/sh

psql service=govhack -P 'format=unaligned' --tuples-only -c 'select array_to_json(array_agg(row_to_json(trademe)),TRUE) from trademe' -o data.json
