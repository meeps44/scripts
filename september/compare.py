import dataclasses

# Each path object is a list of tuples consisting of the hop number and
# the hop address.
# We are assuming that the paths all have the same
# (source, destination, flow label, destination port number) 4-tuple.


def compare_paths(path1, path2, path3, path4):
    hash1 = create_path_hash(path1)
    hash2 = create_path_hash(path2)
    hash3 = create_path_hash(path3)
    hash4 = create_path_hash(path4)

    if (hash1 == hash2 and hash1 == hash3 and hash1 == hash4):
        print("All 4 paths are equal!")
        return True

    print("All 4 paths are not equal")
    return False


# Creates a new path object from a list of hop data.
# Input: Index into the list of hop data where


def create_path(index):
    path = list()
    hop_count = index.hop_count
    counter = 0
    while(counter < hop_count):
        path_item = tuple(1, "some ip")
        path.append(path_item)
    return path
