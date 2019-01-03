# coding: UTF-8

import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.Errors import ErrorCruceInexistente, ErrorCalleInexistente
from usig_normalizador_amba.settings import CALLE_Y_CALLE

from tests.test_commons import cargarCallejeroEstatico


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
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'Elm street y Roque Sáenz Peña')

    def testCalleInexistente02(self):
        self.assertRaises(ErrorCruceInexistente, self.nd.normalizar, 'Roque Sáenz Peña y kokusai dori')

    def testDireccionExistentePeroEnOtroPartido(self):
        res = self.nd.normalizar('Europa y Darwin, Ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 6895, 'Europa', 6953, 'Darwin', 'ituzaingo',  'Ituzaingó')

        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'Europa y Darwin, La Matanza')

    def testDireccionExistentePeroEnOtraLocalidad(self):
        res = self.nd.normalizar('Europa y Darwin, Ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 6895, 'Europa', 6953, 'Darwin', 'ituzaingo',  'Ituzaingó')

        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'Europa y Darwin, Villa Udaondo')

    def testNormalizador_DireccionEnVariosPartidos(self):
        res = self.nd.normalizar('san martin y peron')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, 'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 46673, 'Avenida General San Martín', 82054, 'Av. Eva Perón', 'la_matanza', 'Ramos Mejia')
        self._checkDireccion(res[1], 12124, 'General José de San Martín', 293550, 'Avenida Eva Duarte de Perón', 'san_miguel', 'Campo de Mayo')

    def testNormalizador_PartidoConNumero(self):
        res = self.nd.normalizar('Pablo Ceretti y Jorge Cardassy, 20 de Junio')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 232752, 'Pablo Ceretti', 232731, 'Jorge Cardassy', 'la_matanza', '20 de Junio')
