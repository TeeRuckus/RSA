with open("look.txt", "r") as inStrm:
    contents = inStrm.readlines()


maxNum = len(str(max(contents)))
print(" max num: %s " % maxNum)
"""
contentsNumbers = "".join([str(ord(xx)) for xx in contents])
print(contents)
print(len(contentsNumbers))
"""
