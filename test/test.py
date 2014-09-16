# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','normalizador_direcciones_gba'))

from CommonsTestCase import CommonsTestCase
from CallejeroTestCase import CallejeroTestCase
from NormalizadorDireccionesTestCase import NormalizadorDireccionesTestCase
from CalleYCalleTestCase import CalleYCalleTestCase
from NormalizadorDireccionesGBATestCase import NormalizadorDireccionesGBATestCase


''''''''''''''''''''''''
''' Comienza el test '''
''''''''''''''''''''''''

if __name__=='__main__':
    tl = unittest.TestLoader()
    testables = [\
                 CommonsTestCase,
                 CallejeroTestCase,
                 NormalizadorDireccionesTestCase,
                 CalleYCalleTestCase,
                 NormalizadorDireccionesGBATestCase,
                 ]
    
    for testable in testables:
        print ''
        print ''.center(80,'=')
        print (u'  {0}  '.format(testable.__name__)).center(80,'=')
        print ''.center(80,'=')
        suite = tl.loadTestsFromTestCase(testable)
        unittest.TextTestRunner(verbosity=2).run(suite)
        