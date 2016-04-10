#!/bin/sh

NUM_CORE=12
PELOTON_HOME=~/rxian/iso_peloton_bench
PELOTON_BIN=~/rxian/bin/bin
# Clean up any existing peloton data directory
rm -rf data

pwd=`pwd`
# Rebuild and install
cd $PELOTON_HOME/build/
make -j$NUM_CORE
make install
# sudo make install
cd $pwd

# Setup new peloton data directory
initdb data

# Copy over the peloton configuration file into the directory
sed 's/peloton_logging_mode aries/peloton_logging_mode invalid/g' $PELOTON_HOME/scripts/oltpbenchmark/postgresql.conf > data/postgresql.conf

# Kill any existing peloton processes
pkill -9 peloton
$PELOTON_BIN/pg_ctl -D data stop

# Clean up any existing peloton log
rm data/pg_log/peloton.log

# Start the peloton server
echo "Starting peloton"
$PELOTON_BIN/peloton -D ./data & # > /dev/null 2>&1 &

# Wait for a moment for the server to start up...
sleep 2

# Create a "postgres" user
$PELOTON_BIN/createuser -r -s postgres

# Create a default database for psql
$PELOTON_BIN/createdb $USER

# Create YCSB and TPC-C databases

echo "create database ycsb;" | $PELOTON_BIN/psql postgres
echo "create database tpcc;" | $PELOTON_BIN/psql postgres

echo "Peloton prepared"
$PELOTON_BIN/pg_ctl -D ./data stop
