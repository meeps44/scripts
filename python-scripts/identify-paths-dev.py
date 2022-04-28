import argparse, json, os, re, hashlib
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
def create_path_divergence_list(path_list):
    divergence_list = []
    for pl_index, hoplist in enumerate(path_list): # for each hop-list
        for hl_index, ip_address in enumerate(hoplist):
            try:
                if ip_address != hoplist[pl_index+1][hl_index]:
                    divergence_list.append(hl_index)
                    break
                #if ip_address == hoplist[pl_index+1][hl_index]:
                    #print(f"{ip_address} and {hoplist[pl_index+1][hl_index]} are equal")
                #else:
                    #divergence_list.append(hl_index)
                    #break
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
        except IndexError:
            print("IndexError: index out of range")
            print(f"The lists diverged at {index=}")
            return False
    print("The lists are equal")
    return True

def identify_tag(filename):
    tag = 0
    # the tag is always a 6-digit hexadecimal number
    return tag

def create_tag(destination_ip):
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


def main():
    flow_label_list = create_flow_label_list()
    src_ip_list = create_source_ip_list()
    print(f"{flow_label_list=}")
    print(f"{src_ip_list=}")

    # TEST 1 #
    #test_dict = build_dictionary()
    #print(f"test_dict length: {len(test_dict)}")
    #for key in test_dict:
        #path_id_list = [] # list of path ids to destination "key"
        #for file in directory_contents:
            #if (os.path.isfile(os.path.join(args.directory, file))):
                #filename = str(file)
                #with open(os.path.join(args.directory, file), 'r') as file:
                    #data = json.load(file)
                    #file_flow_label = data['flow_label']
                    #source_ip = data['source']
                    #if create_tag(key) in filename:
                        #path_id_list.append(data['path_id'])
        #test_dict[key] = path_id_list
        #print(f"{test_dict[key]=}")
    # END TEST 1 #

    # TEST 2 #
    #test_dict = build_dictionary()
    #print(f"test_dict length: {len(test_dict)}")
    #for source in src_ip_list:
        #for flow_label in flow_label_list:
            #for key in test_dict:
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
                                #div_list = create_path_divergence_list(some_hoplist)
                #test_dict[key] = path_id_list
                #if len(test_dict[key]) > 0:
                    ##print(f"{test_dict[key]=}")
                    #print(f"Number of paths from {source=} to destination {key} with {flow_label=}: {len(test_dict[key])}")
                #if len(test_dict[key]) > 1:
                    #print(f"List of hop numbers where the paths diverged: {div_list}")
    # END TEST 2 #

    # TEST 3 #
    test_dict = build_dictionary()
    print(f"test_dict length: {len(test_dict)}")
    for source in src_ip_list:
        for flow_label in flow_label_list:
            for key in test_dict:
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
                                hop_list_of_lists.append(path)
                test_dict[key] = path_id_list
                if len(test_dict[key]) > 0:
                    #print(f"{test_dict[key]=}")
                    print(f"Number of paths from {source=} to destination {key} with {flow_label=}: {len(test_dict[key])}")
                if len(test_dict[key]) > 1:
                    print(f"{hop_list_of_lists=}")
                    div_list = create_path_divergence_list(hop_list_of_lists)
                    print(f"List of hop numbers where the paths diverged: {div_list}")
    # END TEST 3 #

    for source in src_ip_list:
        for flow_label in flow_label_list:
            # create a new dictionary
            my_dict = build_dictionary()
            #for src_ip in src_ip_list:
            # create hoplists and path_id lists
            for key in my_dict:
                tag = create_tag(key)
                hoplist = [] # list of list of ip-addresses in a path
                list_of_hoplists = []
                path_id_list = [] # list of path ids to destination "key"
                list_of_pathid_lists = []
                for file in directory_contents:
                    if (os.path.isfile(os.path.join(args.directory, file))):
                        filename = str(file)
                        if tag in filename:
                            #print(f"Tag {tag} found in filename")
                            with open(os.path.join(args.directory, file), 'r') as file:
                                data = json.load(file)
                                file_flow_label = data['flow_label']
                                source_ip = data['source']
                                if file_flow_label == flow_label and source_ip == source:
                                    path_id_list.append(data['path_id'])
                                    path = data['hops'].values()
                                    hoplist.append(path)
                                    list_of_hoplists.append(hoplist)
                                    #print(f"{source_ip=}")
                                    #print(f"Destination ip = {key}")
                                    #print(f"{path_id_list=}")

                my_dict[key].append(path_id_list)

if __name__ == "__main__":
    main()