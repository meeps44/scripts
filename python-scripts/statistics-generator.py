import argparse, json, logging, os, re

# function to count the number of paths with a particular flow-label
def count_path(pathlist):
    counter = 0
    for item in pathlist:
        print("do something")
    return counter

# get unique list values
def unique(my_list):
    list_set = set(my_list)
    unique_list = list(list_set)
    return unique_list

# get unique list-of-lists values
def unique_list_of_lists(my_list):
    unique_list = my_list.copy()
    for item in my_list:
        eq_counter = 0
        for obj in unique_list:
            if item == obj:
                eq_counter = eq_counter + 1
                if eq_counter > 1:
                    unique_list.remove(item) # removes the first object in the list matching "item"
                    eq_counter = eq_counter - 1
    #print(f"Unique list: {unique_list}")
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

scan_counter = 0
destinations = [] # list of all destination IPs found
flow_labels = [] # list of all source flow-labels found
paths = [] # list of lists containing all paths found
unique_paths = [] # subset of list paths, containing only the unique paths
path_and_flow_label_list = [] # list of all paths and their corresponding flow-labels. each 
# entry is saved as a tuple of the two.
path_counter = 0 # total number of paths found
unique_path_counter = 0 # number of unique paths found
flow_label_counter = 0 # number of unique flow-labels found

tags = p.findall(args.file)
tag = tags[0] # we are assuming that the filename will not contain more than one tag, 
# and that the directory will only contain certain kinds of logfiles specific to this project
print(f"Tag: {tag}")
print(f"Input Directory: {os.path.dirname(args.file)}")

# open all files in a directory
for filename in os.listdir(os.path.dirname(args.file)):
    # only open filenames containing the tag
    if tag in filename:
        with open(os.path.join(os.path.dirname(args.file), filename), "r") as file:
            scan_counter = scan_counter + 1
            elements = []
            ip_addresses = []
            # returns JSON object as a dictionary
            data = json.load(file)
            source_ip = data['source']
            destinations.append(data['destination'])
            tcp_port = data['outgoing_tcp_port']
            flow_labels.append(data['flow_label'])
            #returned_flow_label_1 = data1['hops']

            for key, value in data['hops'].items():
                elements.append(value)
                ip_addresses.append(data['hops'][key]['ipv6_address'])
            
            my_tuple = (data['flow_label'], ip_addresses)
            path_and_flow_label_list.append(my_tuple)
            #print(elements)
            #print(ip_addresses)
            paths.append(ip_addresses)

print(f"Scanned {scan_counter} traceroute-logs to destination {destinations[0]}")
path_counter = len(paths)
print(f"Total number of paths discovered: {path_counter}")
unique_paths = unique_list_of_lists(paths)
unique_path_counter = len(unique_paths)
print(f"Number of unique paths discovered: {unique_path_counter}")
#print(f"List of source flow-labels discovered: {flow_labels}")
print(f"Number of unique source flow-labels discovered: {len(unique(flow_labels))}")

for number, unique_path in enumerate(unique_paths):
    path_counter = 0
    for path in paths:
        if unique_path == path:
            path_counter = path_counter + 1
    print(f"Number of traceroutes to path number {number} (any flow-label): {path_counter}")
    print(f"Ratio: {(path_counter / len(paths)) * 100}%")
    #print(f"Traceroutes to path number {number} to total number of unique paths ratio: {path_counter / unique_path_counter}")

# tuple composition: item[0]: flow-label, item[1]: list of ip-addresses
for flow_label in unique(flow_labels):
    for index, unique_path in enumerate(unique_paths):
        path_counter = 0
        for pf_tuple in path_and_flow_label_list:
            if (unique_path == pf_tuple[1]) and (flow_label == pf_tuple[0]):
                path_counter = path_counter + 1
        print(f"Number of traceroutes with source flow-label {flow_label} to path number {index}: {path_counter}")