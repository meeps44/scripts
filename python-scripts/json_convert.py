import json, uuid, argparse, datetime, os, re, ipaddress, hashlib, sys, SubnetTree

# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("hostname")
parser.add_argument("tcp_port")
parser.add_argument("source_ip")
parser.add_argument("flow_label")
parser.add_argument("json_filename")
parser.add_argument("timestamp")
args = parser.parse_args()

def fill_tree(tree, fh):
    for line in fh:
        line = line.strip()
        try:
            tree[line] = line
        except ValueError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)
    return tree

def create_hashmap(rv_file):
    my_hashmap = {}
    with open(rv_file, "r") as file:
        data = file.readlines()
        # Create hashmap
        for line in data:
            line = line.strip()
            line = line.split()
            key = line[0] + "/" + line[1]
            my_hashmap[key] = line[2]
    return my_hashmap


def scan_dir(directory):
    json_list = []
    directory_content = os.listdir(directory)
    for file in directory_content:
        try:
            if (os.path.isfile(os.path.join(args.directory, file))):
                filename = str(file)
                with open(os.path.join(args.directory, file), "r") as file:
                    nmbr_scanned = nmbr_scanned + 1
                    file_data = file.read()
                    json_list.append(convert(file_data))
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)
    return json_list

def convert(data):
    # REGEX that matches IPv6-address. Credit: David M. Syzdek, https://gist.github.com/syzdek/6086792
    IPV4SEG  = r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
    IPV4ADDR = r'(?:(?:' + IPV4SEG + r'\.){3,3}' + IPV4SEG + r')'
    IPV6SEG  = r'(?:(?:[0-9a-fA-F]){1,4})'
    IPV6GROUPS = (
        r'(?:' + IPV6SEG + r':){7,7}' + IPV6SEG,                  # 1:2:3:4:5:6:7:8
        r'(?:' + IPV6SEG + r':){1,7}:',                           # 1::                                 1:2:3:4:5:6:7::
        r'(?:' + IPV6SEG + r':){1,6}:' + IPV6SEG,                 # 1::8               1:2:3:4:5:6::8   1:2:3:4:5:6::8
        r'(?:' + IPV6SEG + r':){1,5}(?::' + IPV6SEG + r'){1,2}',  # 1::7:8             1:2:3:4:5::7:8   1:2:3:4:5::8
        r'(?:' + IPV6SEG + r':){1,4}(?::' + IPV6SEG + r'){1,3}',  # 1::6:7:8           1:2:3:4::6:7:8   1:2:3:4::8
        r'(?:' + IPV6SEG + r':){1,3}(?::' + IPV6SEG + r'){1,4}',  # 1::5:6:7:8         1:2:3::5:6:7:8   1:2:3::8
        r'(?:' + IPV6SEG + r':){1,2}(?::' + IPV6SEG + r'){1,5}',  # 1::4:5:6:7:8       1:2::4:5:6:7:8   1:2::8
        IPV6SEG + r':(?:(?::' + IPV6SEG + r'){1,6})',             # 1::3:4:5:6:7:8     1::3:4:5:6:7:8   1::8
        r':(?:(?::' + IPV6SEG + r'){1,7}|:)',                     # ::2:3:4:5:6:7:8    ::2:3:4:5:6:7:8  ::8       ::
        r'fe80:(?::' + IPV6SEG + r'){0,4}%[0-9a-zA-Z]{1,}',       # fe80::7:8%eth0     fe80::7:8%1  (link-local IPv6 addresses with zone index)
        r'::(?:ffff(?::0{1,4}){0,1}:){0,1}[^\s:]' + IPV4ADDR,     # ::255.255.255.255  ::ffff:255.255.255.255  ::ffff:0:255.255.255.255 (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
        r'(?:' + IPV6SEG + r':){1,4}:[^\s:]' + IPV4ADDR,          # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
    )
    IPV6ADDR = '|'.join(['(?:{})'.format(g) for g in IPV6GROUPS[::-1]])  # Reverse rows for greedy match
    # END REGEX

    #file = "/home/erlend/git/terraform-config/python-scripts/example-output/example-output-1.txt"
    # reg = r"((([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+([0-9a-fA-F]+))+"
    reg = r"(((([0-9a-f]) ?){32})\n){6}"
    pattern = re.compile(reg, re.MULTILINE)

    # file parsing starts here
    match = re.search(pattern, data)

    # create hop-list (list of ipv6_addresses in path)
    hop_list = re.findall(IPV6ADDR, data) 
    # remove duplicates
    hop_list = list( dict.fromkeys(hop_list) )
    # Remove first item in the list (the destination address) and add it as separate dictionary element
    dest = hop_list.pop(0)

    ## Initialize hop dictionary that only contains hops (used for generating path_id)
    tmp_hop_dictionary = { index : {"ipv6_address" : address} for index, address in enumerate(hop_list, start=1)}

    ## Create top-level dictionary
    my_dict = {}

    my_dict["outgoing_tcp_port"] = args.tcp_port
    my_dict["flow_label"] = args.flow_label
    my_dict["timestamp"] = args.timestamp
    my_dict["source"] = args.source_ip
    my_dict["destination"] = dest
    my_dict["path_id"] = hashlib.sha1(json.dumps(tmp_hop_dictionary, sort_keys=True).encode('utf-8')).hexdigest()

    ## Initialize hop dictionary
    hop_dictionary = { index : {"ipv6_address" : address, "returned_flow_label" : "null", "asn" : "null"} for index, address in enumerate(hop_list, start=1)}

    # Find and append returned flow labels to the hop-dictionary
    for item in re.finditer(pattern, data):
        # print(item.group())
        ip = (item.group()[24:72].replace(" ", "")).replace("\n", "") # use regex to find response-IP in txt file
        ipv6_addr = ipaddress.ip_address(int(ip, 16))

        # check for ipv6 extension-headers (work in progress)
        # next_header_values = [] # list of all possible next-header values
        #ext = item.group()[151:158].replace(" ", "")
        # if ext not in next_header_values: 
        # print("Error: next-header value not recognised")
        # for value in next_header_values:
        # if ext == value:
        # jump some predetermined amount of bits depending on the type of next-header and repeat the process, until a value of 58 is reached.
        # 58 is the next-header value for ICMPv6, which is what we want.

        fl = item.group()[151:158].replace(" ", "") # use regex to capture the returned flow-label contained in the ICMP payload. NB! will not work in the presence of IPv6 extension headers

        for index, ip_address in enumerate(hop_list):
            if (str(ip_address).replace(" ", "")).replace("\n", "") == (str(ipv6_addr).replace(" ", "")).replace("\n", ""):
                hop_dictionary[index+1]["returned_flow_label"] = int(fl, 16)
                hop_dictionary[index+1]["asn"] = get_asn(ip_address)
        
    my_dict["hops"] = hop_dictionary
    return my_dict

def get_filename():
    filename = f'/root/logs/{args.hostname}/' + os.path.basename(args.json_filename) + ".json"
    return filename

def fwrite(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4)
        print(f"File {filename} successfully saved to disk")

# asnlookup
def get_asn(prefix, my_hashmap):
    try:
        return my_hashmap[prefix]
    except KeyError as e:
        print(f"KeyError: prefix {prefix} not found in hashmap", file=sys.stderr)
        return 0

def main():
    # Store aliased and non-aliased prefixes in a single subnet tree
    tree = SubnetTree.SubnetTree()

    # Read aliased and non-aliased prefixes
    tree = fill_tree(tree, args.aliased_file)
    my_hashmap = create_hashmap(args.routeviews_file)
    get_asn(tree["ip_address"], my_hashmap)

    json_data = scan_dir(args.directory)
    filename = get_filename()
    fwrite(json_data, filename)

if __name__ == "__main__":
    main()