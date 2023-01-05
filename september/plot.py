#!/usr/bin/python3

# Example data: https://collaborating.tuhh.de/e-exk4/advent/-/blob/master/23-rseq/data.Ryzen7_PRO_5850U

# Data format:
# (source: https://collaborating.tuhh.de/e-exk4/advent/-/blob/master/23-rseq/rseq.c, line 236):

# // Print out the result. We also check that the threads actually
# // counted correctly (state)
# printf("mode=%s threads=%d sum=%ld state=%s aborts=%ld cputime=%fs per_increment=%fns\n",
#MODE, NTHREADS,
# sum, (sum % ROUNDS_PER_THREAD) == 0 ? "ok" : "fail",
# aborts,
# delta,            // total cpu time that was spent
# delta * 1e9 / sum // nanoseconds per increment
# );


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_log(fn):
    with open(fn) as fd:
        lines = fd.readlines()
        rows = []
        for line in lines:
            line = line.strip().split(" ")
            header = [x.split("=")[0] for x in line]
            data = [x.split("=")[1].rstrip("ns") for x in line]
            rows.append(data)
        df = pd.DataFrame(
            columns=header,
            data=rows)
        for x in "threads sum aborts cputime per_increment".split():
            df[x] = df[x].apply(float)
        return df


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.exit("usage: %s [LOGFILE]" % sys.argv[0])
    df = read_log(sys.argv[1])

    per_inc = df.set_index(["mode", "threads"]).per_increment.unstack().T

    ax = per_inc.plot(marker='x', grid=True, figsize=(10, 10))
    ax.set_ylim((0, None))
    ax.set_ylabel("Per Increment [ns]")
    ax.get_figure().savefig('plot.png')
