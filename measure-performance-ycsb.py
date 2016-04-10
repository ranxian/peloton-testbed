# profile ycsb benchmark.
# author: Yingjun Wu <yingjun@comp.nus.edu.sg>
# date: March 5th, 2016

import os
import sys
import time

server1_name = "yingjunw@dev1.db.pdl.cmu.local"
server2_name = "yingjunw@dev2.db.pdl.cmu.local"

oltp_home = "~/rxian/oltpbench"
peloton_bin = "~/rxian/bin/bin"

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

cwd = os.getcwd()
config_filename = "peloton_ycsb_config.xml"
start_cleanup_script = "rm -rf callgrind.out.*"
start_peloton_valgrind_script = "valgrind --tool=callgrind --trace-children=yes %s/peloton -D ./data > /dev/null 2>&1 &" % (peloton_bin)
start_peloton_script = "%s/peloton -D ./data > /dev/null 2>&1 &" % (peloton_bin)
stop_peloton_script = "%s/pg_ctl -D ./data stop" % (peloton_bin)
start_ycsb_bench_script = "%s/oltpbenchmark -b ycsb -c " % (oltp_home) + cwd + "/" + config_filename + " --create=true --load=true --execute=true -s 5 -o %s/outputfile" % (cwd)

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
    os.chdir(os.path.expanduser(oltp_home))
    os.system(start_ycsb_bench_script + "_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio))
    time.sleep(2)

def stop_peloton():
    # go back to cwd
    os.chdir(cwd)
    os.system(stop_peloton_script)

def collect_data(thread_num, read_ratio, insert_ratio, update_ratio):
    os.chdir(cwd)
    dir_name = "collected_data_t" + str(thread_num) + "_" + str(read_ratio) + "_" + str(insert_ratio) + "_" + str(update_ratio)
    os.system("rm -rf " + dir_name)
    os.system("mkdir " + dir_name)
    os.system("mv callgrind.out.* " + dir_name)

if __name__ == "__main__":
    read_ratio = 0
    insert_ratio = 0
    update_ratio = 100
    start_peloton()
#    for thread_num in range(1, 7):
    thread_num = 3
    prepare_parameters(thread_num, read_ratio, insert_ratio, update_ratio)
    start_bench(thread_num, read_ratio, insert_ratio, update_ratio)
    stop_peloton()
