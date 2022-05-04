from enum import Enum
from Errors import *
#better random generator, as it gives you non-pseudo random numbers for algorithm
from random import SystemRandom



class encryptionStatus(Enum):
    """
    Code adapted from own assignment one submission for fundamental concepts of 
    cryptography ISEC2000
    """
    encrypted = 1
    decrypted = 2

class RSA():
    def __init__(self):
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

    @publicKey.setter
    def publicKey(self, inPubKey):
        self.__validateKey(inPubKey)


    #PUBLIC METHODS
    def genereateKey(self):
        """
        """

    def encryption(self):
        """
        e = M^(e) mod n
        """
        pass

    def decryption(self):
        """
        d = M^(ed) mod n 
        """
        pass 

    #DOING METHOD
    def gcd(self, valOne, valTwo):
        """
        Calculates the greatest common dominator between numbers
        """
        #making sure that the assumption of a > b > 0 is held  through the 
        #algorithm
        if not(valTwo > valOne or valTwo >= 0):
            raise GCDError("ERROR: the following bust be true: a > b > 0"+
                    ": a = %s and b = %s" % (valOne, valTwo)) 

        if (valOne == 0):
            return valTwo
        return self.gcd(valTwo % valOne, valOne)

    def eulersTotient(self, n):
        """
        going to be represented by the symbol phi in calculations

        Adapter from Web page: Euler's Totient function
            WEBSITE: GeeksforGeeks
            URL: https://www.geeksforgeeks.org/eulers-totient-function/
            ACCESS DATA: 3/05/2022 
        """
        result = 1
        for i in range(2, n):
            if (self.gcd(i, n) == 1):
                result+=1
        return result


    #TODO: you will need to make sure that you will understand the maths behind this function and how it will actually work
    def millerRabin(self, n, k=49):
        """
        IMPORT: n : integer - the number which you're trying to determine is prime
                k : integer - the number of trials to find if number is valid

        EXPORT: boolean

        PURPOSE: Implementation of the Miller Rabin algorithm to determine if
        the current imported number is going to be a prime number over multiple
        tests. If the algorithm fails any of the trials then the calculated
        number is not a prime number

        NOTES: - 49 tests will give the most optimal solution given some stack 
        overflow threads
        """

        #not checking if a hasn't being repeated, as it's very unlikely for
        #the random function to produce the same number as n is required to be 
        #a very big number hence, they is a really big range of possible numbers
        for ii in range(k):
            a = SystemRandom().randrange(2, n-1)
            if not self.__millerRabin(n,a):
                #if it fails any test then it's a composite number
                return False

        return True

    def __millerRabin(self, n, a):
        """
        IMPORT: n : integer - the number which you're trying to determine if 
        it's prime number or not
                a : integer - random generated number to satisfy the condition
                ....

        EXPORT: Boolean : True if's a prime number otherwise it's not a prime
        number

        PURPOSE: Implementation of single test of miller Rabin algorithm
        """
        #defining the starting exponent of the algorithm
        exp = n - 1
        #keep looping while the number is odd, using bit wise operation as it's
        #faster

        while not exp & 1:
            #integer division by two for faster division
            exp >>= 1

        #obtained smallest odd number
        if pow(a, exp, n) ==  1:
            return True

        #for the condition when exp = -1. Since we're doing modulo division
        #n-1 is the same as -1
        while exp < n  - 1:
            if pow(a, exp, n) == n -1:
                return True

            #multiplying exponent by 2
            exp <<= 1

        return False


    def __findKandQ(self, n):
        """
        finding a power which will satisfy the following condition of 
        n -1 = 2^k * q
        """
        currPow = 1
        while (n % 2 == 0):
            #finding out how many times we can divide this number by 2 
            #until it will get to a floating point number
            currPow += 1
            n = n / 2

        return currPow, n



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

    def __validateInteger(self, n):
        if (n % 1 != 0):
            raise ValueError("RSA only works with whole numbers, %s was supplied" % n)

        return n

