import argparse, json, os
# counts the number of unique paths to a destination

destinations = [] # list of all destination addresses searched
paths = [] # list of all paths
unique_paths = [] # subset of paths, list of all unique paths
number_of_files_scanned = 0
path_id_list = [] # list of path ids
path_list = [] # list of list of ip-addresses in a path

default_dir = os.getcwd()

# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-dir", "-d", const=default_dir, nargs='?', help="Directory containing json log files that you would like to run the flow-label check on")
parser.add_argument("--log", "-l", const='/root/logs/flowlabel_compare.log', nargs='?', help="Specify a logfile. Default = /root/logs/flowlabel_compare.log")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

# creates a list of paths to destination ip_addr
def fill_path_list(tag):
    # First get a list of all paths to destiantion ip_addr
    for file in os.listdir(args.directory):
        if (os.path.isfile(os.path.join(args.directory, file))):
            filename = str(file)
            if tag in filename:
                with open(os.path.join(args.directory, file), 'r') as file:
                    data = json.load(file)
                    path_id_list.append(data['path_id'])
                    path = data['hops'].values()
                    path_list.append(path)

# compares all paths to destination [ip_addr] (alternatively: use tag) 
# and prints out a list of hop numbers where a path divergence was detected
# path_list is a list of lists containering hop addresses
def get_path_div(path_list):
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


    print(f"Path divergence discovered at hop number: {hop_number}")

# compares two lists and returns true if they are equal, false if they are not
def compare_list(list1, list2):
    for index, item in enumerate(list1):


def main():
    if args.directory:
        try:
            for file in os.listdir(args.directory):
                if (os.path.isfile(os.path.join(args.directory, file))):
                    filename = str(file)
                    with open(os.path.join(args.directory, file), 'r') as file:
                        number_of_files_scanned = number_of_files_scanned + 1
                        number_of_hops = len(data['hops'])
                        data = json.load(file)
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

if __name__ == "__main__":
    main()
