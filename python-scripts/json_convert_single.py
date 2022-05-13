import json, datetime, os, re, ipaddress, hashlib, sys, SubnetTree, socket, argparse, subprocess

def fill_subnettree(tree, rv_file):
    with open(rv_file, "r") as file:
        for line in file:
            line = line.strip()
            line = line.split()
            key = line[0] + "/" + line[1]
            try:
                tree[key] = line[2]
            except ValueError as e:
                print("Skipped line '" + line + "'", file=sys.stderr)
    return tree

#routeviews_file = "/root/git/scripts/text-files/routeviews-rv6-20220505-1200.pfx2as.txt"
routeviews_file = "/home/erlend/git/scripts/text-files/routeviews-rv6-20220505-1200.pfx2as.txt"
tree = SubnetTree.SubnetTree()
tree = fill_subnettree(tree, routeviews_file)

def get_asn(tree, ip_address):
    try:
        return tree[ip_address]
    except KeyError as e:
        #print(f"KeyError: {ip_address=} not found in subnettree", file=sys.stderr)
        # If they address is not found, do a whois lookup:
        # example: whois -h whois.cymru.com " -v 216.90.108.31 2005-12-25 13:23:01 GMT"
        result = subprocess.run(["whois", "-h", "whois.cymru.com", ip_address], capture_output=True)
        stdout_as_str = result.stdout.decode("utf-8")
        x = re.findall("AS Name\n[0-9]{1,5}", stdout_as_str)
        as_number = x[0][8:] 
        return as_number
        #return None

def create_dict(directory, filename, tcp_port, source_ip, flow_label):
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

    # reg = r"((([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+([0-9a-fA-F]+))+"
    reg = r"(((([0-9a-f]) ?){32})\n){6}"
    pattern = re.compile(reg, re.MULTILINE)

    # File parsing starts here
    try:
        if (os.path.isfile(os.path.join(directory, filename))):
            with open(os.path.join(directory, filename), "r") as f:
                data = f.read()
                match = re.search(pattern, data)

                # Create hop-list (list of ipv6_addresses in path)
                hop_list = re.findall(IPV6ADDR, data) 
                # Remove duplicates
                hop_list = list( dict.fromkeys(hop_list) )
                # Remove first item in the list (the destination address) and add it as separate dictionary element
                dest = hop_list.pop(0)

                ## Initialize hop dictionary that only contains hops (used for generating path_id)
                tmp_hop_dictionary = { index : {"ipv6_address" : address} for index, address in enumerate(hop_list, start=1)}

                ## Create top-level dictionary
                my_dict = {}
                my_dict["outgoing_tcp_port"] = tcp_port
                my_dict["flow_label"] = flow_label
                my_dict["timestamp"] = str(datetime.datetime.now())
                my_dict["source"] = source_ip
                my_dict["source_asn"] = get_asn(tree, source_ip)
                my_dict["destination"] = dest
                my_dict["destination_asn"] = get_asn(tree, dest)
                my_dict["path_id"] = hashlib.sha1(json.dumps(tmp_hop_dictionary, sort_keys=True).encode('utf-8')).hexdigest()

                ## Initialize hop dictionary
                hop_dictionary = { index : {"ipv6_address" : address, "asn" : "null", "returned_flow_label" : "null"} for index, address in enumerate(hop_list, start=1)}

                # Find and append returned flow labels to the hop-dictionary
                for item in re.finditer(pattern, data):
                    # print(item.group())
                    ip = (item.group()[24:72].replace(" ", "")).replace("\n", "") # use regex to find response-IP in txt file
                    ipv6_addr = ipaddress.ip_address(int(ip, 16))
                    fl = item.group()[151:158].replace(" ", "") # use regex to capture the returned flow-label contained in the ICMP payload. NB! will not work in the presence of IPv6 extension headers

                    for index, ip_address in enumerate(hop_list):
                        if (str(ip_address).replace(" ", "")).replace("\n", "") == (str(ipv6_addr).replace(" ", "")).replace("\n", ""):
                            hop_dictionary[index+1]["asn"] = get_asn(tree, ip_address)
                            hop_dictionary[index+1]["returned_flow_label"] = int(fl, 16)
                    
                my_dict["hops"] = hop_dictionary

    except FileNotFoundError:
        print("Error: No such file or directory")
        exit(1)
    except NotADirectoryError:
        print("Error: Not a directory")
        print("Please use the --file option to compare single files. Use the -h argument for more info.")
        exit(1)

    return my_dict

def create_filename(hostname):
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%YT%H%M%SZ")
    #filename = f'/home/erlend/tmp/' + "convert-" + date + ".json"
    #filename = f'/root/logs/{hostname}/' + hostname + "-" + date + ".json"
    filename = f'/root/logs/{hostname}/' + os.path.basename(hostname) + date + ".json"
    return filename

def fwrite(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"File {filename} successfully saved to disk")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("hostname")
    parser.add_argument("tcp_port")
    parser.add_argument("source_ip")
    parser.add_argument("flow_label")
    args = parser.parse_args()

    hostname = str(socket.gethostname())

    json_data = create_dict(args.directory, args.file, args.tcp_port, args.source_ip, args.flow_label)
    my_filename = create_filename(hostname)
    fwrite(json_data, my_filename)

if __name__ == "__main__":
    main()
