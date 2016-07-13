# coding: UTF-8
from __future__ import absolute_import
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

from CommonsTestCase import CommonsTestCase
from CallejeroTestCase import CallejeroTestCase
from NormalizadorDireccionesTestCase import NormalizadorDireccionesTestCase
from CalleYCalleTestCase import CalleYCalleTestCase
from CalleAlturaTestCase import CalleAlturaTestCase
from NormalizadorDireccionesAMBATestCase import NormalizadorDireccionesAMBATestCase
from NormalizadorDireccionesAMBACalleYCalleTestCase import NormalizadorDireccionesAMBACalleYCalleTestCase
from NormalizadorDireccionesAMBACalleAlturaTestCase import NormalizadorDireccionesAMBACalleAlturaTestCase
from NormalizadorDireccionesAMBAConCabaTestCase import NormalizadorDireccionesAMBAConCabaTestCase
from BuscadorDireccionesTestCase import BuscadorDireccionesTestCase
from BuscadorDireccionesAMBATestCase import BuscadorDireccionesAMBATestCase

''''''''''''''''''''''''
''' Comienza el test '''
''''''''''''''''''''''''
if __name__ == '__main__':
    tl = unittest.TestLoader()
    testables = [
        CommonsTestCase,
        CallejeroTestCase,
        NormalizadorDireccionesTestCase,
        CalleYCalleTestCase,
        CalleAlturaTestCase,
        NormalizadorDireccionesAMBATestCase,
        NormalizadorDireccionesAMBACalleYCalleTestCase,
        NormalizadorDireccionesAMBACalleAlturaTestCase,
        NormalizadorDireccionesAMBAConCabaTestCase,
        BuscadorDireccionesTestCase,
        BuscadorDireccionesAMBATestCase
    ]

    for testable in testables:
        print ''
        print ''.center(80, '=')
        print (u'  {0}  '.format(testable.__name__)).center(80, '=')
        print ''.center(80, '=')
        suite = tl.loadTestsFromTestCase(testable)
        unittest.TextTestRunner(verbosity=2).run(suite)
