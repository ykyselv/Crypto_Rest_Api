#!/bin/bash
    psql -v ON_ERROR_STOP=1 --username postgres -c "CREATE DATABASE cryptobase"


