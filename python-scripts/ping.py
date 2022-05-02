import os, argparse, sys
# Script that measurements the responsiveness of a list of IPv6-addresses
# Usage example: python3 ping.py --hostnames=/root/git/scripts/text-files/nslookup-alexa-top500-full.txt

def ping(hostnames, filename):
    with open(filename, "w") as my_file:
        for hostname in hostnames:
            response = os.system("ping -c 1 " + hostname)
            if response == 0:
                my_file.write(hostname)
            else:
                print(f"{hostname} did not respond to ping", file=sys.stderr)

def main():
    filename = "responsive-alexatop500-addresses.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument("--hostnames", "-i", help="List of hostnames")
    args = parser.parse_args()

    with open(args.hostnames, "r") as my_file:
        hostnames = my_file.readlines()

    ping(hostnames, filename)

if __name__ == "__main__":
    main()
