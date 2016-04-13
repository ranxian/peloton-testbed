import os
import re


def get_throughput(dir_name, file_name):
    f = open("%s/%s" % (dir_name, file_name), "r")
    content = f.read()
    f.close()
    result = re.search(r' (\d+\.\d+) requests/sec', content)
    return float(result.group(1))

def get_abort_rate(dir_name):
    if not os.path.exists("%s/peloton.log" % (dir_name)):
        return 0.0
    f = open("%s/peloton.log" % (dir_name), "r")
    content = f.read()
    f.close()
    result = re.search(r'TxnTotal = (\d+), TxnSuccess = (\d+)', content)
    return (float(result.group(1))-float(result.group(2))) / float(result.group(1))

print ",".join(["Protocol", "Scale", "NewOrder", "Payment", "RPS", "AbrtRate"])
for protocol in ["OPTIMISTIC", "PESSIMISTIC", "SSI", "TO", "SPECULATIVE_READ", "EAGER_WRITE"]:
    for scale in [1, 4, 8, 12]:
        dir_name = "tpcc_collected_data_%s_%d_%d_%d_%d_%d_%d" % (protocol, 100, 0, 0, 0, 0, scale)
        file_name = "outputfile_%s_%d_%d_%d_%d_%d_%d.log" % (protocol, 100, 0, 0, 0, 0, scale)

        if os.path.exists("%s/%s" % (dir_name, file_name)):
            rps = get_throughput(dir_name, file_name)
            abt_rate = get_abort_rate(dir_name)
            print ','.join([protocol, str(scale), "100", "0", str(rps), "%.3f" % (abt_rate * 100)])
            # print ','.join([protocol, str(scale), "100", "0", str(rps)])
