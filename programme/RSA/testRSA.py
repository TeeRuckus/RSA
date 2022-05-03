from RSA import *
import unittest

class testRSA(unittest.TestCase):
    testObj = RSA()


    def testGCD(self):
        self.assertEqual(12, self.testObj.gcd(60,24))
        self.assertEqual(11, self.testObj.gcd(22,11))
        self.assertEqual(6, self.testObj.gcd(12,6))
        self.assertEqual(6, self.testObj.gcd(18,12))
        self.assertEqual(6, self.testObj.gcd(6,0))
        self.assertEqual(1, self.testObj.gcd(11,10))
        self.assertEqual(1, self.testObj.gcd(10,1))
        self.assertEqual(1, self.testObj.gcd(1,0))



    def testEulersTotientFunction(self):
        pass
