import argparse, json, logging

# initialize logging:
logging.basicConfig(filename='/root/logs/route_comparison_output.log',
format='%(asctime)s %(levelname)-8s %(message)s',
level=logging.INFO,
datefmt='%Y-%m-%d %H:%M:%S')


parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument('-v', '-V', '--v', '--V', action='store_true') 
# if the -v flag is enabled, dump both routes to stdout
# action='store_true' implies default=False. Conversely, you could have action='store_false', which implies default=True.
args = parser.parse_args()


with open(args.file, "r") as file:
    # returns JSON object as a dictionary
    data1 = json.load(file)

    source_ip_1 = data1['source']
    destination_ip_1 = data1['destination']
    tcp_port_1 = data1['outgoing_tcp_port']
    flow_label_1 = data1['flow_label']
    #returned_flow_label_1 = data1['hops']

    for key, value in data1['hops'].items():
        print(key, value)
        #try:
            #if (data1['hops'][key]['ipv6_address'] != data2['hops'][key]['ipv6_address']):
                #result = False
                #break
            #result = data1['hops'][key]['ipv6_address'] == data2['hops'][key]['ipv6_address']
        #except KeyError:
            #print("KeyError")
            #result = False
            #break