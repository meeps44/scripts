import argparse, json, logging

# initialize logging:
#logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.basicConfig(filename='example.log',
format='%(asctime)s %(levelname)-8s %(message)s',
level=logging.INFO,
datefmt='%Y-%m-%d %H:%M:%S')

# takes two json-files as input and compares the hop-list

parser = argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
parser.add_argument('-v', '-V', '--v', '--V', action='store_true') 
# if the -v flag is enabled, dump both routes to stdout
# action='store_true' implies default=False. Conversely, you could have action='store_false', which implies default=True.
args = parser.parse_args()


with open(args.file1, "r") as file1, open(args.file2, "r") as file2:
    # returns JSON object as a dictionary
    data1 = json.load(file1)
    data2 = json.load(file2)
    
    # result = data1['hops']['2'] == data2['hops']['2']

    for key, value in data1['hops'].items():
        # print(f"{key}:{value}")
        try:
            if (data1['hops'][key] != data2['hops'][key]):
                print("Route difference detected!")
                result = False
                break
            result = data1['hops'][key] == data2['hops'][key]
        except KeyError:
            print("KeyError")
            result = False
            break
    
    if (result):
        logging.info(f"Routes in file {args.file1} and {args.file2} are equal.")
        print("The routes are equal")
        if (args.v):
            print("Route 1: ")
            for k, v in data2['hops'].items():
                print(f"{k}:{v}")
            print("Route 2: ")
            for k, v in data1['hops'].items():
                print(f"{k}:{v}")
    else:
        logging.info(f'Routes in file {args.file1} and {args.file2} are not equal!')
        print("The routes are not equal")
        if (args.v):
            print("Route 1: ")
            for k, v in data2['hops'].items():
                print(f"{k}:{v}")
            print("Route 2: ")
            for k, v in data1['hops'].items():
                print(f"{k}:{v}")
