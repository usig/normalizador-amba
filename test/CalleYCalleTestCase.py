# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','src'))

from NormalizadorDirecciones import *
from Partido import Partido
from Errors import *
from settings import *

class CalleYCalleTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    nd = NormalizadorDirecciones(p)
    
    def testCalleInexistente01(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'Elm street y Roque Sáenz Peña')

    def testCalleInexistente02(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'Roque Sáenz Peña y kokusai dori')

    def testCalle1UnicaCalle2UnicaCruceInexistente(self):
        try:
            self.nd.normalizar('Mateo Bootz y pavon')
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCruceInexistente))
            self.assertEqual(len(e.getMatchingsCalle1()), 1, 'Deberia haber 1 matching')
            self.assertEqual(len(e.getMatchingsCalle2()), 1, 'Deberia haber 1 matching')

    def testCalle1MuchasCalle2MuchasCruceInexistente(self):
        try:
            self.nd.normalizar('saenz peña y gaspar campos')
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCruceInexistente))
            self.assertEqual(len(e.getMatchingsCalle1()), 2, 'Deberia haber 2 matchings')
            self.assertEqual(len(e.getMatchingsCalle2()), 2, 'Deberia haber 2 matchings')

    def testCalle1UnicaCalle2UnicaCruceExistente(self):
        res = self.nd.normalizar(u'Suecia y libano')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 56284772)
        self.assertEqual(d.calle.nombre, u'Suecia')
        self.assertEqual(d.cruce.codigo, 84216905)
        self.assertEqual(d.cruce.nombre, 'Libano')

    def testCalle1UnicaCalle2MuchasCruceExistenteUnico(self):
        res = self.nd.normalizar("libano y santiago")
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 84216905)
        self.assertEqual(d.calle.nombre, u'Libano')
        self.assertEqual(d.cruce.codigo, 56297295)
        self.assertEqual(d.cruce.nombre, 'Santiago de Liniers')

    def testCalle1MuchasCalle2UnicaCruceExistenteUnico(self):
        res = self.nd.normalizar("san y libano")
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 56297295)
        self.assertEqual(d.calle.nombre, 'Santiago de Liniers')
        self.assertEqual(d.cruce.codigo, 84216905)
        self.assertEqual(d.cruce.nombre, u'Libano')

    def testCalleConY01(self):
        res = self.nd.normalizar(u'fraga y Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 26954872)
        self.assertEqual(d.calle.nombre, 'Fraga')
        self.assertEqual(d.cruce.codigo, 46779820)
        self.assertEqual(d.cruce.nombre, u'Gelly y Obes')

    def testCalleConY02(self):
        res = self.nd.normalizar(u'Gelly y Obes y fraga')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 46779820)
        self.assertEqual(d.calle.nombre, u'Gelly y Obes')
        self.assertEqual(d.cruce.codigo, 26954872)
        self.assertEqual(d.cruce.nombre, 'Fraga')

    def testCalleConY03(self):
        res = self.nd.normalizar(u'Gel y Ob y fraga')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 46779820)
        self.assertEqual(d.calle.nombre, u'Gelly y Obes')
        self.assertEqual(d.cruce.codigo, 26954872)
        self.assertEqual(d.cruce.nombre, 'Fraga')

    def testCalleConYParcial01(self):
        res = self.nd.normalizar(u'fraga y Gel y Ob')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 26954872)
        self.assertEqual(d.calle.nombre, 'Fraga')
        self.assertEqual(d.cruce.codigo, 46779820)
        self.assertEqual(d.cruce.nombre, u'Gelly y Obes')

    def testDireccionSeparadaPorE01(self):
        res = self.nd.normalizar(u'pinero e iglesia')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 30417861)
        self.assertEqual(d.calle.nombre, 'Pinero')
        self.assertEqual(d.cruce.codigo, 30417876)
        self.assertEqual(d.cruce.nombre, u'Iglesias')
