import json, uuid, argparse, datetime, os, re, ipaddress, hashlib

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

#file = "/home/erlend/git/terraform-config/python-scripts/example-output/example-output-1.txt"
flow_label_list = []
# reg = r"((([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+([0-9a-fA-F]+))+"
reg = r"(((([0-9a-f]) ?){32})\n){6}"
pattern = re.compile(reg, re.MULTILINE)

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("hostname")
parser.add_argument("tcp_port")
parser.add_argument("source_ip")
parser.add_argument("flow_label")
args = parser.parse_args()

file = args.file

# file parsing starts here
with open(file, "r") as my_file:
    data = my_file.read()
    match = re.search(pattern, data)
    #print(match)
    #print(match.group())
    #print(re.split(pattern, data))

    ## create hop-list (list of ipv6_addresses in path)
    hop_list = re.findall(IPV6ADDR, data) 
    ## remove duplicates
    hop_list = list( dict.fromkeys(hop_list) )
    ## Remove first item in the list (the destination address) and add it as separate dictionary element
    dest = hop_list.pop(0)

    ## Initialize hop dictionary that only contains hops (used for generating path_id)
    tmp_hop_dictionary = { index : {"ipv6_address" : address} for index, address in enumerate(hop_list, start=1)}

    ## Create top-level dictionary
    my_dict = {}

    my_dict["outgoing_tcp_port"] = args.tcp_port
    my_dict["flow_label"] = args.flow_label
    my_dict["timestamp"] = str(datetime.datetime.now())
    my_dict["source"] = args.source_ip
    my_dict["destination"] = dest
    my_dict["path_id"] = hashlib.sha1(json.dumps(tmp_hop_dictionary, sort_keys=True).encode('utf-8')).hexdigest()

    #count = 0 # in case items is empty and you need it after the loop

    ## Initialize hop dictionary
    hop_dictionary = { index : {"ipv6_address" : address, "returned_flow_label" : "null"} for index, address in enumerate(hop_list, start=1)}

    #print("Hop dictionary before comparsion:")
    #print(hop_dictionary)
    #print("Hop list: ")
    #print(hop_list)

    # Find and append returned flow labels to the hop-dictionary
    for item in re.finditer(pattern, data):
        # print(item.group())
        ip = (item.group()[24:72].replace(" ", "")).replace("\n", "")
        ipv6_addr = ipaddress.ip_address(int(ip, 16))
        fl = item.group()[151:158].replace(" ", "")
        #print(ip)
        #print(fl)
        #tuple = (str(ipv6_addr), fl)
        #flow_label_list.append(tuple)

        for index, item in enumerate(hop_list):
            #print(item)
            #print(ipv6_addr)
            #print(int(fl, 16))
            if (str(item).replace(" ", "")).replace("\n", "") == (str(ipv6_addr).replace(" ", "")).replace("\n", ""):
                #print("hop_list item and ipv6_addr are equal")
                hop_dictionary[index+1]["returned_flow_label"] = int(fl, 16)

    #print("Hop dictionary after comparison: ")
    #print(hop_dictionary)
    
my_dict["hops"] = hop_dictionary
#print("Complete dictionary:")
#print(my_dict)

json_file = args.file
if json_file.endswith('.txt'):
    json_file = json_file[:-4]

json_file = json_file + ".json"

path = f'/root/logs/{args.hostname}/' + os.path.basename(json_file)

with open(path, 'w') as fp:
    json.dump(my_dict, fp, indent=4)
    print(f"File {path} successfully saved to disk")