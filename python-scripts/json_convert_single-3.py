from scapy.all import *
#from scapy.layers.inet import IP, ICMP
import json, datetime, os, re, ipaddress, hashlib, sys, SubnetTree, socket, argparse, subprocess, string

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
        # If the ip_address:asn-mapping is not found in the routeviews data, do a whois lookup:
        reverse_addr = ipaddress.ip_address(ip_address).reverse_pointer
        reverse_addr = reverse_addr[:len(reverse_addr) - 9] + ".origin6.asn.cymru.com."
        result = subprocess.run(["dig", "+short", reverse_addr, "TXT"], capture_output=True) # use DNS-based lookup for optimal performance
        stdout_as_str = result.stdout.decode("utf-8")

        my_str = ""
        for elem in stdout_as_str:
            if elem == "|":
                break
            if elem in string.digits:
                my_str = my_str + elem

        my_str = my_str.strip()
        my_list = my_str.split()
        list_to_string = ' '.join([str(elem) for elem in my_list])
        return list_to_string

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
    # END IPv6 REGEX

    # reg = r"((([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+([0-9a-fA-F]+))+"
    reg = r"(((([0-9a-f]) ?){32})\n){6}"
    pattern = re.compile(reg, re.MULTILINE)

    reg_1 = r"(?<=\<\n)(.|\n)*?(?=\n\>)" # Matches any block enclosed between < and >
    #reg_2 = r"IPv6 in ICMPv6 ]### \n        version   = 6\n        tc        = 0\n        fl        = [0-9]*"
    reg_3 = r"fl        = [0-9]*"
    reg_4 = r"[0-9]+"

    pattern_1 = re.compile(reg_1, re.MULTILINE)
    #pattern_2 = re.compile(reg_2, re.MULTILINE)
    pattern_3 = re.compile(reg_3, re.MULTILINE)
    pattern_4 = re.compile(reg_4, re.MULTILINE)
    


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

                # Initialize hop dictionary that only contains hops (used for generating path_id)
                tmp_hop_dictionary = { index : {"ipv6_address" : address} for index, address in enumerate(hop_list, start=1)}

                # Create top-level dictionary
                tl_dict = {}
                tl_dict["outgoing_tcp_port"] = tcp_port
                tl_dict["flow_label"] = flow_label
                tl_dict["timestamp"] = str(datetime.datetime.now())
                tl_dict["source"] = source_ip
                tl_dict["source_asn"] = get_asn(tree, source_ip)
                tl_dict["destination"] = dest
                tl_dict["destination_asn"] = get_asn(tree, dest)
                tl_dict["path_id"] = hashlib.sha1(json.dumps(tmp_hop_dictionary, sort_keys=True).encode('utf-8')).hexdigest()

                # Initialize hop dictionary
                hop_dictionary = { index : {"ipv6_address" : address, "asn" : "null", "returned_flow_label" : "null"} for index, address in enumerate(hop_list, start=1)}

                # Find and append returned flow labels to the hop-dictionary
                for raw_data in re.finditer(pattern_1, data):
                    ip = (raw_data.group()[24:72].replace(" ", "")).replace("\n", "") # Use regex to find response-IP. The response-IP will always be located at a certain offset in the IPv6-packet header.
                    ipv6_addr = ipaddress.ip_address(int(ip, 16))
                    # Use regex and Scapy to parse the raw hexdump and capture the returned flow-label contained in the ICMP payload
                    packet = raw_data.group()
                    index = 0
                    new_string = ""
                    for line in packet.splitlines():
                        index_nr = str(index).zfill(4)
                        line = f"{index_nr}   " + line + "\n"
                        new_string = new_string + line
                        index = index + 10

                    hex_dump = IPv6(import_hexcap(new_string))
                    packet_string = hex_dump.show(dump=True)
                    #print(packet_string)
                    fl = re.findall(r"IPv6 in ICMPv6 ]### \n        version   = 6\n        tc        = [0-9]*\n        fl        = [0-9]*", packet_string)
                    if fl:
                        fl = re.findall(pattern_3, fl[0])
                        fl = re.findall(pattern_4, fl[0])
                        fl = fl[0]
                    else:
                        fl = "null"
                    print(f"Flow label: {fl}")

                    for index, ip_address in enumerate(hop_list):
                        if (str(ip_address).replace(" ", "")).replace("\n", "") == (str(ipv6_addr).replace(" ", "")).replace("\n", ""):
                            hop_dictionary[index+1]["asn"] = get_asn(tree, ip_address)
                            if fl != "null":
                                hop_dictionary[index+1]["returned_flow_label"] = int(fl, 16)
                            else:
                                hop_dictionary[index+1]["returned_flow_label"] = "null"
                    
                tl_dict["hops"] = hop_dictionary

                

                #for item in re.finditer(pattern, data):
                    #ip = (item.group()[24:72].replace(" ", "")).replace("\n", "") # Use regex to find response-IP in txt file
                    #ipv6_addr = ipaddress.ip_address(int(ip, 16))
                    #fl = item.group()[151:158].replace(" ", "") # Use regex to capture the returned flow-label contained in the ICMP payload 

                    #for index, ip_address in enumerate(hop_list):
                        #if (str(ip_address).replace(" ", "")).replace("\n", "") == (str(ipv6_addr).replace(" ", "")).replace("\n", ""):
                            #hop_dictionary[index+1]["asn"] = get_asn(tree, ip_address)
                            #hop_dictionary[index+1]["returned_flow_label"] = int(fl, 16)
                    
                #tl_dict["hops"] = hop_dictionary

    except FileNotFoundError:
        print("Error: No such file or directory")
        exit(1)
    except NotADirectoryError:
        print("Error: Not a directory")
        print("Please use the --file option to compare single files. Use the -h argument for more info.")
        exit(1)

    return tl_dict

def create_filename(hostname, tag):
    now = datetime.datetime.now()
    date = now.strftime("%d-%m-%YT%H%M%SZ")
    #filename = f'/home/erlend/tmp/' + "convert-" + date + ".json"
    #filename = f'/root/logs/{hostname}/' + hostname + "-" + date + ".json"
    filename = f'/root/logs/{hostname}/' + os.path.basename(hostname) + tag + date + ".json"
    return filename

def fwrite(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"File {filename} successfully saved to disk")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("file")
    parser.add_argument("tcp_port")
    parser.add_argument("source_ip")
    parser.add_argument("tag")
    parser.add_argument("flow_label")
    args = parser.parse_args()

    hostname = str(socket.gethostname())

    json_data = create_dict(args.directory, args.file, args.tcp_port, args.source_ip, args.flow_label)
    print(json_data)
    #my_filename = create_filename(hostname, args.tag)
    #fwrite(json_data, my_filename)

if __name__ == "__main__":
    main()
