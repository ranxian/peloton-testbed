# profile tpcc benchmark.

import os
import sys
import time
import ConfigParser
import subprocess
import re
from subprocess import call


# Config the host and port of Peloton
config = ConfigParser.ConfigParser()
config.readfp(open('testbed.conf'))

PELOTON_BIN = config.get("peloton", "PELOTON_BIN") + "/bin"
PELOTON_SRC = config.get("peloton", "PELOTON_SRC")
PELOTON_HOST = config.get("peloton", "PELOTON_HOST")
PELOTON_USER = config.get("peloton", "PELOTON_USER")
PELOTON_PORT = "57721"

cwd = os.getcwd()
OLTP_HOME = "%s/oltpbench" % (cwd)

parameters = {
"$IP":  "localhost",
"$PORT": "57721",
"$SCALE_FACTOR": "1",
"$TIME":  "10",
"$THREAD_NUMBER": "1",
"$READ_RATIO": "0",
"$INSERT_RATIO": "0",
"$SCAN_RATIO": "0",
"$UPDATE_RATIO": "0",
"$DELETE_RATIO": "0",
"$RMW_RATIO": "0"
}

# Benchmark parameters
scheme = "PESSIMISTIC"
thread_num = 1
new_order_ratio = 100
payment_ratio = 0
order_status_ratio = 0
delivery_ratio = 0
stock_level_ratio = 0

start_cleanup_script = "rm -rf callgrind.out.*"
start_peloton_valgrind_script = "valgrind --tool=callgrind --trace-children=yes %s/peloton -D ./data > /dev/null 2>&1 &" % (PELOTON_BIN)

# Requires that peloton-testbed is in the home directory
start_peloton_script = "%s/peloton -D ~/peloton-testbed/data > /dev/null 2>&1 &" % (PELOTON_BIN)
stop_peloton_script = "%s/pg_ctl -D ~/peloton-testbed/data stop" % (PELOTON_BIN)

config_filename = "peloton_tpcc_config.xml"
start_benchmark_script = "%s/oltpbenchmark -b tpcc -c " % (OLTP_HOME) + cwd + "/" + config_filename + " --create=true --load=true --execute=true -s 5 -o "

def prepare_parameters():
    os.chdir(cwd)
    parameters["$THREAD_NUMBER"] = str(thread_num)
    parameters["$NEW_ORDER_RATIO"] = str(new_order_ratio)
    parameters["$PAYMENT_RATIO"] = str(payment_ratio)
    parameters["$ORDER_STATUS_RATIO"] = str(order_status_ratio)
    parameters["$DELIVERY_RATIO"] = str(delivery_ratio)
    parameters["$STOCK_LEVEL_RATIO"] = str(stock_level_ratio)
    parameters["$IP"] = PELOTON_HOST

    template = ""
    with open("tpcc_template.xml") as in_file:
        template = in_file.read()
    for param in parameters:
        template = template.replace(param, parameters[param])
    with open(config_filename, "w") as out_file:
        out_file.write(template)

def get_result_path():
  global cwd
  return "%s/outputfile_%s_%d_%d_%d_%d_%d" % (cwd, scheme, new_order_ratio, payment_ratio, order_status_ratio, delivery_ratio, stock_level_ratio)

def start_peloton_valgrind():
    os.chdir(cwd)
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    os.system(start_peloton_valgrind_script)
    time.sleep(5)

def start_bench():
    # go to oltpbench directory
    os.chdir(os.path.expanduser(OLTP_HOME))
    call("ant", shell=True)
    cmd = start_benchmark_script + get_result_path()
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

def stop_peloton():
    # go back to cwd
    cmd = "ssh %s@%s -t 'bash -l -c \"%s\"'" % (PELOTON_USER, PELOTON_HOST, stop_peloton_script)
    call(cmd, shell=True)

def collect_data():
    os.chdir(cwd)
    dir_name = "tpcc_collected_data_%s_%d_%d_%d_%d_%d" % (scheme, new_order_ratio, payment_ratio, order_status_ratio, delivery_ratio, stock_level_ratio)
    os.system("rm -rf " + dir_name)
    os.system("mkdir " + dir_name)
    os.system("mv callgrind.out.* " + dir_name)
    os.system("mv %s.* %s/" % (get_result_path(), dir_name))

def bootstrap_peloton():
    shell_cmd = "cd ~/peloton-testbed/; bash bootstrap_peloton.sh " + scheme
    cmd = "ssh %s@%s -t 'bash -l -c \"%s\"'" % (PELOTON_USER, PELOTON_HOST, shell_cmd)
    call(cmd, shell=True)

if __name__ == "__main__":
    scheme = "OPTIMISTIC"
    new_order_ratio = 100
    thread_num = 20
    # bootstrap_peloton()
    prepare_parameters()
    start_bench()
    collect_data()
    stop_peloton()
    # for scheme in ["OPTIMISTIC", "PESSIMISTIC", "SSI", "SPECULATIVE_READ", "TO"]:
    #   for contention in [0.0]:#, 0.1, 0.5, 0.99]:
    #     for read_ratio in [0]:#, 30, 50, 70, 100]:
    #       for thread_num in range(20, 20+1):
    #         insert_ratio = 0
    #         update_ratio = 100 - read_ratio
    #         bootstrap_peloton()
    #         prepare_parameters()
    #         start_bench()
    #         collect_data()
    #         stop_peloton()
