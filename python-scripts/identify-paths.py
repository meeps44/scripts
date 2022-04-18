import argparse, json, os
# counts the number of unique paths to a destination

destinations = [] # list of all destination addresses searched
paths = [] # list of all paths
unique_paths = [] # subset of paths, list of all unique paths
number_of_files_scanned = 0

default_dir = os.getcwd()

# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-dir", "-d", const=default_dir, nargs='?', help="Directory containing json log files that you would like to run the flow-label check on")
parser.add_argument("--log", "-l", const='/root/logs/flowlabel_compare.log', nargs='?', help="Specify a logfile. Default = /root/logs/flowlabel_compare.log")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

# compares all paths to destination [ip_addr] (alternatively: use tag) 
# and prints out the hop number where a path divergence was detected
def get_path_div(ip_addr):
    hop_number = 0
    print(f"Path divergence discovered at hop number {hop_number}")
    # First get a list of all paths to destiantion ip_addr
    path_id_list = [] # list of path ids
    path_list = [] # list of list of ip-addresses in a path
    for file in os.listdir(args.directory):
        if (os.path.isfile(os.path.join(args.directory, file))):
            filename = str(file)
            with open(os.path.join(args.directory, file), 'r') as file:
                data = json.load(file)
                path_id_list.append(data['path_id'])
                path = data['hops'].values()
                path_list.append(path)

def main():
    if args.directory:
        try:
            for file in os.listdir(args.directory):
                if (os.path.isfile(os.path.join(args.directory, file))):
                    filename = str(file)
                    with open(os.path.join(args.directory, file), 'r') as file:
                        number_of_files_scanned = number_of_files_scanned + 1
                        data = json.load(file)
                        destinations.append(data['destination'])
                        paths.append(data['path_id'])

                        for key, value in data['hops'].items():
                            try:
                                if (data['hops'][key]['returned_flow_label'] != source_flow_label):
                                    flow_label_changed = True
                                    changed_counter = changed_counter + 1
                                    hop_number = key
                                    changed_location.append(hop_number)
                                    hop_ip = data['hops'][key]['ipv6_address'] 
                                    hop_flow_label = data['hops'][key]['returned_flow_label'] 
                                    hop_list.append((hop_number, hop_ip, hop_flow_label))

                            except KeyError:
                                print("KeyError")
                                exit(1)
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)

if __name__ == "__main__":
    main()
