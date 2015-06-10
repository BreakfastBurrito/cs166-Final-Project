#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

psql -U db -d db -a -f $DIR/../src/create_tables.sql
psql -U db -d db -a -f $DIR/../src/create_index.sql
psql -U db -d db -a -f $DIR/../src/load_data.sql
