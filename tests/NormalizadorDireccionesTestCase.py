# coding: UTF-8

import unittest

from usig_normalizador_amba.NormalizadorDirecciones import NormalizadorDirecciones
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Calle import Calle
from usig_normalizador_amba.Errors import ErrorCalleInexistente

from tests.test_commons import cargarCallejeroEstatico


class NormalizadorDireccionesTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', 'José C. Paz', 'Partido de José C. Paz', 2430431)
    nd = NormalizadorDirecciones(p)
    cargarCallejeroEstatico(nd.c)

    def _checkCalle(self, calle, codigo, nombre, codigo_partido, localidad):
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, codigo)
        self.assertEqual(calle.nombre, nombre)
        self.assertEqual(calle.partido.codigo, codigo_partido)
        self.assertEqual(calle.localidad, localidad)

    def testNormalizador_nomalizar_calle_inexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori')

    def testNormalizador_normalizar_unica_calle_existente(self):
        res = self.nd.normalizar('Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, 'Santiago de Compostela', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_nombre_permutado(self):
        res = self.nd.normalizar('Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, 'Santiago de Compostela', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_nombre_incompleto(self):
        res = self.nd.normalizar('Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, 'Santiago de Compostela', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_nombre_con_acento_y_case(self):
        res = self.nd.normalizar('PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 341221, 'Potosí', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_nombre_con_enie(self):
        res = self.nd.normalizar('Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 77440, 'Roque Sáenz Peña', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_multiples_calles_existentes(self):
        res = self.nd.normalizar('San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, 'Debería haber 10 matchings.')
        resCalles = ['San Lorenzo', 'San Nicolás', 'San Blas', 'San Salvador', 'San Luis', 'San Marino',
                     'San Agustín', 'Santiago del Estero', 'Santiago de Compostela', 'Santiago L. Copello']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testNormalizador_normalizar_calles_con_y_01(self):
        res = self.nd.normalizar('Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matchings.')
        self._checkCalle(res[0], 77481, 'Gelly y Obes', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_calles_con_y_03(self):
        res = self.nd.normalizar('Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matchings.')
        self._checkCalle(res[0], 11702, 'Vicente López y Planes', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_buscarCalle_calles_con_e_01(self):
        res = self.nd.normalizar('Jose e Rodo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 78817, 'José E. Rodó', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_sinonimos_01(self):
        res1 = self.nd.normalizar('11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, 'Debería haber 1 matching.')
        res2 = self.nd.normalizar('once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, 'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, res2[0].codigo)

    def testNormalizador_normalizar_sinonimos_02(self):
        res = self.nd.normalizar('3')  # 3 de Febrero, Tres Sargentos y Las Tres Marías
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 3, 'Debería haber 1 matching.')
        self.assertTrue(res[0].codigo in [78879, 53341, 237007])
        self.assertTrue(res[1].codigo in [78879, 53341, 237007])
        self.assertTrue(res[2].codigo in [78879, 53341, 237007])

    def testNormalizador_normalizar_muchos_espacios(self):
        res = self.nd.normalizar('  puerto    principe         ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, 'Puerto Príncipe', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_calle_con_parentesis(self):
        res = self.nd.normalizar('Coliqueo (JCP)')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 186501, 'Intendente Arricau (SM) / Cacique Coliqueo (JCP)', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_caracteres_raros(self):
        res = self.nd.normalizar('puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, 'Puerto Príncipe', 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_calles_como_av_o_pje(self):
        casos = [
            'Avenida Arribeños',
            'Arribeños avenida',
            'Arribeños avda',
            'AV. Arribeños',
            'Pasaje Arribeños',
            'Psje. Arribeños',
            'Arribeños pje'
        ]
        for caso in casos:
            res = self.nd.normalizar(caso)
            self.assertTrue(isinstance(res, list))
            self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
            self._checkCalle(res[0], 79350, 'Arribeños', 'jose_c_paz', 'José C. Paz')
