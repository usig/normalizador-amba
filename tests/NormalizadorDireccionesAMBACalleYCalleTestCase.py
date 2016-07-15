# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.Errors import ErrorCruceInexistente, ErrorCalleInexistente
from usig_normalizador_amba.settings import CALLE_Y_CALLE

from test_commons import cargarCallejeroEstatico


class NormalizadorDireccionesAMBACalleYCalleTestCase(unittest.TestCase):
    partidos = ['hurlingham', 'ituzaingo', 'jose_c_paz', 'la_matanza', 'san_isidro', 'san_miguel']
    nd = NormalizadorDireccionesAMBA(include_list=partidos)
    for n in nd.normalizadores:
        cargarCallejeroEstatico(n.c)

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

    def testDireccionExistentePeroEnOtroPartido(self):
        res = self.nd.normalizar(u'Europa y Darwin, Ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 6895, u'Europa', 6953, u'Darwin', 'ituzaingo',  u'Ituzaingó')

        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'Europa y Darwin, La Matanza')

    def testDireccionExistentePeroEnOtraLocalidad(self):
        res = self.nd.normalizar(u'Europa y Darwin, Ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 6895, u'Europa', 6953, u'Darwin', 'ituzaingo',  u'Ituzaingó')

        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'Europa y Darwin, Villa Udaondo')

    def testNormalizador_DireccionEnVariosPartidos(self):
        res = self.nd.normalizar(u'san martin y peron')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 46673, u'Avenida General San Martín', 82054, u'Av. Eva Perón', 'la_matanza', u'Ramos Mejia')
        self._checkDireccion(res[1], 12124, u'General José de San Martín', 293550, u'Avenida Eva Duarte de Perón', 'san_miguel', u'Campo de Mayo')

    def testNormalizador_PartidoConNumero(self):
        res = self.nd.normalizar(u'Pablo Ceretti y Jorge Cardassy, 20 de Junio')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 232752, u'Pablo Ceretti', 232731, u'Jorge Cardassy', 'la_matanza', u'20 de Junio')
