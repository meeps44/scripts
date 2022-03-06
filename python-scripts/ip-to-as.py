import urllib.request

# goes through a list of IP-addresses and gets which AS (Autonomous System)
# the prefix belongs to

# the end result is saved in a dictionary

file = "/root/git/scripts/text-files/responsive-addresses-test.txt"
url = r"https://api.hackertarget.com/aslookup/?q="

with open(file, "r") as my_file:
	data = my_file.readlines()

for line in data:
	print(line)
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