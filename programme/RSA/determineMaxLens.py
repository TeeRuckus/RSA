with open("look.txt", "r") as inStrm:
    contents = inStrm.readlines()


maxNum = max(contents)
print(" max num: %s " % len(maxNum))
"""
contentsNumbers = "".join([str(ord(xx)) for xx in contents])
print(contents)
print(len(contentsNumbers))
"""
