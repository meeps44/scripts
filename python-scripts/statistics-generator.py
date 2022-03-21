import argparse, json, logging, os, re

# function to get unique values
def unique(list1):
    # insert the list to the set
    list_set = set(frozenset(item) for item in list1)

    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list

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

iteration = 0
paths = [] # list of lists containing all paths found
path_counter = 0 # total number of paths found
unique_path_counter = 0 # number of unique paths found
flow_label_counter = 0 # number of unique flow-labels found
flow_labels = []

tags = p.findall(args.file)
tag = tags[0] # we are assuming that the filename will not contain more than one tag, 
# and that the directory will only contain certain kinds of logfiles specific to this project
print(f"Tag: {tag}")
print(f"Input Directory: {os.path.dirname(args.file)}")

# open all files in a directory
for filename in os.listdir(os.path.dirname(args.file)):
    # only open filenames containing the tag
    if tag in filename:
        print(f"Tag {tag} found in filename {filename}")
        with open(os.path.join(os.path.dirname(args.file), filename), "r") as file:
            elements = []
            ip_addresses = []
            # returns JSON object as a dictionary
            data = json.load(file)
            source_ip = data['source']
            destination_ip = data['destination']
            tcp_port = data['outgoing_tcp_port']
            flow_label = data['flow_label']
            #returned_flow_label_1 = data1['hops']

            flow_labels.append(flow_label)

            for key, value in data['hops'].items():
                elements.append(value)
                ip_addresses.append(data['hops'][key]['ipv6_address'])
            
            #print(elements)
            #print(ip_addresses)
            paths.append(ip_addresses)

print(f"All paths:\n{paths}")
path_counter = len(paths)
print(f"Total number of paths: {path_counter}")
unique_path_counter = len(unique(paths))
print(f"Number of unique paths discovered: {unique_path_counter}")
print(f"List of all flow-labels used: {flow_labels}")
print(f"Number of unique flow-labels used for sending packets: {len(unique(flow_labels))}")

print("Number of traceroutes to path {} with flow-label {}: {}")

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