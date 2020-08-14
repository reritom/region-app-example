#!/bin/sh
# This script is used as a delay until the postgres server is ready to accept connections
until /usr/bin/pg_isready -h postgres -p 5432 -t 30
do
    echo ...
    sleep 1
done
