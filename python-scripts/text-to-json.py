import json, uuid, argparse, datetime, os

parser = argparse.ArgumentParser()
parser.add_argument("filepath")
parser.add_argument("hostname")
parser.add_argument("tcp_port")
parser.add_argument("source_ip")
parser.add_argument("flow_label")
args = parser.parse_args()

# "/Users/admin/Desktop/test-new.txt"

with open(args.filepath, "r") as my_file:
    hop_list = my_file.read().splitlines() 

# Remove first item in the list (the destination address) and add it as separate dictionary element
dest = hop_list.pop(0)
dest_dict = { "destination": dest}

# Create top-level dictionary
my_dict = {}
my_dict["probe_uuid"] = str(uuid.uuid4())
# my_dict["flow_label"] = 100
my_dict["outgoing_tcp_port"] = args.tcp_port
my_dict["flow_label"] = args.flow_label
my_dict["timestamp"] = str(datetime.datetime.now())
my_dict["source"] = args.source_ip
my_dict["destination"] = dest

count = 0 # in case items is empty and you need it after the loop
hop_dictionary = { count : item for count, item in enumerate(hop_list, start=1) }

my_dict["hops"] = hop_dictionary

json_file = args.filepath
if json_file.endswith('.txt'):
    json_file = json_file[:-4]

json_file = json_file + ".json"

#print(os.path.basename(json_file))

#with open(f'{json_file}', 'w') as fp:
    #json.dump(my_dict, fp, indent=4)

path = f'/root/logs/{args.hostname}/' + os.path.basename(json_file)

print(path)

with open(path, 'w') as fp:
    json.dump(my_dict, fp, indent=4)

#TODO: Add Source IP dictionary field
#TODO: Add time&date dictionary field
#TODO: Add outgoing TCP port field
#TODO: Add any other fields (packet metadata?)