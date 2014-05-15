# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','src'))

from CommonsTestCase import CommonsTestCase
from CallejeroTestCase import CallejeroTestCase

''''''''''''''''''''''''
''' Comienza el test '''
''''''''''''''''''''''''

if __name__=='__main__':
    tl = unittest.TestLoader()
    testables = [\
                 CommonsTestCase,
                 CallejeroTestCase,
                 ]
    
    for testable in testables:
        print ''
        print ''.center(80,'=')
        print ('  %s  ' % testable.__name__).center(80,'=')
        print ''.center(80,'=')
        suite = tl.loadTestsFromTestCase(testable)
        unittest.TextTestRunner(verbosity=2).run(suite)
        