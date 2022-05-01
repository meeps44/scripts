import os, argparse
# script that measurements the responsiveness of a list of IPv6-addresses

def ping(hostnames, filename):
    with open(filename, "w") as my_file:
        for hostname in hostnames:
            response = os.system("ping -c 1 " + hostname)
            if response == 0:
                print(f"{hostname} responded to ping")
                my_file.write(hostname)
            else:
                print(f"{hostname} did not respond to ping")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostnames", "-i", help="List of hostnames")
    args = parser.parse_args()

    with open(args.hostnames, "r") as my_file:
        hostnames = my_file.readlines()

    filename = "ip-responsiveness-test.txt"
    ping(hostnames, filename)

if __name__ == "__main__":
    main()
