from RSA import *
def main():
    #I am just trying to play with my assignment and to see if I can get it
    #encrypting and decrypting properly for the text
    rsaObj = RSA()
    rsaObj.n = 187
    rsaObj.publicKey = 7
    contents = rsaObj.loadFile("RSA-test.txt")
    encryptedMssg = rsaObj.encrypt()
    #print(encryptedMssg)


if __name__ == "__main__": 
    main()
