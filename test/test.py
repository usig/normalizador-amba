# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','src'))

from CommonsTestCase import CommonsTestCase

''''''''''''''''''''''''
''' Comienza el test '''
''''''''''''''''''''''''

if __name__=='__main__':
    tl = unittest.TestLoader()
    testables = [\
                 CommonsTestCase,
                 ]
    
    for testable in testables:
        suite = tl.loadTestsFromTestCase(testable)
        unittest.TextTestRunner(verbosity=2).run(suite)
        print '======================================================================'