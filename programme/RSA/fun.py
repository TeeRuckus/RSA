with open("RSA-test.txt", "r") as inStrm:
    contents = inStrm.readlines()


contents = "".join(contents)
contentsNumbers = "".join([str(ord(xx)) for xx in contents])
print(contents)
print(len(contentsNumbers))
