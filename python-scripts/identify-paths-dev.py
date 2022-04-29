import argparse, json, os, hashlib
# lists the unique paths to a destination
# example usage: python3 identify-paths-dev.py -d=/home/erlend/python-programming/smalljsondata

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

# create and return a list of all path_ids to destination ip_addr with flow label flow_label
#def create_pathid_list(destination_tag, flow_label):
    #path_list = [] # list of list of ip-addresses in a path

    #path_id_list = [] # list of path ids
    #for file in directory_contents:
        #if (os.path.isfile(os.path.join(args.directory, file))):
            #filename = str(file)
            #if destination_tag in filename:
                #with open(os.path.join(args.directory, file), 'r') as file:
                    #data = json.load(file)
                    #file_flow_label = data['flow_label']
                    #if file_flow_label == flow_label:
                        #path_id_list.append(data['path_id'])

                        #path = data['hops'].values()
                        #path_list.append(path)
                        #hop_list_of_lists.append(path_list)
                        ##outgoing_port = data['outgoing_tcp_port']
    #return path_id_list

#def create_hoplists(destination_tag, flow_label):
    #hoplist = [] # list of list of ip-addresses in a path
    #list_of_hoplists = []

    #for file in directory_contents:
        #if (os.path.isfile(os.path.join(args.directory, file))):
            #filename = str(file)
            #if destination_tag in filename:
                #with open(os.path.join(args.directory, file), 'r') as file:
                    #data = json.load(file)
                    #file_flow_label = data['flow_label']
                    #if file_flow_label == flow_label:
                        #path = data['hops'].values()
                        #hoplist.append(path)
                        #list_of_hoplists.append(hoplist)
    #return list_of_hoplists


# compares all paths in the path list to destination ip_addr (alternatively: use tag) 
# and returns a list of the hop numbers where a path divergence was detected
#def create_path_divergence_list(path_list):
    #divergence_list = []
    #for pl_index, hoplist in enumerate(path_list): # for each hop-list
        #for hl_index, ip_address in enumerate(hoplist):
            #try:
                #if ip_address != hoplist[pl_index+1][hl_index]:
                    #divergence_list.append(hl_index)
                    #break
                ##if ip_address == hoplist[pl_index+1][hl_index]:
                    ##print(f"{ip_address} and {hoplist[pl_index+1][hl_index]} are equal")
                ##else:
                    ##divergence_list.append(hl_index)
                    ##break
            #except IndexError:
                #print("index out of range")
                #break
    #return divergence_list

## compares two lists and prints the index where they diverged (if they diverged)
#def compare_lists(list1, list2):
    #for index, item in enumerate(list1):
        #try:
            #if item != list2[index]:
                #print(f"The lists diverged at {index=}")
                #return False
        #except IndexError:
            #print("IndexError: index out of range")
            #print(f"The lists diverged at {index=}")
            #return False
    #print("The lists are equal")
    #return True

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
                    with open(os.path.join(args.directory, file), 'r') as file:
                        data = json.load(file)
                        dest_dict[data['destination']] = [] # create a key for every destination ip

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
    # get unique vales
    set_list = set(src_list)
    unique_list = list(set_list)
    return unique_list

# compares two lists and returns the index where they diverged (if they diverged)
def compare_lists(list1, list2):
    for index, item in enumerate(list1):
        try:
            #if item == list2[index]:
                #print(f"{item} and {list2[index]} are equal")
            #else:
                #print(f"list1 item: {item} \nlist2 item: {list2[index]}")
                #print(f"The lists diverged at {index=}")
                #return index
            if item != list2[index]:
                #print(f"list1 item: {item} \nlist2 item: {list2[index]}")
                #print(f"The lists diverged at {index=}")
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
def paths_diverged(pathid_list):
    result = all(element == pathid_list[0] for element in pathid_list)
    return result

def main():
    flow_label_list = create_flow_label_list()
    src_ip_list = create_source_ip_list()
    print(f"{flow_label_list=}")
    print(f"{src_ip_list=}")

    # TEST 3 #
    #test_dict = build_dictionary()
    #print(f"test_dict length: {len(test_dict)}")
    #for source in src_ip_list:
        #for flow_label in flow_label_list:
            #for key in test_dict:
                #hop_list_of_lists = []
                #path_id_list = [] # list of path ids to destination "key"
                #for file in directory_contents:
                    #if (os.path.isfile(os.path.join(args.directory, file))):
                        #filename = str(file)
                        #with open(os.path.join(args.directory, file), 'r') as file:
                            #data = json.load(file)
                            #file_flow_label = data['flow_label']
                            #source_ip = data['source']
                            #if create_tag(key) in filename and file_flow_label == flow_label and source_ip == source:
                                #path_id_list.append(data['path_id'])
                                #path = list(data['hops'].values())
                                ##path = data['hops'].values()
                                #new_list = []
                                #for item in path:
                                    #new_list.append(item['ipv6_address'])
                                ##hop_list_of_lists.append(path)
                                #hop_list_of_lists.append(new_list)
                #test_dict[key] = path_id_list
                #if len(test_dict[key]) > 0:
                    ##print(f"{test_dict[key]=}")
                    #print(f"Number of paths from {source=} to destination {key} with {flow_label=}: {len(test_dict[key])}")
                #if len(test_dict[key]) > 1:
                    #tmp = compare_list_of_lists(hop_list_of_lists)
                    #div_list = []
                    ## to correct mismatch between hop number and list index, we increment by 1
                    #for item in tmp:
                        #div_list.append(item+1)
                    ## to make 
                    #if div_list:
                        #print(f"List of hop numbers where the paths diverged: {div_list}")
                    #else:
                        ##print(f"{hop_list_of_lists=}")
                        #print("The paths did not diverge")
    # END TEST 3 #


    # TEST 4 #
    #test_dict = build_dictionary()
    #print(f"test_dict length: {len(test_dict)}")
    #for source in src_ip_list:
        #for flow_label in flow_label_list:
            #divergence_dictionary = {}
            #for file in directory_contents:
                #if (os.path.isfile(os.path.join(args.directory, file))):
                    #filename = str(file)
                    #with open(os.path.join(args.directory, file), 'r') as file:
                        #data = json.load(file)
                        #file_flow_label = data['flow_label']
                        #source_ip = data['source']
                        #destination_ip = data['destination']
                        #path_id = data['path_id']
                        #if destination_ip in test_dict and file_flow_label == flow_label and source_ip == source:
                            #test_dict[destination_ip].append(path_id)
            
            #for key in test_dict:
                #if len(test_dict[key]) > 0:
                    ##print(f"{test_dict[key]=}")
                    #print(f"Number of paths from {source=} to destination {key} with {flow_label=}: {len(test_dict[key])}")
                #if len(test_dict[key]) > 1:
                    #divergence_dictionary[key] = []

                    #path_id_list = []
                    #for file in directory_contents:
                        #filename = str(file)
                        #if create_tag(key) in filename:
                            #if (os.path.isfile(os.path.join(args.directory, file))):
                                #with open(os.path.join(args.directory, file), 'r') as file:
                                    #data = json.load(file)
                                    #file_flow_label = data['flow_label']
                                    #source_ip = data['source']
                                    #if file_flow_label == flow_label and source_ip == source:
                                        #path_id_list.append(data['path_id'])
                                        #path = list(data['hops'].values())
                                        ##path = data['hops'].values()
                                        #new_list = []
                                        #for item in path:
                                            #new_list.append(item['ipv6_address'])
                                        ##hop_list_of_lists.append(path)
                                        #hop_list_of_lists.append(new_list)
                    #tmp = compare_list_of_lists(hop_list_of_lists)
                    #div_list = []
                    ## to correct mismatch between hop number and list index, we increment by 1
                    #for item in tmp:
                        #div_list.append(item+1)
                    ## to make 
                    #if div_list:
                        #print(f"List of hop numbers where the paths diverged: {div_list}")
                    #else:
                        ##print(f"{hop_list_of_lists=}")
                        #print("The paths did not diverge")

    # END TEST 4 #

    # TEST 5 #
    #test_dict = build_dictionary()
    #print(f"test_dict length: {len(test_dict)}")
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
                        nmbr_scanned = nmbr_scanned + 1
                        data = json.load(file)
                        file_flow_label = data['flow_label']
                        source_ip = data['source']
                        destination_ip = data['destination']
                        path_id = data['path_id']
                        if destination_ip in test_dict and file_flow_label == flow_label and source_ip == source:
                            test_dict[destination_ip].append(path_id)
            
            print(f"Scanned {nmbr_scanned=} of documents")
            #print(f"{test_dict=}")
            
            for key in test_dict:
                if len(test_dict[key]) == 1:
                    #print(f"{test_dict[key]=}")
                    print(f"Number of paths from {source=} to destination {key} with {flow_label=}: {len(test_dict[key])}")
                if len(test_dict[key]) > 1:
                    divergence_dictionary[key] = []

            #print(f"{divergence_dictionary=}")
            
            for key in divergence_dictionary:

                # NEW: Checks if paths diverged before doing the rest
                if not paths_diverged(divergence_dictionary[key]):
                    hop_list_of_lists = []
                    path_id_list = [] # list of path ids to destination "key"
                    for file in directory_contents:
                        if (os.path.isfile(os.path.join(args.directory, file))):
                            filename = str(file)
                            with open(os.path.join(args.directory, file), 'r') as file:
                                data = json.load(file)
                                file_flow_label = data['flow_label']
                                source_ip = data['source']
                                if create_tag(key) in filename and file_flow_label == flow_label and source_ip == source:
                                    path_id_list.append(data['path_id'])
                                    path = list(data['hops'].values())
                                    #path = data['hops'].values()
                                    new_list = []
                                    for item in path:
                                        new_list.append(item['ipv6_address'])
                                    #hop_list_of_lists.append(path)
                                    hop_list_of_lists.append(new_list)
                    divergence_dictionary[key] = path_id_list
                    if len(divergence_dictionary[key]) > 0:
                        #print(f"{test_dict[key]=}")
                        print(f"Number of paths from {source=} to destination {key} with {flow_label=}: {len(divergence_dictionary[key])}")
                    if len(divergence_dictionary[key]) > 1:
                        tmp = compare_list_of_lists(hop_list_of_lists)
                        div_list = []
                        # to correct mismatch between hop number and list index, we increment by 1
                        for item in tmp:
                            div_list.append(item+1)
                        if div_list:
                            print(f"List of hop numbers where the paths diverged: {div_list}")
                        else:
                            print("The paths did not diverge")
    # END TEST 5 #

if __name__ == "__main__":
    main()
