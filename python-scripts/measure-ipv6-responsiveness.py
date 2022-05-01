import os
# script that measurements the responsiveness of a list of IPv6-addresses

def ping(hostnames, filename):
    with open(filename, "w") as my_file:
        for hostname in hostnames:
            response = os.system("ping -c 1 " + hostname)
            if response == 0:
                print(f"{hostname} responded to ping")
                my_file.write(hostname + "\n")
            else:
                print(f"{hostname} did not respond to ping")

def main():
    filename = "ip-responsiveness-test.txt"
    hostnames = ["google.com"]
    ping(hostnames, filename)

if __name__ == "__main__":
    main()