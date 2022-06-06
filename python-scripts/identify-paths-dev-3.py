import argparse, json, os, hashlib
# Lists the unique paths to a destination
# Example usage: python3 identify-paths-dev.py -d=/home/erlend/python-programming/smalljsondata

default_dir = os.getcwd()
# Initialize argument parsing
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
    tag = hashlib.md5(destination_ip.encode()).hexdigest()[:8]
    return tag

def create_flow_label_list():
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
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        # Create a key for every destination ip
                        dest_dict[data['destination']] = {
                            "path_id": [],
                            "asn": [] 
                        } 

                        number_of_hops = len(data['hops'])
                        number_of_files_scanned = number_of_files_scanned + 1
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
                        src_list.append(data['source'])
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)
    set_list = set(src_list)
    unique_list = list(set_list)
    return unique_list

# Compares two lists and returns the index where they diverged (if they diverged)
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
            tmp = compare_lists(item, list1[index+1])
            if tmp != None:
                divergence_list.append(tmp)
        except IndexError:
            return divergence_list
    return divergence_list

# Checks if a list of path_ids all contain the same path_id
# If yes, return True.
def paths_equal(pathid_list):
    result = all(element == pathid_list[0] for element in pathid_list)
    return result

def get_unique(input_list):
    #set_list = set(input_list)
    #unique_list = list(set_list)
    unique_list = list()
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

def print_legend():
    print(f"Source \
        Destination \
        Flow_label \
        Number_of_unique_paths_to_destination \
        Hop_number_where_paths_diverged \
        List_of_unique_ASes_traversed \
        Number_of_unique_ASes_traversed\
        ")

def print_info(source_ip, dest_ip, flowlabel, number_of_unique_paths_to_destination, hop_number_where_paths_diverged, list_of_unique_ASes_traversed, number_of_unique_ASes_traversed):
    print(f"{source_ip} {dest_ip} {flowlabel} {number_of_unique_paths_to_destination} {hop_number_where_paths_diverged} {list_of_unique_ASes_traversed} {number_of_unique_ASes_traversed}", end=" ")


def main():
    flow_label_list = create_flow_label_list()
    src_ip_list = create_source_ip_list()
    print(f"{flow_label_list=}")
    print(f"{src_ip_list=}")
    asn_list = []

    print_legend()

    for source in src_ip_list:
        for flow_label in flow_label_list:
            nmbr_scanned = 0
            test_dict = build_dictionary()
            divergence_dictionary = {}
            for file in directory_contents:
                if (os.path.isfile(os.path.join(args.directory, file))):
                    filename = str(file)
                    with open(os.path.join(args.directory, file), 'r') as file:
                        nmbr_scanned = nmbr_scanned + 1
                        data = json.load(file)
                        file_flow_label = data['flow_label']
                        source_ip = data['source']
                        destination_ip = data['destination']
                        path_id = data['path_id']
                        source_asn = data['source_asn']
                        #as_hop_list = []
                        if destination_ip in test_dict and file_flow_label == flow_label and source_ip == source:
                            test_dict[destination_ip]['path_id'].append(path_id)
                            test_dict[destination_ip]['asn'].append(int(source_asn))
                            #as_hop_list.append(int(source_asn))

                            for value in data['hops']:
                                if data['hops'][value]['asn'] != "":
                                    test_dict[destination_ip]['asn'].append(int(data['hops'][value]['asn']))
                                    #as_hop_list.append(int(data['hops'][value]['asn']))
                            #test_dict[destination_ip]['asn'].append(as_hop_list)

            for destination_ip in test_dict:
                # If there is only one unique path found with flow label [f] to destination [d]:
                if len(get_unique(test_dict[destination_ip]['path_id'])) == 1:
                    print_info(source_ip=source, dest_ip=destination_ip, flowlabel=flow_label, number_of_unique_paths_to_destination=len(get_unique(test_dict[destination_ip]['path_id'])),
                     hop_number_where_paths_diverged=None, list_of_unique_ASes_traversed=get_unique(test_dict[destination_ip]['asn']), number_of_unique_ASes_traversed=len(get_unique(test_dict[destination_ip]['asn'])))
                    print("")
                
                # If there are multiple different paths found with flow label [f] to destination [d]: append them to the divergence dictionary:
                if len(get_unique(test_dict[destination_ip]['path_id'])) > 1:
                    divergence_dictionary[destination_ip] = {'path_id_list':[], 'asn_list':[]}

                    # Append each path to the divergence dictionary
                    for item in test_dict[destination_ip]['path_id']:
                        divergence_dictionary[destination_ip]['path_id_list'].append(item)

                    # Append each list of AS-hops to the divergence dictionary
                    for item in test_dict[destination_ip]['asn']:
                        divergence_dictionary[destination_ip]['asn_list'].append(item)
            
            # Scan the files again, figure out on which hop the paths diverged and print the result
            # To optimize, we calculate divergence hop number only for the destinations where a path divergence was detected 
            # (the number of unique paths found to destination [d] with flow label [f] is > 1)
            for destination_ip in divergence_dictionary:
                hop_list_of_lists = []
                path_id_list = [] # list of path ids to destination "destination_ip"
                for file in directory_contents:
                    if (os.path.isfile(os.path.join(args.directory, file))):
                        filename = str(file)
                        if create_tag(destination_ip) in filename:
                            with open(os.path.join(args.directory, file), 'r') as file:
                                data = json.load(file)
                                file_flow_label = data['flow_label']
                                source_ip = data['source']
                                if file_flow_label == flow_label and source_ip == source:
                                    path_id_list.append(data['path_id'])
                                    path = list(data['hops'].values())
                                    #path = data['hops'].values()
                                    new_list = []
                                    for item in path:
                                        new_list.append(item['ipv6_address'])
                                    #hop_list_of_lists.append(path)
                                    hop_list_of_lists.append(new_list)

                divergence_dictionary[destination_ip]['path_id_list'] = path_id_list
                tmp = compare_list_of_lists(hop_list_of_lists)
                div_list = []
                for item in tmp:
                    div_list.append(item+1) # To correct mismatch between hop number and list index, we increment by 1
                if div_list:
                    print_info(source_ip=source, dest_ip=destination_ip, flowlabel=flow_label, number_of_unique_paths_to_destination=len(get_unique(test_dict[destination_ip]['path_id'])),
                    hop_number_where_paths_diverged=div_list, list_of_unique_ASes_traversed=get_unique(test_dict[destination_ip]['asn']), number_of_unique_ASes_traversed=len(get_unique(test_dict[destination_ip]['asn'])))
                    print("")

                    # Print ASN where path diverged
                    #print(f"{div_list=}")
                    #for hopnumber in div_list:
                        #div_asn = list()
                        #for file in directory_contents:
                            #if (os.path.isfile(os.path.join(args.directory, file))):
                                #filename = str(file)
                                #if create_tag(destination_ip) in filename:
                                    #with open(os.path.join(args.directory, file), 'r') as file:
                                        #data = json.load(file)
                                        #file_flow_label = data['flow_label']
                                        #source_ip = data['source']
                                        #destination_ip = data['destination']
                                        #if file_flow_label == flow_label and source_ip == source:
                                            #try:
                                                #asn = data['hops'][str(hopnumber)]['asn']
                                                #div_asn.append(asn)
                                                ##print(f"{asn}", end=" ")
                                            #except KeyError:
                                                #print("Error: Skipped line")
                        #print(div_asn)
                        #print(get_unique(div_asn))

if __name__ == "__main__":
    main()
