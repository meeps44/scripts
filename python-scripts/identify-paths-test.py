import argparse, json, os, hashlib

# lists the unique paths to a destination and the hop number they diverged (if they diverged)
# example usage: python3 identify-paths-test.py -d=/home/erlend/python-programming/smalljsondata

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
path_id_list_of_lists = [] # list of lists where each list contains all path_ids for one destiantion
hop_list_of_lists = []

def create_tag(destination_ip):
    # the tag is always a 6-digit hexadecimal number
    tag = hashlib.md5(destination_ip.encode()).hexdigest()[:6]
    return tag

def create_flow_label_list():
    flow_label_list = []
    if args.directory:
        try:
            for file in directory_contents:
                if (os.path.isfile(os.path.join(args.directory, file))):
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        print(len(data))
                        for item in data:
                            flow_label_list.append(item['flow_label'])
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
    dest_dict = {}
    if args.directory:
        try:
            for file in directory_contents:
                if (os.path.isfile(os.path.join(args.directory, file))):
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        for item in data:
                            dest_dict[item['destination']] = [] # create a key for every destination ip
                            number_of_hops = len(item['hops'])
                        #print(f"Number of hops to destination {data['destination']}: {number_of_hops}")
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)
    return dest_dict

def create_source_ip_list():
    src_list = []
    if args.directory:
        try:
            for file in directory_contents:
                if (os.path.isfile(os.path.join(args.directory, file))):
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        for item in data:
                            src_list.append(item['source'])
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)
    # get unique vales
    set_list = set(src_list)
    unique_list = list(set_list)
    return unique_list

# compares two lists and returns the index where they diverged (if they diverged)
def compare_lists(list1, list2):
    for index, item in enumerate(list1):
        try:
            if item != list2[index]:
                return index
        except IndexError:
            print("IndexError: index out of range")
            #print(f"The lists diverged at {index=}")
            return index
    #print("The lists are equal")
    return None

def compare_list_of_lists(list1):
    divergence_list = []
    for index, item in enumerate(list1): # for each hop-list
        try:
            #print(f"Comparing list{index} and list{index+1}")
            tmp = compare_lists(item, list1[index+1])
            if tmp != None:
                divergence_list.append(tmp)
        except IndexError:
            #print(f"Index {index+1} out of range")
            return divergence_list
    #print(f"{divergence_list=}")
    return divergence_list

# checks if a list of path_ids all contain the same path_id
# if yes, return true. else, return false
def paths_equal(pathid_list):
    result = all(element == pathid_list[0] for element in pathid_list)
    return result

def get_unique(input_list):
    set_list = set(input_list)
    unique_list = list(set_list)
    return unique_list

def main():
    flow_label_list = create_flow_label_list()
    src_ip_list = create_source_ip_list()
    print(f"{flow_label_list=}")
    print(f"{src_ip_list=}")

    for source in src_ip_list:
        for flow_label in flow_label_list:
            nmbr_scanned = 0
            test_dict = build_dictionary()
            #print(f"test_dict length: {len(test_dict)}")
            divergence_dictionary = {}
            for file in directory_contents:
                if (os.path.isfile(os.path.join(args.directory, file))):
                    filename = str(file)
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        for item in data:
                            file_flow_label = item['flow_label']
                            source_ip = item['source']
                            destination_ip = item['destination']
                            path_id = item['path_id']
                            if destination_ip in test_dict and file_flow_label == flow_label and source_ip == source:
                                test_dict[destination_ip].append(path_id)
            
            print("Print order:")
            print(f"Source destination flow_label Number_of_unique_paths_to_destination Hop_number_where_paths_diverged")
            for key in test_dict:
                if len(test_dict[key]) == 1:
                    #print(f"Number of paths from {source=} to destination {key} with {flow_label=}: {len(test_dict[key])}")
                    #print(f"Source {source} destination {key} flow_label {flow_label} Number_of_unique_paths_to_destination {len(get_unique(test_dict[key]))} Hop_number_where_paths_diverged 0")
                    print(f"{source} {key} {flow_label} {len(get_unique(test_dict[key]))} 0")
                if len(test_dict[key]) > 1:
                    divergence_dictionary[key] = []

            #print(f"{divergence_dictionary=}")
            
            for key in divergence_dictionary:
                # Check if paths diverged before doing the rest
                hop_list_of_lists = []
                path_id_list = [] # list of path ids to destination "key"
                for file in directory_contents:
                    if (os.path.isfile(os.path.join(args.directory, file))):
                        with open(os.path.join(args.directory, file), 'r') as file:
                            data = json.load(file)
                            for item in data:
                                file_flow_label = item['flow_label']
                                source_ip = item['source']
                                destination_ip = item['destination']
                                if destination_ip == key and file_flow_label == flow_label and source_ip == source:
                                    path_id_list.append(item['path_id'])
                                    path = list(item['hops'].values())
                                    new_list = []
                                    new_list.append(item['ipv6_address'])
                            #hop_list_of_lists.append(path)
                            hop_list_of_lists.append(new_list)
                divergence_dictionary[key] = path_id_list
                if len(divergence_dictionary[key]) == 1:
                    #print(f"Source {source} destination {key} flow_label {flow_label} Number_of_unique_paths_to_destination {len(get_unique(divergence_dictionary[key]))} Hop_number_where_paths_diverged 0")
                    print(f"{source} {key} {flow_label} {len(get_unique(divergence_dictionary[key]))} 0")
                if len(divergence_dictionary[key]) > 1:
                    tmp = compare_list_of_lists(hop_list_of_lists)
                    div_list = []
                    for item in tmp:
                        div_list.append(item+1) # to correct mismatch between hop number and list index, we increment by 1
                    if div_list:
                        #print(f"Source {source} destination {key} flow_label {flow_label} Number_of_unique_paths_to_destination {len(get_unique(divergence_dictionary[key]))} Hop_number_where_paths_diverged {div_list}")
                        print(f"{source} {key} {flow_label} {len(get_unique(divergence_dictionary[key]))} {div_list}")
                        #print(f"List of hop numbers where the paths diverged: {div_list}")

if __name__ == "__main__":
    main()
