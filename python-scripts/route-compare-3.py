import argparse, json, logging

# initialize logging:
logging.basicConfig(filename='/root/logs/comparison_output.log',
format='%(asctime)s %(levelname)-8s %(message)s',
level=logging.INFO,
datefmt='%Y-%m-%d %H:%M:%S')


# takes two json-files as input and compares the hop-list

parser = argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
parser.add_argument('-v', '-V', '--v', '--V', action='store_true') 
# if the -v flag is enabled, dump both routes to stdout
# action='store_true' implies default=False. Conversely, you could have action='store_false', which implies default=True.
args = parser.parse_args()


with open(args.file1, "r") as file1, open(args.file2, "r") as file2:
    # returns JSON object as a dictionary
    data1 = json.load(file1)
    data2 = json.load(file2)

    source_ip_1 = data1['source']
    destination_ip_1 = data1['destination']
    tcp_port_1 = data1['outgoing_tcp_port']
    flow_label_1 = data1['flow_label']
    #returned_flow_label_1 = data1['hops']

    source_ip_2 = data2['source']
    destination_ip_2 = data2['destination']
    tcp_port_2 = data2['outgoing_tcp_port']
    flow_label_2 = data2['flow_label']

    for key, value in data1['hops'].items():
        try:
            if (data1['hops'][key]['ipv6_address'] != data2['hops'][key]['ipv6_address']):
                result = False
                break
            result = data1['hops'][key]['ipv6_address'] == data2['hops'][key]['ipv6_address']
        except KeyError:
            print("KeyError")
            result = False
            break
    
    if (result):
        logging.info(f"\nCompared files {args.file1} and {args.file2}\n \
        {args.file1} info:\n \
        Source IP: {source_ip_1}\n \
        Destination IP: {destination_ip_1}\n \
        Flow label: {flow_label_1}\n \
        Outbound TCP port: {tcp_port_1}\n \
        {args.file2} info:\n \
        Source IP: {source_ip_2}\n \
        Destination IP: {destination_ip_2}\n \
        Flow label: {flow_label_2}\n \
        Outbound TCP port: {tcp_port_2}\n \
        Comparison result: The routes are equal.")
        print("The routes are equal")
        if (args.v):
            print("Route 1: ")
            for k, v in data2['hops'].items():
                print(f"{k}:{v}")
            print("Route 2: ")
            for k, v in data1['hops'].items():
                print(f"{k}:{v}")
    else:
        logging.info(f"\nCompared files {args.file1} and {args.file2}\n \
        {args.file1} info:\n \
        Source IP: {source_ip_1}\n \
        Destination IP: {destination_ip_1}\n \
        Flow label: {flow_label_1}\n \
        Outbound TCP port: {tcp_port_1}\n \
        {args.file2} info:\n \
        Source IP: {source_ip_2}\n \
        Destination IP: {destination_ip_2}\n \
        Flow label: {flow_label_2}\n \
        Outbound TCP port: {tcp_port_2}\n \
        Comparison result: The routes are NOT equal!")
        print("The routes are not equal")
        if (args.v):
            print("Route 1: ")
            for k, v in data2['hops'].items():
                print(f"{k}:{v}")
            print("Route 2: ")
            for k, v in data1['hops'].items():
                print(f"{k}:{v}")