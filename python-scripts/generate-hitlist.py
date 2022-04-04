from __future__ import print_function
from pathlib import Path

import numpy as np
import argparse
import sys
import SubnetTree

def fill_tree(tree, fh):
    for line in fh:
        line = line.strip()
        try:
            tree[line] = line
        except ValueError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)
    return tree

# gets all the unqiue AS-numbers from the provided routeviews data file
# nb! the full path to the file must be included in the argument
def get_as_numbers_from_file(routeviews_input):
    as_numbers = []
    with open(routeviews_input, "r") as file:
        lines = file.readlines()
        for line in lines:
            list = line.split()
            asn = list[2]
            as_numbers.append(asn)

        # get unqiue values
        as_numbers = np.unique(np.array(as_numbers))
    return as_numbers

# gets the asn from an IP prefix
def get_asn(prefix):
    path = "/mnt/c/Users/Erlend/Downloads/RouteViews data/"
    filename = "routeviews-rv6-20220312-2200-short.txt" 
    full = path + filename
    with open(full, "r") as file:
        lines = file.readlines()
        for line in lines:
            list = line.split()
            ip = list[0]
            prefix_length = list[1]
            ip_with_prefix = ip + "/" + prefix_length
            asn = list[2]

            if prefix == ip_with_prefix:
                return asn
    return 0

# generates a list of all IP-addresses in the ipv6-hitlist that belong to the same AS
def generate_hitlist_per_as(tmp_prefixlist, ip_address_file):
    as_hitlist = []

    tree = SubnetTree.SubnetTree()
    tree = SubnetTree.fill_tree(tree, tmp_prefixlist)

    # generates a list of all IP-addresses in the ipv6-hitlist that belong to the same AS
    for line in ip_address_file:
        print(line + "," + tree[line] + "," + tree[line][-2:])
        new_list = [line, tree[line], tree[line][-2:]]
        as_hitlist.append(new_list)
    
    # get the last item with the longest prefix length
    prefixlength = 0
    ip = 0

    for item in as_hitlist:
        if item[2] > prefixlength:
            prefixlength = item[2]
            ip = item[0]

    return ip


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix-file", required=True, type=argparse.FileType('r'), help="File containing list of RouteViews prefixes")
    parser.add_argument("-i", "--ip-address-file", required=True, type=argparse.FileType('r'), help="File containing IP addresses to be matched against (non-)aliased prefixes")
    parser.add_argument("-h", "--filtered-hitlist", required=True, type=argparse.FileType('r'), help="File containing the final hitlist that you want to write to")
    args = parser.parse_args()

    tree = SubnetTree.SubnetTree()
    tree = SubnetTree.fill_tree(tree, args.prefix_file)

    tuple_list = []
    hitlist = []
    as_numbers = get_as_numbers_from_file(args.prefix_file)

    for as_number in as_numbers:
        tmp_prefixlist = []
        for line in args.prefix_file:
            list = line.split()
            ip = list[0]
            prefix_length = list[1]
            asn = list[2]

            if as_number == asn:
                tmp_prefixlist.append(line)
        
        ip = generate_hitlist_per_as(tmp_prefixlist, args.ip_address_file)
        print(f"{as_number=}")
        print(f"{ip=}")
        hitlist.append(ip)
        tuple_list.append(as_number, ip)

    with open(args.filtered_hitlist, "a") as file:
        file.write(hitlist)

if __name__ == "__main__":
    main()
