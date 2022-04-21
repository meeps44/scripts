from enum import unique
from collections import defaultdict
import argparse, json, os, itertools

# Example usage: python3 ~/git/scripts/python-scripts/flowlabel-compare-2.py -d=/mnt/c/Users/Erlend/Downloads/Archived\ Logs/Stage\ 1/Small\ scale\ test/JsonFiles/

path_id_dict = {} # dictionary where the key = destination ip address, value = [list of path_ids found] 

default_dir = os.getcwd()

# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-dir", "-d", const=default_dir, nargs='?', help="Directory containing json log files that you would like to run the flow-label check on")
parser.add_argument("--log", "-l", const='/root/logs/flowlabel_compare.log', nargs='?', help="Specify a logfile. Default = /root/logs/flowlabel_compare.log")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

path_id_list = []

changed_counter = 0
changed_location = [] # list of hop-numbers where a change in the flow-label was detected
unique_ip_addresses = []
unique_ip_address_counter = 0
number_of_files_scanned = 0
flow_label_survived = [] # list of ip-addresses where the flow-label completely survived
source_flow_label_list = [] # list of source flow-labels
vantage_point_list = [] # list of vantage points used (source ip addresses)

def build_dictionary():
    if args.directory:
        try:
            for file in os.listdir(args.directory):
                if (os.path.isfile(os.path.join(args.directory, file))):
                    filename = str(file)
                    with open(os.path.join(args.directory, file), 'r') as file:
                        number_of_files_scanned = number_of_files_scanned + 1
                        data = json.load(file)
                        vantage_point_list.append(data['source'])
                        destination_ip = data['destination']
                        source_flow_label = int(data['flow_label'])
                        source_flow_label_list.append(source_flow_label)
                        tcp_port = data['outgoing_tcp_port']
                        flow_label_changed = False
                        hop_list = [] 
        except FileNotFoundError:
            print("Error: No such file or directory")
            exit(1)
        except NotADirectoryError:
            print("Error: Not a directory")
            print("Please use the --file option to compare single files. Use the -h argument for more info.")
            exit(1)

def compare_paths():
    for my_list in my_dict.values():
        print(f"{my_list=}")
        #tmp = my_list[i]
        for a, b in itertools.combinations(my_list, 2):
            print(f"{a=} {b=}")
            if a != b:
                print(f"{a} and {b} are not equal")
                break
            else:
                print(f"{a} and {b} are equal")

def main():
    build_dictionary()
    compare_paths()

if __name__ == "__main__":
    main()


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
