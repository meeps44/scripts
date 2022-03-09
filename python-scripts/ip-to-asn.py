import urllib.request, whois

# matches a prefix with an IP-address.
# the result, along with the AS advertising this specifix prefix is logged
# to a key-value dictionary.

# file = "/root/git/scripts/text-files/responsive-addresses-test.txt"
# file = "/home/erlend/git/scripts/text-files/responsive-addresses-test.txt"
file = "/home/erlend/git/scripts/text-files/responsive-addresses-test.txt"
url = r"https://api.hackertarget.com/aslookup/?q="

#with open(file, "r") as my_file:
	#data = my_file.readlines()
	#for line in data:
		#with urllib.request.urlopen(f"{url}{line}") as response:
			#body = response.read()
			#print(body)

ip = "2a00:1450:4009:823::200e"

w = whois.whois(ip)
print(w)