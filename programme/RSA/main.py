from RSA import *
def main():
    #I am just trying to play with my assignment and to see if I can get it
    #encrypting and decrypting properly for the text
    rsaObj = RSA()
    keys = rsaObj.generateKeys()
    rsaObj.n = keys[2]
    rsaObj.publicKey = keys[0]
    rsaObj.privateKey = keys[1]
    contents = rsaObj.loadFileText("RSA-test.txt")
    encryptedMssg = rsaObj.encrypt()
    message = rsaObj.decrypt()
    print(message)



if __name__ == "__main__": 
    main()
