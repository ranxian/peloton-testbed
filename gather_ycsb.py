import os

print ",".join(["Protocol", "Contention", "Read", "Write", "MR", "RPS"])
for protocol in ["OPTIMISTIC", "PESSIMISTIC", "SSI", "TO", "SPECULATIVE_READ"]:
    for contention in ["0.00", "0.10", "0.20", "0.30", "0.40", "0.50", "0.60", "0.70", "0.80", "0.90", "0.99"]:
        for read_ratio in ["0", "30", "50", "70", "100"]:
            dir_name = "ycsb_collected_data_%s_%s_%s_%s_%s_%d" % (protocol, contention, read_ratio, "0", str(100-int(read_ratio)), 20)
            file_name = "outputfile_%s_%s_%s_%s_%s_%d.res" % (protocol, contention, read_ratio, "0", str(100 - int(read_ratio)), 20)

            if os.path.exists("%s/%s" % (dir_name, file_name)):
                f = open("%s/%s" % (dir_name, file_name), "r")
                content = f.readline()
                content = f.readline()
                f.close()

                rps = float(content.split(",")[1])
                print ','.join([protocol, contention, read_ratio, str(100-int(read_ratio)), "0", str(rps)])


        dir_name = "ycsb_collected_data_%s_%s_0_0_0_100" % (protocol, contention)
        file_name = "outputfile_%s_%s_0_0_0_100.res" % (protocol, contention)

        if os.path.exists("%s/%s" % (dir_name, file_name)):
            f = open("%s/%s" % (dir_name, file_name), "r")
            content = f.readline()
            content = f.readline()
            f.close()

            rps = float(content.split(",")[1])
            print ','.join([protocol, contention, "0", "0", "100", str(rps)])