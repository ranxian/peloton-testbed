# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

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
"$SCALE_FACTOR": "20",
"$TIME":  "10",
"$THREAD_NUMBER": "1",
"$READ_RATIO": "0",
"$INSERT_RATIO": "0",
"$SCAN_RATIO": "0",
"$UPDATE_RATIO": "0",
"$DELETE_RATIO": "0",
"$RMW_RATIO": "0"
}

scheme = "OPTIMISTIC"
contention = 0.00
read_ratio = 0
insert_ratio = 0
update_ratio = 100
mr_ratio = 0
thread_num = 24


start_cleanup_script = "rm -rf callgrind.out.*"
start_peloton_valgrind_script = "valgrind --tool=callgrind --trace-children=yes %s/peloton -D ./data > /dev/null 2>&1 &" % (PELOTON_BIN)
start_peloton_script = "%s/peloton -D ~/peloton-testbed/data > /dev/null 2>&1 &" % (PELOTON_BIN)
stop_peloton_script = "%s/pg_ctl -D ~/peloton-testbed/data stop" % (PELOTON_BIN)

config_filename = "peloton_ycsb_config.xml"
start_ycsb_bench_script = "%s/oltpbenchmark -b ycsb -c " % (OLTP_HOME) + cwd + "/" + config_filename + " --create=true --load=true --execute=true -s 5 -o "

def prepare_parameters():
    os.chdir(cwd)
    parameters["$THREAD_NUMBER"] = str(thread_num)
    parameters["$READ_RATIO"] = str(read_ratio)
    parameters["$INSERT_RATIO"] = str(insert_ratio)
    parameters["$UPDATE_RATIO"] = str(update_ratio)
    parameters["$MR_RATIO"] = str(mr_ratio)
    parameters["$IP"] = PELOTON_HOST
    ycsb_template = ""
    with open("ycsb_template.xml") as in_file:
        ycsb_template = in_file.read()
    for param in parameters:
        ycsb_template = ycsb_template.replace(param, parameters[param])
    with open(config_filename, "w") as out_file:
        out_file.write(ycsb_template)

    os.system("sed -i 's/ZIPFIAN_CONSTANT=.*?;/ZIPFIAN_CONSTANT=%.f;/' %s" % (contention, OLTP_HOME + "/src/com/oltpbenchmark/distributions/ZipfianGenerator.java"))

def get_result_path():
  global cwd
  return "%s/outputfile_%s_%.2f_%d_%d_%d_%d" % (cwd, scheme, contention, read_ratio, insert_ratio, update_ratio, mr_ratio)

def start_peloton_valgrind():
    os.chdir(cwd)
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    os.system(start_peloton_valgrind_script)
    time.sleep(5)

def start_bench():
    # go to oltpbench directory
    os.chdir(os.path.expanduser(OLTP_HOME))
    call("ant clean", shell=True)
    call("ant", shell=True)
    cmd = start_ycsb_bench_script + get_result_path()
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

def stop_peloton():
    # go back to cwd
    cmd = "ssh %s@%s -t 'bash -l -c \"%s\"'" % (PELOTON_USER, PELOTON_HOST, stop_peloton_script)
    call(cmd, shell=True)

def collect_data():
    os.chdir(cwd)
    dir_name = "ycsb_collected_data" + "_" + scheme + "_"+ "%.2f" % (contention) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio) + "_" + str(mr_ratio)
    os.system("rm -rf " + dir_name)
    os.system("mkdir " + dir_name)
    os.system("mv callgrind.out.* " + dir_name)
    os.system("mv %s.* %s/" % (get_result_path(), dir_name))

def bootstrap_peloton():
    shell_cmd = "cd ~/peloton-testbed/; bash bootstrap_peloton.sh " + scheme
    cmd = "ssh %s@%s -t 'bash -l -c \"%s\"'" % (PELOTON_USER, PELOTON_HOST, shell_cmd)
    call(cmd, shell=True)


# R/W: 0/100, 10/90, 30/70, 50/50, 70/30, 100/0 
# Cont: 0, 0.1, 0.3, 0.5, 0.9, 0.99
# Thr: 1-12
if __name__ == "__main__":
    # for scheme in ["OPTIMISTIC", "PESSIMISTIC", "SSI", "SPECULATIVE_READ", "TO", "EAGER_WRITE"]:
    #   for contention in [0.0]:#, 0.1, 0.5, 0.99]:
    #     for read_ratio in [0]:#, 30, 50, 70, 100]:
    #       thread_num = 24
    #     insert_ratio = 0
    #     update_ratio = 100 - read_ratio
    #     bootstrap_peloton(scheme)
    #     prepare_parameters()
    #     start_bench()
    #     collect_data()
    #     stop_peloton()

    for scheme in ["OPTIMISTIC", "PESSIMISTIC", "SSI", "SPECULATIVE_READ", "TO", "EAGER_WRITE"]:
      for contention in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]:
        insert_ratio = 0
        update_ratio = 0
        read_ratio = 0
        mr_ratio = 100
        bootstrap_peloton()
        prepare_parameters()
        start_bench()
        collect_data()
        stop_peloton()
