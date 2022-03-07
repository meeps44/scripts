import urllib.request

# gets a list of ipv6-prefixes advertised by each public asn (up to and including asn 35000)

# the file the list gets saved to
# asnmap = "/root/git/scripts/text-files/asnmap.json"
asnmap = "/Users/admin/git/scripts/text-files/asnmap.json"

# file = "/root/git/scripts/text-files/responsive-addresses-test.txt"
# file = "/home/erlend/git/scripts/text-files/responsive-addresses-test.txt"
# file = "/home/erlend/git/scripts/text-files/responsive-addresses-test.txt"
# file = "/root/git/scripts/text-files/full-as-list.txt"

# ip_url = r"https://api.hackertarget.com/aslookup/?q="
asn_url = r"https://api.hackertarget.com/aslookup/?q=AS"

with open(asnmap, "a") as asnmap:
    for asn in range(32934, 32936):
        with urllib.request.urlopen(f"{asn_url}{asn}") as response:
            body = response.read()
            asnmap.write(f"{str(body)}\n")