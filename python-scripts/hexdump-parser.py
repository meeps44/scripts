"""
 Parses raw IPv6 hexdump in the format:

60 00 80 00 00 98 3a 36 20 01 48 60 00 00 00 00 
00 00 00 08 40 00 f4 33 2a 03 b0 c0 00 01 00 d0 
00 00 00 00 0b 45 60 01 03 00 aa b5 00 00 00 00 
68 00 00 01 00 16 06 04 2a 03 b0 c0 00 01 00 d0 
00 00 00 00 0b 45 60 01 2a 00 14 50 40 0f 08 0d 
00 00 00 00 00 00 20 0e 82 b1 01 bb 00 00 00 00 
00 00 00 00 50 00 16 d0 00 0a 00 00 27 47 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
20 00 df a2 00 0c 01 01 9e 4a 38 01 00 00 29 04 
""" 

"""
Example output:
###[ IPv6 ]### 
  version   = 6
  tc        = 0
  fl        = 0
  plen      = 70
  nh        = ICMPv6
  hlim      = 63
  src       = 2604:a880:ffff:6:1::418
  dst       = 2a03:b0c0:1:d0::b45:6001
###[ ICMPv6 Time Exceeded ]### 
     type      = Time exceeded
     code      = hop limit exceeded in transit
     cksum     = 0x7d04
     length    = 0
     unused    = 0x0
###[ IPv6 in ICMPv6 ]### 
        version   = 6
        tc        = 0
        fl        = 1
        plen      = 22
        nh        = TCP
        hlim      = 1
        src       = 2a03:b0c0:1:d0::b45:6001
        dst       = 2a00:1450:400f:80d::200e
###[ TCP in ICMP ]### 
           sport     = 33457
           dport     = https
           seq       = 0
           ack       = 0
           dataofs   = 5
           reserved  = 0
           flags     = 
           window    = 5840
           chksum    = 0x3
           urgptr    = 0
           options   = []
###[ Raw ]### 
              load      = "'N"
"""

def parse(data):
    print("Packet values:")

def main():
    filepath = ""
    with open(filepath, "r") as file:
        data = file.read()
    
    parse(data)

if __name__ == "__main__":
    main()
