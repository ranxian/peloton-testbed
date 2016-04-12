### Prepare Peloton

* Peloton repository will be noted as `PELOTON_SRC`
* Paths for Peloton binaries will be noted as `PELOTON_BIN`

1. `cp testbed.conf.example testbed.conf`, then edit `testbed.conf`
2. `cd PELOTON_SRC`, run `./bootstrap`
3. `cd PELOTON_SRC/bin`, run `../configure --prefix=PELOTON_BIN`

After Peloton is properly configured, you no longer need to do it again.

### Run YCSB Benchmark

1. edit `mesure_performance_ycsb.py`, modify the workload settings in the `__main__` part
2. Run `python measure_performance_ycsb.py`, you must first complete *Prepare Peloton* step.

### Run TPC-C Benchmark

1. edit `measure_performance_tpcc.py`, modify the workload settings in the `__main__` part
2. Run `python measure_performance_tpcc.py`, you must first complete *Prepare Peloton* step.