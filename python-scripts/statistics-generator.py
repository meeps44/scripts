import argparse, json, logging, os, re

# function to count the number of paths with a particular flow-label
def count_path(pathlist):
    counter = 0
    for item in pathlist:
        print("do something")
    return counter


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

scan_counter = 0
destinations = []
paths = [] # list of lists containing all paths found
path_counter = 0 # total number of paths found
unique_path_counter = 0 # number of unique paths found
flow_label_counter = 0 # number of unique flow-labels found
flow_labels = []
path_and_flow_label_list = []

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

print(f"Scanned {scan_counter} traceroute documents to destination {destinations[0]}")
print(f"All paths:\n{paths}")
path_counter = len(paths)
print(f"Total number of paths: {path_counter}")
unique_path_counter = len(unique(paths))
print(f"Number of unique paths discovered: {unique_path_counter}")
print(f"List of all outgoing flow-labels used: {flow_labels}")
print(f"Number of unique outgoing flow-labels used: {len(unique(flow_labels))}")

print(f"Total number of tracerouts to path number {path}: {}")
print(f"Number of traceroutes to path number {path} with flow-label {}: {}")


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