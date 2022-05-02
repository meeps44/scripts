import argparse, json, os, hashlib

# Gets the number of hops between a source host to a destination node

default_dir = os.getcwd()
# initialize argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-dir", "-d", const=default_dir, nargs='?', help="Directory containing json log files that you would like to run the flow-label check on")
args = parser.parse_args()
directory_contents = os.listdir(args.directory)

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
    print(f"{scanned} documents scanned")

if __name__ == "__main__":
	main()
