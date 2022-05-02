import argparse, json, os, hashlib

# Gets the number of hops between a source host to a destination node

default_dir = os.getcwd()
# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-dir", "-d", const=default_dir, nargs='?', help="Directory containing json log files that you would like to run the flow-label check on")
args = parser.parse_args()
directory_contents = os.listdir(args.directory)

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
def paths_diverged(pathid_list):
    result = all(element == pathid_list[0] for element in pathid_list)
    return result

def print_hopnumbers():
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
                        #print(f"Number of hops from source {data['source']} to destination {data['destination']}: {number_of_hops}")
                        print(f"Source: {data['source']} Destination: {data['destination']} Flowlabel: {data['flow_label']} Hopnumber: {number_of_hops}")
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)
    return number_of_files_scanned

def main():
    scanned = print_hopnumbers()
    print(f"Scanned {scanned} of documents")

if __name__ == "__main__":
	main()
