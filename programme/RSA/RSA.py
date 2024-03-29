from enum import Enum
from Errors import *
#recommended package for cryptographic safe random generated numbers
from secrets import SystemRandom

#this is going to be the numbers which will work for p and q numbers being 2^64
#DIGIT_LEN = 20
DIGIT_LEN = 41
DIGIT_LEN_HEX = 35

class RSA():
    def __init__(self):
        self.__message = None
        self.__privateKey = None
        self.__publicKey = None
        self.__n = None


    #ACCESSOR METHODS
    @property
    def n(self): 
        return self.__n

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


    def encrypt(self):
        """
        PURPOSE: an encryption algorithm which will satisfy the following
        e = M^(e) mod n, M < n
        """

        if self.__message == "None":
            raise RSAEncryptionError("Please set message before trying "+
                    "encryption")

        #only the public key is needed when we're going to be encrypting a message
        if self.__publicKey == None:
            raise RSAEncryptionError("Please set public key before trying "+
                    "encryption")

        if self.n == None:
            raise RSAEncryptionError("Please set n before trying "+
                    "encryption")

        messageInts = [format(ord(xx), "0>3") for  xx in self.__message]

        encryptedBlocks = []
        for number in messageInts:
            encryptedBlocks.append(self.__encryptBlock(number))

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
        if(len(inBlock) > self.__n):
            raise RSAEncryptionError("Length of message has to be less than n"+
                    " length of n: %s and length of message: %s" % (self.__n,len(self.__message)))

        e = str(pow(int(inBlock), self.__publicKey, self.__n))
        #formatting the encrypted message, so it will be a lot easier to 
        #decrypt at the end
        #giving the range which prime numbers can be, the longest length of
        #integer possible is going to be of 20 digits hence, for numbers
        #which will fall show we will want to pad them to the left, so 
        #it's easier to decrypt
        e = format(e, "0>%s" % DIGIT_LEN)

        return e



    def decrypt(self):
        """
        To decrypt the whole message in relation to the function
        d = M^(d) mod n 
        """
        #we have to compare it to the string of None because when you set a 
        #message it's always going to be made to a string
        if self.__message == "None":
            raise RSADecryptionError("Please set a cipher text before trying"+
                    " to decrypt message")

        if self.__privateKey == None:
            raise RSADecryptionError("Please set private key before trying"+
                    " to decrypt messages")


        if self.__n == None:
            raise RSADecryptionError("Please set n before trying to "
                    "decrypt message")


        #the cipher texts will have being stored in groups of three
        #from the encryption algorithm, getting groups of three from the
        #algorithm 
        startValues = [xx for xx in range(0, len(self.__message), DIGIT_LEN)]
        cipher = self.__createBlocks(self.__message, startValues)

        message = []
        for number in cipher:
            message.append(self.__decryptBlock(number))

        message = "".join(message)
        self.__message = message

        return message


    def __decryptBlock(self, inCipher):
        """
        decrypting an integer, and the actual implementation of the decryption
        of
        d = m^(d) mod n
        """
        e = chr(pow(int(inCipher), self.__privateKey, self.__n))

        return e



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
        n = p * q
        phi = (p - 1) * (q - 1)
        valid = False
        #selecting the appropriate public exponent

        while not valid:
            e = SystemRandom().randrange(2, phi)
            if (self.gcdExt(phi,e)[0] == 1):
                valid = True

        #we now have our sets of our public keys which we can use
        pubKey = e
        #calculating the key private keys used for the algorithm
        d = self.gcdExt(e, phi)[1]
        privKey = d

        self.__privateKey = privKey
        self.__publicKey = pubKey

        return (pubKey, privKey, n)

    def loadFileText(self, fileName):
        """
        load a file which is going to normal alphabetic letters
        """
        with open(fileName, "r") as inStrm:
            #read the file in as a gigantic string
            fileContents = inStrm.readlines()

        #I want the file contents as one giant string
        fileContents = "".join(fileContents)
        self.__message = fileContents

        return fileContents

    def loadFileHex(self, fileName):
        """
        load a file which is going to be formatted as hexadecimal
        """
        with open(fileName, "r") as inStrm:
            #read the file in as a gigantic string
            fileContents = inStrm.readlines()

        #changing the hex contents back to integers, so the encryption and 
        #decryption algorithms can function as expected
        fileContents = "".join(fileContents)
        startValues = [xx for xx in range(0, len(fileContents), DIGIT_LEN_HEX)]
        data = self.__createBlocks(fileContents, startValues)
        dataInts = [self._hex2int(xx) for xx in data]
        self.__message = "".join(dataInts)

    def saveFileHex(self, fileName):
        """
        Save the file in a hex decimal format
        """

        #splitting up the message into the blocks which they were created, so 
        #we can convert that into a hexadecimal number 
        startValues = [xx for xx in range(0, len(self.__message), DIGIT_LEN)]
        data = self.__createBlocks(self.__message, startValues)
        dataHex = [self._int2Hex(xx) for xx in data]
        dataHex = "".join(dataHex)

        with open(fileName, "w") as outStrm:
            outStrm.writelines(dataHex)

    def saveFile(self, fileName):
        """
        Save a file as a normal text file
        """
        with open(fileName, "w") as outStrm:
            outStrm.writelines(self.__message)

    def _generatePandQ(self):
        """
        PURPOSE: to generate a p and q value which will form a target n
        in the range of 2^64. Hence, it will produce a p and q which are going
        to be 2^512. Numbers in the range will approximately have 155
        digits
        """

        #the target n is going to be 2^64 for as specified by the assignment
        #algorithm. Hence, the prime numbers will need to be in the range of 
        #2^32 which will be approximately 155 digits long. Hence, randomly
        #generating numbers which will have 155 digits

        lowerBound =   pow(2,64)
        upperBound = 2 * pow(2,64)


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

    def _int2Hex(self, inInt):
        """
        To convert an integer number into it's hexadecimal equivalent
        """
        inInt = int(inInt)
        hexNum = hex(inInt)
        hexNum = hexNum[2:]
        hexNum = format(hexNum, "0>%s" % DIGIT_LEN_HEX)

        return hexNum


    def _hex2int(self, inHex):
        """
        To convert a hexadecimal number back to its integer representation
        """
        intHex = int(inHex,16)
        intHex = format(intHex, "0>%s" % DIGIT_LEN)
        return intHex

    #PRIVATE METHODS 

    def __createBlocks(self,inStr,startVal):
        """
        PURPOSE: to divide up a message into blocks in relation to the starting
        values lists which is passed into the function
        """
        blocks = []
        for pos, start in enumerate(startVal):
            #if they is going to be only one block, we just ant to return that
            if len(startVal) == 1:
                blocks.append(inStr)
            elif pos < len(startVal) - 1:
                blocks.append(inStr[start:startVal[pos+1]])

        if len(startVal) != 1:
            blocks.append(inStr[startVal[-1]:])

        return blocks

    def __validateMessage(self, inMssg):
        #forcing inMssg to be a string when it's read in
        inMssg = str(inMssg)
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

        return  inKey

    def __validateInteger(self, n):
        if not isinstance(n, int):
            raise RSAError("RSA must only work with integers")

        if n <= (2 ** 64):
            raise RSAError("Select an n which is within the range of 2**64"+
                    " current selected number %s " % n)

        return n
