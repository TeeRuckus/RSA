from enum import Enum
from Errors import *
#recommended package for cryptographic safe random generated numbers
from secrets import SystemRandom

#TODO: you will actually need to consider if you will need this class in this program or not, just seems like it's making your code highly coupled and is a waste of time
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
        self.__n = None
        self.__encryption  = encryptionStatus.decrypted


    #ACCESSOR METHODS
    @property
    def n(self): 
        return n

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
        self.__privateKey = self.__validateKey(inPrivKey)

    @publicKey.setter
    def publicKey(self, inPubKey):
        self.__publicKey = self.__validateKey(inPubKey)

    @n.setter
    def n(self, inN):
        self.__n = self.__validateInteger(inN)


    def encryption(self):
        """
        PURPOSE: an encryption algorithm which will satisfy the following
        e = M^(e) mod n, M < n
        """

        if self.__message == None:
            raise RSAEncryptionError("Please set message before trying "+
                    "encryption")

        #only the public key is needed when we're going to be encrypting a message
        if self.__publicKey == None:
            raise RSAEncryptionError("Please set public key before trying "+
                    "encryption")

        if self.n == None:
            raise RSAEncryptionError("Please set n before trying "+
                    "encryption")


        #we want each block to be no more than 2^1024 integers long
        startVal = [xx for xx in range(0, len(self.__message), 2**1024)]
        blocks = self.__createBlocks(self.__message, startVal)

        encryptedBlocks = []
        for block in blocks:
            encryptedBlocks.append(self.__encryptBlock(block))

        eMssg = "".join(encryptedBlocks)
        self.__message = eMssg

        return eMssg



    def __encryptBlock(self, inBlock):
        """
        PURPOSE: an encryption algorithm which will satisfy the following
        e = M^(e) mod n, M < n. This will encrypt just one single block at a time.

        The algorithm will encrypt one number at a time, to make it easier to
        decrypt when reading in from a file later on
        """
        encrypted = ""
        if(len(inBlock) > self.__n):
            raise RSAEncryptionError("Length of message has to be less than n"+
                    " length of n: %s and length of message: %s" % (n,self.__message))

        #converting each character into an integer
        blockInts = "".join([str(ord(xx)) for xx in inBlock])

        for mssg in blockInts:
            e += str(pow(int(mssg), self.__publicKey[0], self.__publicKey[1]))

        return e



    def decryption(self):
        """
        d = M^(ed) mod n 
        """
        pass 



    def _squareAndMultiply(self,exp:int, base:int, n:int) -> int:
        """
        PURPOSE: an efficient manner to find the solution to thew following
        problem base ^ exp mod n. This is really useful for dealing with
        algorithms which will have very large numbers. Therefore, the output
        of this algorithm will be the following
        y = base^(exp) mod n


        The square and multiply algorithm as outlined in lecture 6: Public Key
        Cryptography and RSA
        """

        #representing the base number as a binary number 
        binaryExp = self._int2Binary(exp)
        y = base

        for ii in binaryExp[1:]:
            y = pow(y, 2, n)
            if ii.strip() == "1":
                y = (y * base) % n

        return y

    #DOING METHOD
    def  gcdExt(self, a:int, b:int) -> "(gcd, x, y)":
        """
        Extracted code from assignment one fundamentals of cryptography
        submission

        ax + by = gcd(a,b)
        """
        # Base Case 
        if a == 0 :
            return b,0,1
        #recursive call to find the GCD
        gcd,x1,y1 = self.gcdExt(b%a, a)
        x = y1 - (b//a) * x1
        y = x1

        return gcd,x,y


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
            if (self.gcdExt(i, n)[0] == 1):
                result+=1
        return result


    def generateKeys(self):
        """
        PURPOSE: To generate the public keys e and d, and to generate a
        private key which will be used by the algorithm
        """

        p,q = self._generatePandQ()
        #TODO:this number is going to become the modulus key in your encryption
        #and decryption scheme, and  that number will become public
        n = p * q
        phi = (p - 1) * (q - 1)
        valid = False
        #selecting the appropriate public exponent

        while not valid:
            e = SystemRandom().randrange(2, phi)
            if (self.gcdExt(phi,e)[0] == 1):
                valid = True

        #we now have our sets of our public keys which we can use
        pubKeys = e
        #calculating the key private keys used for the algorithm
        d = self, gcdExt(e, phi)[1]
        privKey = d

        self.__privateKey = privKey
        self.__publicKey = pubKey

        return (pubKey, privKey, n)




    #TODO: just generate numbers which are going to be 155 digits long and 
    #just pick a number in between that range, it's better to get something implemented
    #by trying to do it the right way if I am being honest with you at this current moment
    def _generatePandQ(self):
        """
        PURPOSE: to generate a p and q value which will form a target n
        in the range of 2^1024. Hence, it will produce a p and q which are going
        to be 2^512. Numbers in the range will approximately have 155
        digits

        Notes:
            TODO: currently mocking function to allow for faster execution
            times hence, come back and change this so it generates numbers in
            appropriate range
        """

        #the target n is going to be 2^1024 for cryptographic secure
        #algorithm. Hence, the prime numbers will need to be in the range of 
        #2^512 which will be approximately 155 digits long. Hence, randomly
        #generating numbers which will have 155 digits

        #TODO: comeback and remove the mocking of this current objec
        #lowest bound should be 3 to satisfy n-1 in miller rabin algortihm
        lowerBound = 4
        upperBound = 20

        """
        lowerBound = "".join(["0" for ii in range(1,155)])
        lowerBound = int("1" + lowerBound)
        upperBound = "".join(["9" for ii in range(1,156)])
        upperBound = int(upperBound)
        """
        valid = False
        p, q = None, None
        pValid, qValid  = False, False


        while not valid:
            #keeping looping till p and q are going to be both prime numbers
            #we don't want to keep re-generating p and q if we have 
            #already found a prime number, as the computation process,=
            if not pValid:
                p = SystemRandom().randrange(lowerBound, upperBound)

            if not qValid:
                q = SystemRandom().randrange(lowerBound, upperBound)

            #if the generated number is even, we already know it's not prime, 
            #don't even bother to test  the following number for primality
            if (p & 1):
                if(self.millerRabin(p)):
                    pValid = True

            if(q & 1):
                if(self.millerRabin(q)):
                    qValid = True

            if(pValid and qValid):
                valid = True

        return (p,q)




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


    def _int2Binary(self, intNum, requiredLen=0):
        """
        PURPOSE: to convert an integer number to a binary number of a required 
        length, if binary number can be represented by the required length
        """
        return format(intNum, "0>"+str(requiredLen)+"b")

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

    def __createBlocks(self,inBinary,startVal):
        """
        PURPOSE: to divide up a message into blocks in relation to the starting
        values lists which is passed into the function
        """

        blocks = []
        for pos, start in enumerate(startVal):
            #if they is going to be only one block, we just ant to return that
            if len(startVal) == 1:
                blocks.append(inBinary)
            elif pos < len(startVal) - 1:
                blocks.append(inBinary[start:startVal[pos+1]])

        blocks.append(inBinary[startVal[-1]:])

        return blocks

    def __validateMessage(self, inMssg):
        #message can be anything as long as it's a string, and that string
        #will have something in it
        if(not isinstance(inMssg, str)):
            raise RSAMessageError("Message must be a string, type of %s "+
                    "was given instead" % type(inMssg))

        if (len(inMssg) == 0):
            raise RSAMessageError("A blank message was supplied length of"
                    "%s message was supplied " % len(inMssg))

        return inMssg

    def __validateKey(self, inKey):
        if (not isinstance(inKey, int)):
            raise  RSAKeyError("key must be an integer number type of %s "+
                    "was supplied instead" % type(ii))

        if (self.__n == None):
            raise RSAKeyError("Please set n before you set the keys")

        #need to check if the keys are going to be co-prime to each other, as
        #they should've being due to the calculation of the key
        if(self.gcdExt(inKey[0], self.__n)[0] != 1):
            raise RSAKeyError("Key must be co-prime with n")

        return  inKey

    def __validateInteger(self, n):
        if not isinstance(n, int):
            raise ValueError("RSA must only work with integers")

        return n

