#!/bin/bash
# This script will compile and run peloton

# Pull latest testbed
git pull origin master

# The repository of peloton source code
PELOTON_SRC=~/peloton/iso_peloton_bench
# The directory to put all the built binaries, you should configure peloton like
# ../configure --prefix=~/bin
PELOTON_BIN=~/peloton
# Branch of the peloton source code
PELOTON_BRANCH=master
# Host of the peloton server
PELOTON_HOST=localhost

while IPS= read -r line; do
    first=`echo $line | head -c 1`
    if [ "$first" != "#" ] && [ "$line" != "[peloton]" ]; then
        declare $line
    fi
done < "testbed.conf"

pwd=`pwd`

rm -rf data
# Rebuild and install
cd $PELOTON_SRC/build/
git checkout $PELOTON_BRANCH
git pull origin $PELOTON_BRANCH
make -j
make install

cd $pwd

# Setup new peloton data directory
initdb data

# Copy over the peloton configuration file into the directory
cp $pwd/config/postgresql.conf data/postgresql.conf
cp $pwd/config/pg_hba.conf data/pg_hba.conf

# Kill any existing peloton processes
pkill -9 peloton
$PELOTON_BIN/bin/pg_ctl -D data stop

# Clean up any existing peloton log
rm data/pg_log/peloton.log

# Start the peloton server
echo "Starting peloton"
$PELOTON_BIN/bin/peloton -D ./data & # > /dev/null 2>&1 &

# Wait for a moment for the server to start up...
sleep 2

# Create a "postgres" user
$PELOTON_BIN/bin/createuser -r -s postgres

# Create a default database for psql
$PELOTON_BIN/bin/createdb $USER

# Create YCSB and TPC-C databases

echo "create database ycsb;" | $PELOTON_BIN/bin/psql postgres
echo "create database tpcc;" | $PELOTON_BIN/bin/psql postgres

echo "Peloton prepared"
$PELOTON_BIN/bin/pg_ctl -D ./data stop

# Compile oltp benchmark
(cd $pwd/oltpbench; ant)

