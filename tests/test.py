# coding: UTF-8

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))

from tests.CommonsTestCase import CommonsTestCase
from tests.CallejeroTestCase import CallejeroTestCase
from tests.NormalizadorDireccionesTestCase import NormalizadorDireccionesTestCase
from tests.CalleYCalleTestCase import CalleYCalleTestCase
from tests.CalleAlturaTestCase import CalleAlturaTestCase
from tests.NormalizadorDireccionesAMBATestCase import NormalizadorDireccionesAMBATestCase
from tests.NormalizadorDireccionesAMBACalleYCalleTestCase import NormalizadorDireccionesAMBACalleYCalleTestCase
from tests.NormalizadorDireccionesAMBACalleAlturaTestCase import NormalizadorDireccionesAMBACalleAlturaTestCase
from tests.NormalizadorDireccionesAMBAConCabaTestCase import NormalizadorDireccionesAMBAConCabaTestCase
from tests.BuscadorDireccionesTestCase import BuscadorDireccionesTestCase
from tests.BuscadorDireccionesAMBATestCase import BuscadorDireccionesAMBATestCase

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
        print('')
        print(''.center(80, '='))
        print(('  {0}  '.format(testable.__name__)).center(80, '='))
        print(''.center(80, '='))
        suite = tl.loadTestsFromTestCase(testable)
        unittest.TextTestRunner(verbosity=2).run(suite)
