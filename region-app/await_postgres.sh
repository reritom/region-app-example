#!/bin/sh
until /usr/bin/pg_isready -h postgres -p 5432 -t 30
do
    echo ...
    sleep 1
done
