from Errors import *


class encryptionStatus(Enum):
    """
    Code adapted from own assignment one submission for fundamental concepts of 
    cryptography ISEC2000
    """
    encrypted = 1
    decrypted = 2

class RSA():
    def __init__():
        self.__message = None
        self.__privateKey = None
        self.__publicKey = None
        self.__encryption  = encryptionStatus.decrypted


    #ACCESSOR METHODS
    @property
    def message(self):
        return str(self.__message)

    @property
    def privateKey(self):
        raise RSAKeyError("ERROR: you can't access the private key as it's a secret")

    @property
    def publicKey(self):
        return self.__publicKey

    #MUTATOR METHODS
    @message.setter
    def message(self, newMssg):
       self.__message = self.__validateMessage(newMssg)

    @privateKey.setter 
    def privateKey(self, inPrivKey):
        self.__validateKey(inPrivKey)

    @ppublicKey.setter
    def publicKey(self, inPubKey):
        self.__validateKey(inPubKey)


    #PUBLIC METHODS
    def encryption(self):
        pass

    def decryption(self):
        pass 

    #DOING METHOD
    def loadFile(self, fileName):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """
        with open(fileName, "r") as inStrm:
            #read the file in as a gigantic string
            fileContents = inStrm.readlines()

        #I want the file contents as one giant string
        fileContents = "".join(fileContents)

        binaryFileContents = []
        if (self.__encryption == encryptionStatus.decrypted):
            for char in fileContents:
                binaryFileContents.append(self._char2Binary(char))
        else:
            for hexDec in fileContents:
                #binaryFileContents.append(self._hexadecimal2Binary(hexDec))
                binaryFileContents.append(self._hexadecimal2BinaryFile(hexDec))

        #making this back into one giant string again
        binaryFileContents = "".join(binaryFileContents)
        self.__message = binaryFileContents
        print("message length ", len(self.__message))

        return binaryFileContents

    def saveFile(self, fileName):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """
        binaryMessage = self._padBinaryNum(self.__message, 8)
        startVal =  [xx for xx in range(0, len(binaryMessage), 8)]
        hexGroups = self._createBlocks(binaryMessage, startVal)

        #saving the file as hexadecimal digits
        if (self.__encryption == encryptionStatus.encrypted):
            #grouping the binary into groups of 8 bits
            #grouping the current message with each group having 8 bits
            with open(fileName, "w" ) as outStrm:
                for binary in hexGroups:
                    toWrite = self._binary2Hexadecimal(binary)
                    if len(toWrite) == 1:
                        toWrite = "0" + toWrite
                    outStrm.write(toWrite)
        else:
            with open(fileName, "w") as outStrm:
                for binary in hexGroups:
                    outStrm.write(self._binary2Char(binary))

    def _char2Binary(self, inChar):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """
        intChar = ord(inChar)
        binaryNum = ""

        #we want this to be easily represented in hexadecimal, and
        #we don't want information to be lost in the process. Hence,
        #requiring that each character will be represented by 8 bits. As
        #that will encompass all characters on the ASCII table
        binaryNum = self._calcInt2Binary(intChar, 8)

        return binaryNum

    def _hexadecimal2BinaryFile(self, inHex):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """
        decNum = int(inHex, 16)
        binaryNum = format(decNum, "0>4b")

        return binaryNum

    #TODO: I think that he maths in here is going to be a little bit wrong
    def _padBinaryNum(self, inBinary, requiredLen):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """

        remainder = 0
        #we always want the big number to be divided by the smaller number
        if len(inBinary) > requiredLen:
            remainder = len(inBinary) % requiredLen
        else:
            remainder =  requiredLen % len(inBinary)

        bits = "".join(["0" for xx in range(0,remainder)])
        #padding the front of the message with the required zeros
        inBinary = bits + inBinary
        return  inBinary

    def _createBlocks(self,inBinary,startVal):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """
        blocks = []
        for pos, start in enumerate(startVal):
            #if they is going to be only one block, we just ant to return that
            if len(startVal) == 1:
                blocks.append(inBinary)
            elif pos < len(startVal) - 1:
                blocks.append(inBinary[start:startVal[pos+1]])

        #TODO: make sure that this is actually working properly
        #print(startVal[-1])
        #flushing out the remainder of the message once at the end of the blocks#
        blocks.append(inBinary[startVal[-1]:])


        return blocks

    def _binary2Hexadecimal(self, inBinary):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """
        decimalNum =  int(inBinary,2)
        hexNum = hex(decimalNum)

        return hexNum[2:]


    def  _binary2Char(self, inBinary):
        """
        Code adapted from own assignment one submission for fundamental concepts of 
        cryptography ISEC2000
        """
        decNum = int(inBinary, 2)
        return chr(decNum)

    #PRIVATE METHODS 
    def __validateMessage(self, inMssg): 
        #TODO: come back and implement this method when you will have time
        pass

    def __validateKey(self, inPubKey):
        #TODO: come back and implement this method when you will have time
        pass
