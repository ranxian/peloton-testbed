### Prepare Peloton

* Peloton repository will be noted as `PELOTON_SRC`
* Paths for Peloton binaries will be noted as `PELOTON_BIN`

1. `cp testbed.conf.example testbed.conf`, then edit `testbed.conf`
2. `cd PELOTON_SRC`, run `./bootstrap`
3. `cd PELOTON_SRC/bin`, run `../configure --prefix=PELOTON_BIN`

After Peloton is properly configured, you no longer need to do it again.

### Build and Run Peloton

run `bash bootstrap.sh`

### Run YCSB Benchmark

1. edit `mesure_performance_ycsb.py`, modify the workload characteristics in the `__main__` part
2. run `python measure_performance_ycsb.py`, you must have completed *Prepare Peloton* and *Build and Run Peloton*. Each time you run this script you should run `bash bootstrap.sh`
