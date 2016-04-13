import os


def get_throughput(dir_name, file_name):
    f = open("%s/%s" % (dir_name, file_name), "r")
    content = f.read()
    f.close()
    result = re.search(r' (\d+\.\d+) requests/sec', content)
    return float(result.group(1))

print ",".join(["Protocol", "Scale", "NewOrder", "Payment", "RPS"])
for protocol in ["OPTIMISTIC", "PESSIMISTIC", "SSI", "TO", "SPECULATIVE_READ", "EAGER_WRITE"]:
    for scale in [1, 4, 8, 12]:
        dir_name = "tpcc_collected_data_%s_%d_%d_%d_%d_%d_%d" % (protocol, 100, 0, 0, 0, 0, scale)
        file_name = "outputfile_%s_%d_%d_%d_%d_%d_%d.log" % (protocol, 100, 0, 0, 0, 0, scale)

        if os.path.exists("%s/%s" % (dir_name, file_name)):
            rps = get_throughput(dir_name, file_name)
            print ','.join([protocol, str(scale), "100", "0", str(rps)])