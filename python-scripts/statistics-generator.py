import argparse, json, logging, os, re

p = re.compile('[0-9a-f]{6}')

# initialize logging:
#logging.basicConfig(filename='/root/logs/route_comparison_output.log',
#format='%(asctime)s %(levelname)-8s %(message)s',
#level=logging.INFO,
#datefmt='%Y-%m-%d %H:%M:%S')

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument('-v', '-V', '--v', '--V', action='store_true') 
# if the -v flag is enabled, dump both routes to stdout
# action='store_true' implies default=False. Conversely, you could have action='store_false', which implies default=True.
args = parser.parse_args()


elements = []
ip_addresses = []
iteration = 0
number_of_paths = 0
number_of_flow_labels = 0
path_flow_set = {}

tag = str(p.findall(args.file))
print(f"Tag: {tag}")
print(f"Input Directory: {os.path.dirname(args.file)}")

# open all files in a directory
for filename in os.listdir(os.path.dirname(args.file)):
    # only open filenames containing the tag
    if tag in filename:
        print(f"Tag {tag} found in filename {filename}")
        #with open(args.file, "r") as file:
            ## returns JSON object as a dictionary
            #data = json.load(file)

            #source_ip = data['source']
            #destination_ip = data['destination']
            #tcp_port = data['outgoing_tcp_port']
            #flow_label = data['flow_label']
            ##returned_flow_label_1 = data1['hops']

            #for key, value in data['hops'].items():
                #elements.append(value)
                #ip_addresses.append(data['hops'][key]['ipv6_address'])
            
            #print(elements)
            #print(ip_addresses)

#with open(args.file, "r") as file:
    ## returns JSON object as a dictionary
    #data1 = json.load(file)

    #source_ip_1 = data1['source']
    #destination_ip_1 = data1['destination']
    #tcp_port_1 = data1['outgoing_tcp_port']
    #flow_label_1 = data1['flow_label']
    ##returned_flow_label_1 = data1['hops']

    #for key, value in data1['hops'].items():
        #elements.append(value)
        #ip_addresses.append(data1['hops'][key]['ipv6_address'])
    

    #print(elements)
    #print(ip_addresses)

#print(f"From {source_ip_1}")
#print(f"To {destination_ip_1}")
#print(f"Scanned {iteration} number of documents to destination {destination_ip_1}")
#print(f"Number of paths discovered: {number_of_paths}")
#print(f"Number of flow-labels used: {number_of_flow_labels}")

#for item in path_flow_set:
    #print(f"Number of traceroutes traversing path {path} with flow-label {flow_label}: {}")






        #try:
            #if (data1['hops'][key]['ipv6_address'] != data2['hops'][key]['ipv6_address']):
                #result = False
                #break
            #result = data1['hops'][key]['ipv6_address'] == data2['hops'][key]['ipv6_address']
        #except KeyError:
            #print("KeyError")
            #result = False
            #break