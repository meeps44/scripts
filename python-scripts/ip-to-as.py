import urllib.request

# matches a prefix with an IP-address.
# the result, along with the AS advertising this specifix prefix is logged
# to a key-value dictionary.

# goes through a list of IP-addresses and gets which AS (Autonomous System)
# the IP-address belongs to, up to a maximum of 35000 ASes. 
# the script will get one IP-address per AS.

# file = "/root/git/scripts/text-files/responsive-addresses-test.txt"
file = "/home/erlend/git/scripts/text-files/responsive-addresses-test.txt"
url = r"https://api.hackertarget.com/aslookup/?q="

with open(file, "r") as my_file:
	data = my_file.readlines()
	for line in data:
		with urllib.request.urlopen(f"{url}{line}") as response:
			body = response.read()
			print(body)

#dict = {
	#"asn":2549,
	#"prefixes": [
		#"2001:1210:105:34:0:606:a8:31"
		#"2001:1210::1:1"
	#],
	#"AS range":"2001:1210::1:1"
#}