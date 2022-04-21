from enum import unique
from collections import defaultdict
import argparse, json, os, itertools

# Example usage: python3 ~/git/scripts/python-scripts/flowlabel-compare-2.py -d=/mnt/c/Users/Erlend/Downloads/Archived\ Logs/Stage\ 1/Small\ scale\ test/JsonFiles/

#hitlist_path = "/root/git/scripts/text-files/stage2_hitlist.txt"
hitlist_path = "/home/erlend/tmp/stage2_hitlist.txt"

default_dir = os.getcwd()

# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-dir", "-d", const=default_dir, nargs='?', help="Directory containing json log files that you would like to run the flow-label check on")
args = parser.parse_args()

path_id_list = []

changed_counter = 0
changed_location = [] # list of hop-numbers where a change in the flow-label was detected
unique_ip_addresses = []
unique_ip_address_counter = 0
flow_label_survived = [] # list of ip-addresses where the flow-label completely survived
source_flow_label_list = [] # list of source flow-labels
vantage_point_list = [] # list of vantage points used (source ip addresses)

filtered_hitlist = []
number_of_files_scanned = 0
path_id_dict = {} # dictionary where the key = destination ip address, value = [list of path_ids found] 
def build_dictionary():
    if args.directory:
        try:
            for file in os.listdir(args.directory):
                if (os.path.isfile(os.path.join(args.directory, file))):
                    with open(os.path.join(args.directory, file), 'r') as file:
                        number_of_files_scanned = number_of_files_scanned + 1
                        data = json.load(file)
                        destination_ip = data['destination']
                        if destination_ip in path_id_dict:
                            path_id_dict[destination_ip].append(data['path_id'])
                        else:
                            path_id_dict[destination_ip] = []
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)

def compare_lists():
    for key, my_list in path_id_dict.item():
        #print(f"{my_list=}")
        for a, b in itertools.combinations(my_list, 2):
            #print(f"{a=} {b=}")
            if a != b:
                print(f"Path {a} and {b} are not equal")
                filtered_hitlist.append(key)
                break
            else:
                print(f"Path {a} and {b} are equal")

def write_hitlist():
    with open(hitlist_path, "w") as file:
        for element in filtered_hitlist:
            file.write(element + "\n")

def main():
    build_dictionary()
    compare_lists()

if __name__ == "__main__":
    main()

def print_stats():
    # get unique values
    set_list = set(flow_label_survived)
    unique_list = list(set_list)
    pruned_ip_list = "/home/erlend/tmp/flowlabel_survived_list.txt"
    #pruned_ip_list = "/root/git/scripts/text-files/flowlabel_survived_list.txt"
    with open(pruned_ip_list, "w") as file:
        for element in unique_list:
            file.write(element + "\n")
        print(f"Pruned IP-address list saved to: {pruned_ip_list}")

    print(f"Number of files scanned: {number_of_files_scanned}")
    vp_set_list = set(vantage_point_list)
    vp_unique_list = list(vp_set_list)
    print(f"Number of unique source IP-addresses (vantage points): {len(vp_unique_list)}")
    print(f"Number of unique destination IP-addresses: {len(unique_list)}")
    #print(f"List of source flow-labels detected: {source_flow_label_list}")
    fl_set_list = set(source_flow_label_list)
    fl_unique_list = list(fl_set_list)
    print(f"List of unique source flow-labels found: {fl_unique_list}")
    print(f"Number of unique source flow-labels: {len(fl_unique_list)}")
    print(f"Number of times the flow-label changed in transit: {changed_counter}")
    print(f"List of hops where the flow-label changed: {changed_location}")

    print("Distribution of where the flow-label changed (the hop-number):")
    d = defaultdict(int)
    for item in changed_location:
        d[item] += 1

    print(f"{d}")
