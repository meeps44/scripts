import argparse, json, os
# lists the unique paths to a destination
# example usage: python3 identify-paths-dev.py -d=/root/home/

default_dir = os.getcwd()
# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-dir", "-d", const=default_dir, nargs='?', help="Directory containing json log files that you would like to run the flow-label check on")
args = parser.parse_args()
directory_contents = os.listdir(args.directory)

destinations = [] # list of all destination addresses searched
paths = [] # list of all paths
unique_paths = [] # subset of paths, list of all unique paths
number_of_files_scanned = 0
path_id_list = [] # list of path ids
path_id_list_of_lists = [] # list of lists where each list contains all path_ids for one destiantion
path_list = [] # list of list of ip-addresses in a path

# creates a list of paths to destination ip_addr
def build_path_id_list(destination_tag):
    # First get a list of all path_ids to destiantion ip_addr
    for file in directory_contents:
        if (os.path.isfile(os.path.join(args.directory, file))):
            filename = str(file)
            if destination_tag in filename:
                with open(os.path.join(args.directory, file), 'r') as file:
                    data = json.load(file)
                    flow_label = data['flow_label']
                    #outgoing_port = data['outgoing_tcp_port']
                    path_id_list.append(data['path_id'])
                    path = data['hops'].values()
                    path_list.append(path)

# compares all paths to destination [ip_addr] (alternatively: use tag) 
# and returns a list of hop numbers where a path divergence was detected
# path_list is a list of lists containing IP-addresses
def discover_path_divergence(path_list):
    divergence_list = []
    hop_number = 0
    for pl_index, hoplist in enumerate(path_list): # for each hop-list
        for hl_index, ip_address in enumerate(hoplist):
            try:
                if ip_address == hoplist[pl_index+1][hl_index]:
                    print(f"{ip_address} and {hoplist[pl_index+1][hl_index]} are equal")
                else:
                    divergence_list.append(hl_index)
            except IndexError:
                print("index out of range")
                break
    return divergence_list

# compares two lists and prints the index where they diverged (if they diverged)
def compare_lists(list1, list2):
    for index, item in enumerate(list1):
        try:
            if item != list2[index]:
                print(f"The lists diverged at {index=}")
                return False
                #return index
            #if item == list2[index]:
                #print(f"{item} and {list2[index]} are equal")
            #else:
                #print(f"list1 item: {item} \nlist2 item: {list2[index]}")
                #print(f"The lists diverged at {index=}")
                #return index
        except IndexError:
            print("IndexError: index out of range")
            print(f"The lists diverged at {index=}")
            return False
            #return index
    print("The lists are equal")
    return True

def create_tag(destination_ip):
    tag = 0
    return tag

def build_flow_label_list():
    flow_label_list = []
    if args.directory:
        try:
            for file in directory_contents:
                if (os.path.isfile(os.path.join(args.directory, file))):
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        flow_label_list.append(data['flow_label'])
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)
    # get unique vales
    set_list = set(flow_label_list)
    unique_list = list(set_list)
    return unique_list

def build_dictionary():
    number_of_files_scanned = 0
    dest_dict = {}
    if args.directory:
        try:
            for file in directory_contents:
                if (os.path.isfile(os.path.join(args.directory, file))):
                    filename = str(file)
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        number_of_files_scanned = number_of_files_scanned + 1
                        number_of_hops = len(data['hops'])
                        dest_dict[data['destination']] = [] # create a key for every destination ip
                        tag = create_tag(data['destination'])
                        dest_dict[data['destination']].append(build_path_id_list(tag))
                        #dest_dict[data['destination']].append(data['path_id'])

                        destinations.append(data['destination'])
                        paths.append(data['path_id'])

                        print(f"Number of hops to destination {data['destination']}: {number_of_hops}")
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)
    return dest_dict


def main():
    destination = 0
    for flow_label in build_flow_label_list():
        my_dict = build_dictionary()
        print(f"Number of paths to {destination=} with {flow_label=}: {len(my_dict[destination])}")
        print(f"List of hop numbers where the paths to {destination=} with {flow_label=} diverged: ")
        # perform route comparison

if __name__ == "__main__":
    main()
