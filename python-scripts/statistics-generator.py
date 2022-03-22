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
    print("Entering the unique_list_of_lists function")
    # convert list of lists to set of sets
    print(f"Original list: {my_list}")
    #(print(f"Original list item: {item}\n") for item in list1)

    unique_list = my_list
    for item in my_list:
        eq_counter = 0
        index = 0
        while index < len(my_list):
            if item == my_list[index]:
                eq_counter = eq_counter + 1
                if eq_counter > 1:
                    unique_list.pop(index)
                    eq_counter = eq_counter - 1
            index = index + 1
    print(f"Unique list: {unique_list}")
    return unique_list


    #list_set = set(frozenset(item) for item in my_list)

    ## convert set back to list
    #unique_list = list(list(item) for item in list_set)
    #print(f"Unique list: {unique_list}")
    #return unique_list

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
        #print(f"Tag {tag} found in filename {filename}")
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
#print(f"All paths:\n{paths}")
path_counter = len(paths)
print(f"Total number of paths discovered: {path_counter}")
unique_paths = unique_list_of_lists(paths)
unique_path_counter = len(unique_paths)
print(f"Number of unique paths discovered: {unique_path_counter}")
print(f"List of all outgoing flow-labels used: {flow_labels}")
print(f"Number of unique outgoing flow-labels used: {len(unique(flow_labels))}")

#print(path_and_flow_label_list)
#print(len(path_and_flow_label_list))

#for index, unique_path in enumerate(unique_paths):
#for path in paths:
    #path_counter = 0
    #for index, unique_path in enumerate(unique_paths):
        #print(f"Unique path: {unique_path}")
        #print(f"Path: {path}")
        #if path == unique_path:
            #path_counter = path_counter + 1
    #print(f"Number of traceroutes to path number {index}: {path_counter}")

for number, unique_path in enumerate(unique_paths):
    path_counter = 0
    index = 0

    for path in paths:
        if unique_path == path:
            path_counter = path_counter + 1
        #index = index + 1
    print(f"Number of traceroutes to path number {number}: {path_counter}")


    #while index < len(paths):
        #print(f"Unique path: {unique_path}")
        #print(f"Paths index {index}: {paths[index]}")
        #if unique_path == paths[index]:
            #path_counter = path_counter + 1
        #index = index + 1
    #print(f"Number of traceroutes to path number {number}: {path_counter}")

    #for path in paths:
        #print(f"Unique path: {unique_path}")
        #print(f"Path: {path}")
        #if unique_path == path:
            #path_counter = path_counter + 1
    #print(f"Number of traceroutes to path number {index}: {path_counter}")


# per flow-label
# tuple composition: item[0]: flow-label, item[1]: list of ip-addresses
for flow_label in unique(flow_labels):
    for index, unique_path in enumerate(unique_paths):
        path_counter = 0
        for pf_tuple in path_and_flow_label_list:
            if (unique_path == pf_tuple[1]) and (flow_label == pf_tuple[0]):
                path_counter = path_counter + 1
        print(f"Number of traceroutes with flow-label {flow_label} to path number {index}: {path_counter}")


# tuple composition: item[0]: flow-label, item[1]: list of ip-addresses
# for each path, do:
#for idx, item in path_and_flow_label_list:
    #path_counter = 0
    #path_and_flow_counter = 0
    #for index, object in enumerate(path_and_flow_label_list):
        ## if the paths are equal: increment path counter
        #if item[1] == path_and_flow_label_list[index][1]:
            #path_counter = path_counter + 1 
        #if item == path_and_flow_label_list[index]:
            #path_and_flow_counter = path_and_flow_counter + 1

    #print(f"Number of traceroutes to path number {idx} with flow-label {}: {}")
    



#class Path:
    #def __init__(self, ip_addresses, flow_label, path_number):
        #self.path = ip_addresses
        #self.flow_label = flow_label
        #self.path_number = path_number

    #def get_path(self):
        #return self.path
    
    #def get_path_length(self):
        #return len(self.path)

    #def get_flow_label(self):
        #return self.flow_label