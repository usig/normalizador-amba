# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from CommonsTestCase import CommonsTestCase
from CallejeroTestCase import CallejeroTestCase
from NormalizadorDireccionesTestCase import NormalizadorDireccionesTestCase
from CalleYCalleTestCase import CalleYCalleTestCase
from CalleAlturaTestCase import CalleAlturaTestCase
from NormalizadorDireccionesAMBATestCase import NormalizadorDireccionesAMBATestCase
from NormalizadorDireccionesAMBACalleYCalleTestCase import NormalizadorDireccionesAMBACalleYCalleTestCase
from NormalizadorDireccionesAMBACalleAlturaTestCase import NormalizadorDireccionesAMBACalleAlturaTestCase


''''''''''''''''''''''''
''' Comienza el test '''
''''''''''''''''''''''''

if __name__=='__main__':
    tl = unittest.TestLoader()
    testables = [\
                   CommonsTestCase,
                   CallejeroTestCase,
                   CalleAlturaTestCase,
                   NormalizadorDireccionesTestCase,
                   CalleYCalleTestCase,
                   NormalizadorDireccionesAMBATestCase,
                   NormalizadorDireccionesAMBACalleYCalleTestCase,
                   NormalizadorDireccionesAMBACalleAlturaTestCase
                 ]
    
    for testable in testables:
        print ''
        print ''.center(80,'=')
        print (u'  {0}  '.format(testable.__name__)).center(80,'=')
        print ''.center(80,'=')
        suite = tl.loadTestsFromTestCase(testable)
        unittest.TextTestRunner(verbosity=2).run(suite)
