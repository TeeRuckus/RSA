from RSA import *
import unittest

class testRSA(unittest.TestCase):
    testObj = RSA()


    def testGCD(self):
        self.assertEqual(12, self.testObj.gcd(60,24),'gcd(60,24)')
        self.assertEqual(11, self.testObj.gcd(22,11), 'gcd(22,11)')
        self.assertEqual(6, self.testObj.gcd(12,6), 'gcd(12,6)')
        self.assertEqual(6, self.testObj.gcd(18,12), 'gcd(18,12)')
        self.assertEqual(6, self.testObj.gcd(6,0), 'gcd(6,0)')
        self.assertEqual(1, self.testObj.gcd(11,10), 'gcd(11,10)')
        self.assertEqual(1, self.testObj.gcd(10,1), 'gcd(10,1)')
        self.assertEqual(1, self.testObj.gcd(1,0), 'gcd(1,0)')

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
