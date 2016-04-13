## Getting started

First clone this repo

```
git clone https://github.com/ranxian/peloton-testbed --recursive
```

### Prepare Peloton

* Peloton repository will be noted as `PELOTON_SRC`
* Paths for Peloton binaries will be noted as `PELOTON_BIN`

1. `cp testbed.conf.example testbed.conf`, then edit `testbed.conf`
2. `cd PELOTON_SRC`, run `./bootstrap`
3. `cd PELOTON_SRC/bin`, run `../configure --prefix=PELOTON_BIN`

After Peloton is properly configured, you no longer need to do it again.

If you after a client machine and a server machine for benchmark, you need to make sure that `ssh PELOTON_USER@PELOTON_HOST` can work directly, for example you may consider add the pubkey of the client machine to the server machine. See `testbed.conf.example` for details.

### Run YCSB Benchmark

1. Edit `mesure_performance_ycsb.py`, modify the workload settings in the `__main__` part
2. Run `python measure_performance_ycsb.py`, you must first complete *Prepare Peloton* step.
3. Run `python gather_ycsb.py` to gather result.

### Run TPC-C Benchmark

1. Edit `measure_performance_tpcc.py`, modify the workload settings in the `__main__` part
2. Run `python measure_performance_tpcc.py`, you must first complete *Prepare Peloton* step.
3. Run `python gather_tpcc.py` to gather result.