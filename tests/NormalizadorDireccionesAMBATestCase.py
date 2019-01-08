# coding: UTF-8

import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Calle import Calle
from usig_normalizador_amba.Errors import ErrorCalleInexistente

from tests.test_commons import cargarCallejeroEstatico


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
        res = self.nd.normalizar('acevedo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 5, 'Debería haber 5 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 52498, 'Acevedo Eduardo', 'hurlingham', 'Hurlingham')
        self._checkCalle(res[1], 174423, 'Manuel Acevedo', 'ituzaingo', 'Ituzaingó')
        self._checkCalle(res[2], 46174, 'Acevedo', 'la_matanza', 'Lomas del Mirador')
        self._checkCalle(res[3], 46346, 'Acevedo', 'la_matanza', 'La Tablada')
        self._checkCalle(res[4], 49987, 'Padre Acevedo', 'san_isidro', 'Beccar')

    def testNormalizador_NormalizarCalleExistentePorPartido01(self):
        res = self.nd.normalizar('acevedo, hurlingham')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 52498, 'Acevedo Eduardo', 'hurlingham', 'Hurlingham')

        res = self.nd.normalizar('acevedo, hur')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 52498, 'Acevedo Eduardo', 'hurlingham', 'Hurlingham')

    def testNormalizador_NormalizarCalleExistentePorPartido02(self):
        res = self.nd.normalizar('acevedo, ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, 'Manuel Acevedo', 'ituzaingo', 'Ituzaingó')

        res = self.nd.normalizar('acevedo, itu')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, 'Manuel Acevedo', 'ituzaingo', 'Ituzaingó')

    def testNormalizador_NormalizarCalleExistentePorPartido03(self):
        res = self.nd.normalizar('acevedo, Beccar')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 49987, 'Padre Acevedo', 'san_isidro', 'Beccar')

        res = self.nd.normalizar('acevedo, padre')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 49987, 'Padre Acevedo', 'san_isidro', 'Beccar')

    def testNormalizador_NormalizarNombresPermutado(self):
        res = self.nd.normalizar('acevedo manuel, ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, 'Manuel Acevedo', 'ituzaingo', 'Ituzaingó')

    def testNormalizador_NormalizarNombreIncompleto(self):
        res = self.nd.normalizar('Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 53658, 'Santiago de Compostela', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_NormalizarNombreConAcentoYCase(self):
        res = self.nd.normalizar('PoToSÍ, José')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 341221, 'Potosí', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_NormalizarNombreConEnie(self):
        res = self.nd.normalizar('Roque Saenz Peña, Jose')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 77440, 'Roque Sáenz Peña', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_NormalizarCallesConY_01(self):
        res = self.nd.normalizar('Gelly y Obes, Jose C Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 77481, 'Gelly y Obes', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_NormalizarCalleConComa_01(self):
        res = self.nd.normalizar('Acevedo, Manuel, Ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, 'Manuel Acevedo', 'ituzaingo', 'Ituzaingó')

    def testNormalizador_NormalizarCalleConComa_02(self):
        res = self.nd.normalizar('Acevedo, Manuel')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 174423, 'Manuel Acevedo', 'ituzaingo', 'Ituzaingó')

    def testNormalizador_NormalizarCalleConComa_03(self):
        res = self.nd.normalizar('O\'Higgins, San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, 'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self._checkCalle(res[0], 15350, 'O\'Higgins', 'san_isidro', 'San Isidro')
        self._checkCalle(res[1], 79669, 'O\'Higgins', 'san_miguel', 'Bella Vista')

    def testNormalizador_NormalizarConLimite(self):
        res = self.nd.normalizar('San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, 'Debería haber 10 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar('San', 25)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 25, 'Debería haber 25 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar('San', 200)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 170, 'Debería haber 170 matching/s. Hay {0}'.format(len(res)))
