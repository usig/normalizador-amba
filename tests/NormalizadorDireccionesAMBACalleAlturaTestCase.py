# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.Errors import ErrorCalleInexistente

from test_commons import cargarCallejeroEstatico


class NormalizadorDireccionesAMBACalleAlturaTestCase(unittest.TestCase):
    partidos = ['almirante_brown', 'jose_c_paz', 'lomas_de_zamora', 'quilmes', 'san_isidro', 'vicente_lopez']
    nd = NormalizadorDireccionesAMBA(include_list=partidos)
    for n in nd.normalizadores:
        cargarCallejeroEstatico(n.c)

    def _checkDireccion(self, direccion, codigo, nombre, altura, codigo_partido, localidad):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.calle.codigo, codigo)
        self.assertEqual(direccion.calle.nombre, nombre)
        self.assertEqual(direccion.altura, altura)
        self.assertEqual(direccion.partido.codigo, codigo_partido)
        self.assertEqual(direccion.localidad, localidad)

    def testNormalizador_NomalizarCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori 1865')

    def testNormalizador_NomalizarDireccionInexistenteEnPartido(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'O\'Higgins 1479, Lomas de Zamora')

    def testNormalizador_RestaurantDeLosKao(self):
        res = self.nd.normalizar(u'O\'Higgins 1479, Florida')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 4882, u'O\'Higgins', 1479, 'vicente_lopez', u'Florida')

    def testNormalizador_DireccionEnVariosPartidos(self):
        res = self.nd.normalizar(u'pavón 4450')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0], 278904, u'Pavón', 4450, 'jose_c_paz', u'José C. Paz')
        self._checkDireccion(res[1], 214876, u'Diagonal Pavón', 4450, 'vicente_lopez', u'Florida Oeste')
