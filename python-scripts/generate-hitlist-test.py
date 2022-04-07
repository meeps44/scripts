import SubnetTree, sys

def get_as_numbers_from_file(routeviews_input):
    as_numbers = []
    with open(routeviews_input, "r") as file:
        lines = file.readlines()
        for line in lines:
            my_list = line.split()
            asn = my_list[2]
            as_numbers.append(asn)
            print(f"{asn=}")

        unique_numbers = list(set(as_numbers))
    return unique_numbers

def get_asn(prefix, filename):
    #path = "/mnt/c/Users/Erlend/Downloads/RouteViews data/"
    #full = path + filename
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            list = line.split()
            ip = list[0]
            prefix_length = list[1]
            ip_with_prefix = ip + "/" + prefix_length
            asn = list[2]
            print(f"{ip=}")

            if prefix == ip_with_prefix:
                return asn
    return 0

def fill_tree(tree, fh, suffix):
    for line in fh:
        line = line.strip()
        try:
            tree[line] = line + suffix
        except ValueError as e:
            print("Skipped line '" + line + "'", file=sys.stderr)
    return tree

# generates a list of all IP-addresses in the ipv6-hitlist that belong to the same AS
def create_as_specific_hitlist(routeviewsdata, hitlist, asn):
    tree = SubnetTree.SubnetTree()
    tree = SubnetTree.fill_tree(tree, routeviewsdata)
    new_hitlist = []

    for ip_address in hitlist:
        if get_asn(ip_address) == asn:
            new_hitlist.append(ip_address)
    return new_hitlist

# creates a hitlist that is a subset of the total hitlist, containing
# all the IP-addresses that belong to a specific AS
#def create_as_specific_hitlist(routeviewsdata, hitlist, asn):
#    tree = SubnetTree.SubnetTree()
#    tree = SubnetTree.fill_tree(tree, routeviewsdata)
#    routeviews_subset = []
#
#    # generates a list of all IP-addresses in the ipv6-hitlist that belong to the same AS
#    for line in hitlist:
#        print(line + "," + tree[line] + "," + tree[line][-2:])
#        if tree[line][-2:] == asn:
#            new_list = [line, tree[line], tree[line][-2:]]
#            routeviews_subset.append(new_list)
#    return routeviews_subset

# gets the IP-address from the provided hitlist with the longest prefix length
def get_ip_with_longest_prefix(hitlist, routeviewsdata):
    tree = SubnetTree.SubnetTree()
    tree = SubnetTree.fill_tree(tree, routeviewsdata)

    prefixlength = 0
    ip = 0

    for line in hitlist:
        if tree[line][-2:] > prefixlength:
            prefixlength = tree[line][-2:]
            ip = line
    return ip

def main():
    filepath = "C:\\Users\\Erlend\\Downloads\\RouteViews data\\routeviews-rv6-20220312-2200-short.txt"
    # get_as_numbers_from_file(filepath)
    #print(get_asn("600:6001:110b::/48", filepath))
    

if __name__ == "__main__":
        main()
