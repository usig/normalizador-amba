# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDirecciones import NormalizadorDirecciones
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.Errors import ErrorCalleInexistente, ErrorCruceInexistente

from usig_normalizador_amba.settings import CALLE_Y_CALLE

from test_commons import cargarCallejeroEstatico


class CalleYCalleTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    nd = NormalizadorDirecciones(p)
    cargarCallejeroEstatico(nd.c)

    def _checkDireccion(self, direccion, codigo_calle, nombre_calle, codigo_cruce, nombre_cruce, codigo_partido, localidad):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.tipo, CALLE_Y_CALLE)
        self.assertEqual(direccion.calle.codigo, codigo_calle)
        self.assertEqual(direccion.calle.nombre, nombre_calle)
        self.assertEqual(direccion.cruce.codigo, codigo_cruce)
        self.assertEqual(direccion.cruce.nombre, nombre_cruce)
        self.assertEqual(direccion.partido.codigo, codigo_partido)
        self.assertEqual(direccion.localidad, localidad)

    def testCalleInexistente01(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'Elm street y Roque Sáenz Peña')

    def testCalleInexistente02(self):
        self.assertRaises(ErrorCruceInexistente, self.nd.normalizar, u'Roque Sáenz Peña y kokusai dori')

    def testCalle1UnicaCalle2UnicaCruceInexistente(self):
        try:
            self.nd.normalizar('Mateo Bootz y pavon')
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCruceInexistente))

    def testCalle1MuchasCalle2MuchasCruceInexistente(self):
        try:
            self.nd.normalizar(u'saenz peña y gaspar campos')
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCruceInexistente))

    def testCalle1UnicaCalle2UnicaCruceExistente(self):
        res = self.nd.normalizar(u'Suecia y libano')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 182539, u'Suecia', 231716, u'Líbano', 'jose_c_paz', u'José C. Paz')

    def testCalle1UnicaCalle2MuchasCruceExistenteUnico(self):
        res = self.nd.normalizar(u'líbano y Avenida')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 231716, u'Líbano', 78155, u'Avenida Croacia', 'jose_c_paz', u'José C. Paz')

    def testCalle1MuchasCalle2UnicaCruceExistenteUnico(self):
        res = self.nd.normalizar(u'Avenida y líbano')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 78155, u'Avenida Croacia', 231716, u'Líbano', 'jose_c_paz', u'José C. Paz')

    def testCalleConY01(self):
        res = self.nd.normalizar(u'Arias y Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 77242, u'Coronel Arias', 77481, u'Gelly y Obes', 'jose_c_paz', u'José C. Paz')

    def testCalleConY02(self):
        res = self.nd.normalizar(u'Gelly y Obes y Arias')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 77481, u'Gelly y Obes', 77242, u'Coronel Arias', 'jose_c_paz', u'José C. Paz')

    def testCalleConY03(self):
        res = self.nd.normalizar(u'Gel y Ob y Coronel Arias')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 77481, u'Gelly y Obes', 77242, u'Coronel Arias', 'jose_c_paz', u'José C. Paz')

    def testCalleConYParcial01(self):
        res = self.nd.normalizar(u'Arias y Gel y Ob')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 77242, u'Coronel Arias', 77481, u'Gelly y Obes', 'jose_c_paz', u'José C. Paz')

    def testDireccionSeparadaPorE01(self):
        res = self.nd.normalizar(u'pinero e iglesia')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        self._checkDireccion(res[0], 53491, u'Piñero', 53648, u'Iglesias', 'jose_c_paz', u'José C. Paz')

    def testCalle1MuchasCalle2MuchasCruceExistenteMulti(self):
        res = self.nd.normalizar(u'santiago y are')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, 'Deberia haber 2 matchings')
        self._checkDireccion(res[0], 53658, u'Santiago de Compostela', 53565, u'Gral Arenales', 'jose_c_paz', u'José C. Paz')
        self._checkDireccion(res[1], 77662, u'Santiago L. Copello', 53565, u'Gral Arenales', 'jose_c_paz', u'José C. Paz')

    def testCalleConE02(self):
        res = self.nd.normalizar(u'José E. Rodó y Paula Albarracín')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber 1 matchings')
        self._checkDireccion(res[0], 78817, u'José E. Rodó', 52665, u'Paula Albarracín', 'jose_c_paz', u'José C. Paz')

    def testDireccionSeparadaPorECalleNoEmpiezaConI(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'miranda e arregui')
