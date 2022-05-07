from RSA import *
import unittest

class testRSA(unittest.TestCase):
    testObj = RSA()


    def testGCD(self):
        self.assertEqual(12, self.testObj.gcdExt(60,24)[0],'gcd(60,24)')
        self.assertEqual(11, self.testObj.gcdExt(22,11)[0], 'gcd(22,11)')
        self.assertEqual(6, self.testObj.gcdExt(12,6)[0], 'gcd(12,6)')
        self.assertEqual(6, self.testObj.gcdExt(18,12)[0], 'gcd(18,12)')
        self.assertEqual(6, self.testObj.gcdExt(6,0)[0], 'gcd(6,0)')
        self.assertEqual(1, self.testObj.gcdExt(11,10)[0], 'gcd(11,10)')
        self.assertEqual(1, self.testObj.gcdExt(10,1)[0], 'gcd(10,1)')
        self.assertEqual(1, self.testObj.gcdExt(1,0)[0], 'gcd(1,0)')

    def testEulersTotientFunction(self):
        self.assertEqual(1, self.testObj.eulersTotient(1), "f(1) = 1")
        self.assertEqual(1, self.testObj.eulersTotient(2), "f(2) = 1")
        self.assertEqual(2, self.testObj.eulersTotient(3), "f(3) = 2")
        self.assertEqual(2, self.testObj.eulersTotient(4), "f(4) = 2")
        self.assertEqual(4, self.testObj.eulersTotient(5), "f(5) = 4")
        self.assertEqual(2, self.testObj.eulersTotient(6), "f(6) = 2")
        self.assertEqual(6, self.testObj.eulersTotient(7), "f(7) = 6")
        self.assertEqual(4, self.testObj.eulersTotient(8), "f(8) = 4")
        self.assertEqual(6, self.testObj.eulersTotient(9), "f(9) = 6")
        self.assertEqual(4, self.testObj.eulersTotient(10), "f(10) = 4")
        self.assertEqual(10, self.testObj.eulersTotient(11), "f(11) = 10")
        self.assertEqual(4, self.testObj.eulersTotient(12), "f(12) = 4")
        self.assertEqual(12, self.testObj.eulersTotient(13), "f(13) = 12")
        self.assertEqual(6, self.testObj.eulersTotient(14), "f(14) = 6")
        self.assertEqual(8, self.testObj.eulersTotient(15), "f(15) = 8")
        self.assertEqual(8, self.testObj.eulersTotient(16), "f(16) = 8")
        self.assertEqual(16, self.testObj.eulersTotient(17), "f(17) = 16")
        self.assertEqual(6, self.testObj.eulersTotient(18), "f(18) = 6")
        self.assertEqual(18, self.testObj.eulersTotient(19), "f(19) = 18")
        self.assertEqual(8, self.testObj.eulersTotient(20), "f(20) = 8")
        self.assertEqual(12, self.testObj.eulersTotient(21), "f(21) = 12")
        self.assertEqual(10, self.testObj.eulersTotient(22), "f(22) = 10")
        self.assertEqual(22, self.testObj.eulersTotient(23), "f(23) = 22")
        self.assertEqual(8, self.testObj.eulersTotient(24), "f(24) = 8")
        self.assertEqual(20, self.testObj.eulersTotient(25), "f(25) = 20")
        self.assertEqual(12, self.testObj.eulersTotient(26), "f(26) = 12")
        self.assertEqual(18, self.testObj.eulersTotient(27), "f(27) = 18")
        self.assertEqual(12, self.testObj.eulersTotient(28), "f(28) = 12")
        self.assertEqual(28, self.testObj.eulersTotient(29), "f(29) = 28")
        self.assertEqual(8, self.testObj.eulersTotient(30), "f(30) = 8")


    def testMillerRabin(self):
        k = 49

        self.assertFalse(self.testObj.millerRabin(561 ,k), "n=561")
        self.assertTrue(self.testObj.millerRabin(29, k),  "n=29")
        self.assertFalse(self.testObj.millerRabin(221, k),  "n=221")
        self.assertFalse(self.testObj.millerRabin(21, k),  "n=21")
        self.assertTrue(self.testObj.millerRabin(47, k),  "n=47")
        self.assertFalse(self.testObj.millerRabin(174, k),  "n=174")
        self.assertFalse(self.testObj.millerRabin(200, k),  "n=200")

    #@unittest.skip("takes a long time for it to generate a key hence, don't want to slow down algorithm")
    def testKeyGeneration(self):
        #this is going to be testing assuming that the testMillerRabin function
        #will work properly. Hence, it's coupled to that function and it's 
        #working 

        p,q = self.testObj._generatePandQ()
        self.assertTrue(self.testObj.millerRabin(p), "testing if p is prime number")
        self.assertTrue(self.testObj.millerRabin(q), "testing if q is prime number")

        #doing a bits test to make sure that the generate number will have
        #1024 bits for the target n which we will need to make
        n = p * q
        binaryBits = bin(n)[2:]
        #TODO: I don't know about this, it might need to be exactly 1024, make sure that you verify with documentations
        #self.assertLess(1024, len(binaryBits), "multiplication of primes must be 1024")


    def testExtendedEuclidean(self):
        result = self.testObj.gcdExt(1398, 324)

        self.assertEqual((6,-19,82) , self.testObj.gcdExt(1398, 324), "a=139 b=324")
        self.assertEqual((1,1,0), self.testObj.gcdExt(1,2), " a=1 b=2")
        self.assertEqual((1,13,-3), self.testObj.gcdExt(13, 56), " a=13 b=56 ")
        self.assertEqual((31,2,-3), self.testObj.gcdExt(527,341), " a=527 b=341 ")
        self.assertEqual((6,5,-7), self.testObj.gcdExt(270,192), " a=270 b=192")
        self.assertEqual((12,2,-1), self.testObj.gcdExt(36,60), " a=36 b=60 ")
        self.assertEqual((5,-3,5), self.testObj.gcdExt(65,40), " a=65 b=40 ")
        self.assertEqual((13,-6,1), self.testObj.gcdExt(26,169), " a=26 b=169 ")

    def testSquareAndMultiply(self):
        b = [11, 11, 3, 7, 7, 256, 12345, ]
        e = [26,13, 104, 560, 10000000, 10000000,9999]
        n = [2, 53, 67, 561, 561, 561, 256]
        sol = [1, 52, 25, 1, 1, 1, 137]

        for ii in range(len(b)):
            self.assertEqual(sol[ii],
                    self.testObj._squareAndMultiply(e[ii], b[ii], n[ii]))
    
    def testEncyption(self):
        self.testObj.n = 187
        self.testObj.publicKey = 7
        self.testObj.message = 88
        self.assertEqual("078078", self.testObj.encrypt(), "encrypting number 88")

