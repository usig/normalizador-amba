# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Calle import Calle
from usig_normalizador_amba.Errors import ErrorCalleInexistente

from test_commons import cargarCallejeroEstatico


class NormalizadorDireccionesAMBATestCase(unittest.TestCase):
    partidos = ['hurlingham', 'ituzaingo', 'jose_c_paz', 'la_matanza', 'san_isidro', 'san_miguel']
    nd = NormalizadorDireccionesAMBA(include_list=partidos)
    for n in nd.normalizadores:
        cargarCallejeroEstatico(n.c)

    def _checkCalle(self, calle, codigo, nombre, codigo_partido, localidad):
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, codigo)
        self.assertEqual(calle.nombre, nombre)
        self.assertEqual(calle.partido.codigo, codigo_partido)
        self.assertEqual(calle.localidad, localidad)

    def testNormalizador_NomalizarCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori')

    def testNormalizador_NormalizarCalleExistenteBusquedaEnTodosLosPartidos(self):
        res = self.nd.normalizar(u'acevedo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 5, u'Debería haber 5 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 52498, u'Acevedo Eduardo', 'hurlingham', u'Hurlingham')
        self._checkCalle(res[1], 174423, u'Manuel Acevedo', 'ituzaingo', u'Ituzaingó')
        self._checkCalle(res[2], 46174, u'Acevedo', 'la_matanza', u'Lomas del Mirador')
        self._checkCalle(res[3], 46346, u'Acevedo', 'la_matanza', u'La Tablada')
        self._checkCalle(res[4], 49987, u'Padre Acevedo', 'san_isidro', u'Beccar')

    def testNormalizador_NormalizarCalleExistentePorPartido01(self):
        res = self.nd.normalizar(u'acevedo, hurlingham')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 52498, u'Acevedo Eduardo', 'hurlingham', u'Hurlingham')

        res = self.nd.normalizar(u'acevedo, hur')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 52498, u'Acevedo Eduardo', 'hurlingham', u'Hurlingham')

    def testNormalizador_NormalizarCalleExistentePorPartido02(self):
        res = self.nd.normalizar(u'acevedo, ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, u'Manuel Acevedo', 'ituzaingo', u'Ituzaingó')

        res = self.nd.normalizar(u'acevedo, itu')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, u'Manuel Acevedo', 'ituzaingo', u'Ituzaingó')

    def testNormalizador_NormalizarCalleExistentePorPartido03(self):
        res = self.nd.normalizar(u'acevedo, Beccar')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 49987, u'Padre Acevedo', 'san_isidro', u'Beccar')

        res = self.nd.normalizar(u'acevedo, padre')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 49987, u'Padre Acevedo', 'san_isidro', u'Beccar')

    def testNormalizador_NormalizarNombresPermutado(self):
        res = self.nd.normalizar(u'acevedo manuel, ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, u'Manuel Acevedo', 'ituzaingo', u'Ituzaingó')

    def testNormalizador_NormalizarNombreIncompleto(self):
        res = self.nd.normalizar(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 53658, u'Santiago de Compostela', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_NormalizarNombreConAcentoYCase(self):
        res = self.nd.normalizar(u'PoToSÍ, José')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 341221, u'Potosí', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_NormalizarNombreConEnie(self):
        res = self.nd.normalizar(u'Roque Saenz Peña, Jose')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 77440, u'Roque Sáenz Peña', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_NormalizarCallesConY_01(self):
        res = self.nd.normalizar(u'Gelly y Obes, Jose C Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 77481, u'Gelly y Obes', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_NormalizarCalleConComa_01(self):
        res = self.nd.normalizar(u'Acevedo, Manuel, Ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, u'Manuel Acevedo', 'ituzaingo', u'Ituzaingó')

    def testNormalizador_NormalizarCalleConComa_02(self):
        res = self.nd.normalizar(u'Acevedo, Manuel')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, u'Manuel Acevedo', 'ituzaingo', u'Ituzaingó')

    def testNormalizador_NormalizarCalleConComa_03(self):
        res = self.nd.normalizar(u'O\'Higgins, San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 15350, u'O\'Higgins', 'san_isidro', u'San Isidro')
        self._checkCalle(res[1], 79669, u'O\'Higgins', 'san_miguel', u'Bella Vista')

    def testNormalizador_NormalizarConLimite(self):
        res = self.nd.normalizar(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, u'Debería haber 10 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar(u'San', 25)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 25, u'Debería haber 25 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar(u'San', 200)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 170, u'Debería haber 170 matching/s. Hay {0}'.format(len(res)))
