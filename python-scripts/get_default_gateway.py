import netifaces

gws = netifaces.gateways()
print(gws)
gw = gws['default'][netifaces.AF_INET][0]
print(gw)
