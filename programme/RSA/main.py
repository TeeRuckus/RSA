from RSA import *
import argparse

DEFAULT_KEYS_FILE = "keys.rsa"

RSA_DESCRIPTION  = """
                A demonstration of the RSA algorithm and how common RSA features 
                will work such as key scheduling, primality tests, encryption,
                and description.

                IMPORTANT NOTE: This should not be used for actual cryptographic
                purposes, this is purely a demonstration and program is not
                safe
                  """

def main():
    #adding in the argument parser arguments
    parser = argparse.ArgumentParser(description=RSA_DESCRIPTION)
    parser.add_argument("mode", help="Weather you would like to run this demonstration"
            + "in encryption or decryption mode")
    parser.add_argument("inputFile", help="Enter the file which you want to read"
            " data in from")
    parser.add_argument("outputFile", help="Enter the file which you want to"+
            " export the results of this demonstration to")
    args = parser.parse_args()

    rsa = RSA()
    if (args.mode.upper()[0] == "E"):
        generateKeys(rsa)
        rsa.loadFileText(args.inputFile)
        rsa.encrypt()
        rsa.saveFileHex(args.outputFile)

    if(args.mode.upper()[0] == "D"):
        loadKeys(rsa)
        rsa.loadFileHex(args.inputFile)
        rsa.decrypt()
        rsa.saveFile(args.outputFile)

def loadKeys(rsa, fileName=DEFAULT_KEYS_FILE):
    """
    Function to load keys from file if the file exists, if the keys file doesn't
    exist create new keys and create the keys file for usage
    """
    try:
        with open(fileName, "r") as inStrm:
            fileContents = inStrm.readlines()

        if len(fileContents) == 0:
            print("no keys stored in file, generating new keys")
            generateKeys(rsa, fileName)
        else:
            fileFound(fileContents, rsa)

    except FileNotFoundError as err:
        print("Specified key file doesn't exist. Generating and creating new"
                +' file "keys.rsa" to store keys')

        generateKeys(rsa,fileName)


def fileFound(fileContents, rsa):
    print("Found file ...")
    keys = "".join(fileContents)
    keys = keys.split(" ")
    keys = [int(xx.strip()) for xx in keys]
    rsa.n = keys[2]
    rsa.publicKey = keys[0]
    rsa.privateKey = keys[1]

def generateKeys(rsa, fileName=DEFAULT_KEYS_FILE):
    """
    It checks if a keys file has already being created, if it has it will use
    that file instead of generating a new set of keys, as generating keys is
    a very expensive process which takes a lot of computing power
    """
    try:
        with open(fileName, "r") as inStrm:
            fileContents = inStrm.readlines()
        fileFound(fileContents, rsa)

    except FileNotFoundError as err:
        #generating new keys file
        keys = rsa.generateKeys()
        rsa.n = keys[2]
        rsa.publicKey = keys[0]
        rsa.privateKey = keys[1]
        keys = " ".join([str(xx).strip() for xx in keys])

        #writing the keys file into the system
        with open(fileName, "w") as outStrm:
            outStrm.writelines(keys)

if __name__ == "__main__":
    main()
