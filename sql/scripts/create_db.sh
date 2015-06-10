#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#psql -p $PGPORT $DB_NAME < $DIR/../src/create_tables.sql
#psql -p $PGPORT $DB_NAME < $DIR/../src/create_indexes.sql
#psql -p $PGPORT $DB_NAME < $DIR/../src/load_data.sql

psql -U db -d db -a -f $DIR/../src/create_indexes.sql
psql -U db -d db -a -f $DIR/../src/create_tables.sql
psql -U db -d db -a -f $DIR/../src/load_data.sql
