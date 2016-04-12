import os

print ",".join(["Protocol", "Scale", "NewOrder", "Payment", "RPS"])
for protocol in ["OPTIMISTIC", "PESSIMISTIC", "SSI", "TO", "SPECULATIVE_READ", "EAGER_WRITE"]:
    for scale in [1, 4, 8, 12]:
        dir_name = "tpcc_collected_data_%s_%d_%d_%d_%d_%d_%d" % (protocol, 100, 0, 0, 0, 0, scale)
        file_name = "outputfile_%s_%d_%d_%d_%d_%d_%d.res" % (protocol, 100, 0, 0, 0, 0, scale)

        if os.path.exists("%s/%s" % (dir_name, file_name)):
            f = open("%s/%s" % (dir_name, file_name), "r")
            content = f.readline()
            content = f.readline()
            f.close()

            rps = float(content.split(",")[1])
            print ','.join([protocol, str(scale), "100", "0", str(rps)])