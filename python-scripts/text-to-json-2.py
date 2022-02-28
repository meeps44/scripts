import json, uuid, argparse, datetime, os, re, ipaddress

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
reg = r"((([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+\n(([0-9a-fA-F]+) )+([0-9a-fA-F]+))+"
pattern = re.compile(reg)

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
    
    # create and populate list of returned flow-labels as a (ipv6-address, returned_flow_label) tuple
    flow_labels = ["".join(x) for x in re.findall(pattern, data)]
    for index, item in enumerate(flow_labels):
        size = len(flow_labels[index])
        #print(a[index][:size - 37])
        flow_labels[index] = flow_labels[index][:size - 37]
        #print(f"Index:\t{index}")
        #print(a[index])

        # get the destination address, flow label tuple from the output
        #tuple = (a[index][151:158].replace(" ", ""), (a[index][24:72].replace(" ", "")).replace("\n", ""))

        ip = (flow_labels[index][24:72].replace(" ", "")).replace("\n", "")

        ipv6_addr = ipaddress.ip_address(int(ip, 16))
        #print(ipv6_addr)

        tuple = (str(ipv6_addr), flow_labels[index][151:158].replace(" ", ""))
        #print("Tuple:")
        #print(tuple)
        flow_label_list.append(tuple)
    
    # remove duplicate items from flow_label_list
    flow_label_list = list(dict.fromkeys(flow_label_list))

    #result = re.findall(IPV6ADDR, data)
    #print(result)

    # create hop-list (list of ipv6_addresses in path)
    #hop_list = my_file.read().splitlines() 
    hop_list = re.findall(IPV6ADDR, data) 
    # remove duplicates
    hop_list = list( dict.fromkeys(hop_list) )
    # Remove first item in the list (the destination address) and add it as separate dictionary element
    dest = hop_list.pop(0)

    #print("Hop list:")
    #print(hop_list)

    # Create top-level dictionary
    my_dict = {}
    #my_dict["probe_uuid"] = str(uuid.uuid4())

    my_dict["outgoing_tcp_port"] = args.tcp_port
    my_dict["flow_label"] = args.flow_label
    my_dict["timestamp"] = str(datetime.datetime.now())
    my_dict["source"] = args.source_ip
    my_dict["destination"] = dest

    count = 0 # in case items is empty and you need it after the loop
    #hop_dictionary = { index : item for index, item in enumerate(hop_list, start=1) }
    #hop_dictionary = { index : {address : flow_label_list[index][1]} for index, address in enumerate(hop_list, start=1) if (address == flow_label_list[0][0])}

    # Initialize hop dictionary
    hop_dictionary = { index : {"ipv6_address" : address, "returned_flow_label" : "null"} for index, address in enumerate(hop_list, start=1)}

    index = 0
    for item in hop_list:
        if hop_dictionary[index+1]["ipv6_address"] == item:
            hop_dictionary[index+1]["returned_flow_label"] = int(flow_label_list[index][1], 16)
        index = index + 1

    #print("Hop dictionary:")
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