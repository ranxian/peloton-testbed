# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

import os
import sys
import time
import ConfigParser
import subprocess


# Config the host and port of Peloton
config = ConfigParser.ConfigParser()
config.readfp(open('testbed.conf'))

PELOTON_BIN = config.get("peloton", "PELOTON_BIN") + "/bin"
PELOTON_HOST = config.get("peloton", "PELOTON_HOST")
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

start_cleanup_script = "rm -rf callgrind.out.*"
start_peloton_valgrind_script = "valgrind --tool=callgrind --trace-children=yes %s/peloton -D ./data > /dev/null 2>&1 &" % (PELOTON_BIN)
start_peloton_script = "%s/peloton -D ./data > /dev/null 2>&1 &" % (PELOTON_BIN)
stop_peloton_script = "%s/pg_ctl -D ./data stop" % (PELOTON_BIN)

config_filename = "peloton_ycsb_config.xml"
start_ycsb_bench_script = "%s/oltpbenchmark -b ycsb -c " % (OLTP_HOME) + cwd + "/" + config_filename + " --create=true --load=true --execute=true -s 5 -o %s/outputfile" % (cwd)

def prepare_parameters(thread_num, read_ratio, insert_ratio, update_ratio):
    os.chdir(cwd)
    parameters["$THREAD_NUMBER"] = str(thread_num)
    parameters["$READ_RATIO"] = str(read_ratio)
    parameters["$INSERT_RATIO"] = str(insert_ratio)
    parameters["$UPDATE_RATIO"] = str(update_ratio)
    ycsb_template = ""
    with open("ycsb_template.xml") as in_file:
        ycsb_template = in_file.read()
    for param in parameters:
        ycsb_template = ycsb_template.replace(param, parameters[param])
    with open(config_filename, "w") as out_file:
        out_file.write(ycsb_template)

def start_peloton_valgrind():
    os.chdir(cwd)
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    os.system(start_peloton_valgrind_script)
    time.sleep(5)

def start_peloton():
    os.chdir(cwd)
    os.system(stop_peloton_script)
    os.system(start_cleanup_script)
    os.system(start_peloton_script)
    time.sleep(5)

def start_bench(thread_num, read_ratio, insert_ratio, update_ratio):
    # go to oltpbench directory
    os.chdir(os.path.expanduser(OLTP_HOME))
    cmd = start_ycsb_bench_script + "_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

def stop_peloton():
    # go back to cwd
    os.chdir(cwd)
    os.system(stop_peloton_script)

def collect_data(thread_num, read_ratio, insert_ratio, update_ratio):
    os.chdir(cwd)
    dir_name = "ycsb_collected_data_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio)
    os.system("rm -rf " + dir_name)
    os.system("mkdir " + dir_name)
    os.system("mv callgrind.out.* " + dir_name)
    os.system("mv outputfile_t%d_%d_%d_%d.* %s/" % (thread_num, read_ratio, insert_ratio, update_ratio, dir_name))

if __name__ == "__main__":
    read_ratio = 0
    insert_ratio = 0
    update_ratio = 100
    start_peloton()
#    for thread_num in range(1, 7):
    thread_num = 3
    prepare_parameters(thread_num, read_ratio, insert_ratio, update_ratio)
    start_bench(thread_num, read_ratio, insert_ratio, update_ratio)
    time.sleep(10)
    collect_data(thread_num, read_ratio, insert_ratio, update_ratio)
    stop_peloton()
