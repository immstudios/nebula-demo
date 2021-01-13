#!/bin/bash

PGPASSWORD=nebulapass psql -U postgres <<-EOSQL
    CREATE USER nebula WITH PASSWORD 'nebula';
    CREATE DATABASE nebula OWNER nebula;
EOSQL

PGPASSWORD=nebula psql -U nebula nebula --file=/docker-entrypoint-initdb.d/schema
