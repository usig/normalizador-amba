# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDirecciones import NormalizadorDirecciones
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Calle import Calle
from usig_normalizador_amba.Errors import ErrorCalleInexistente

from test_commons import cargarCallejeroEstatico


class NormalizadorDireccionesTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
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
        res = self.nd.normalizar(u'Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, u'Santiago de Compostela', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_nombre_permutado(self):
        res = self.nd.normalizar(u'Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, u'Santiago de Compostela', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_nombre_incompleto(self):
        res = self.nd.normalizar(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, u'Santiago de Compostela', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_nombre_con_acento_y_case(self):
        res = self.nd.normalizar(u'PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 341221, u'Potosí', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_nombre_con_enie(self):
        res = self.nd.normalizar(u'Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 77440, u'Roque Sáenz Peña', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_multiples_calles_existentes(self):
        res = self.nd.normalizar(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, u'Debería haber 10 matchings.')
        resCalles = [u'San Lorenzo', u'San Nicolás', u'San Blas', u'San Salvador', u'San Luis', u'San Marino',
                     u'San Agustín', u'Santiago del Estero', u'Santiago de Compostela', u'Santiago L. Copello']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testNormalizador_normalizar_calles_con_y_01(self):
        res = self.nd.normalizar(u'Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self._checkCalle(res[0], 77481, u'Gelly y Obes', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_calles_con_y_03(self):
        res = self.nd.normalizar(u'Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self._checkCalle(res[0], 11702, u'Vicente López y Planes', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_buscarCalle_calles_con_e_01(self):
        res = self.nd.normalizar(u'Jose e Rodo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 78817, u'José E. Rodó', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_sinonimos_01(self):
        res1 = self.nd.normalizar(u'11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.nd.normalizar(u'once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, res2[0].codigo)

    def testNormalizador_normalizar_sinonimos_02(self):
        res = self.nd.normalizar(u'3')  # 3 de Febrero, Tres Sargentos y Las Tres Marías
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 3, u'Debería haber 1 matching.')
        self.assertTrue(res[0].codigo in [78879, 53341, 237007])
        self.assertTrue(res[1].codigo in [78879, 53341, 237007])
        self.assertTrue(res[2].codigo in [78879, 53341, 237007])

    def testNormalizador_normalizar_muchos_espacios(self):
        res = self.nd.normalizar(u'  puerto    principe         ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, u'Puerto Príncipe', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_calle_con_parentesis(self):
        res = self.nd.normalizar(u'Coliqueo (JCP)')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 186501, u'Intendente Arricau (SM) / Cacique Coliqueo (JCP)', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_caracteres_raros(self):
        res = self.nd.normalizar(u'puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, u'Puerto Príncipe', 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_calles_como_av_o_pje(self):
        casos = [
            u'Avenida Arribeños',
            u'Arribeños avenida',
            u'Arribeños avda',
            u'AV. Arribeños',
            u'Pasaje Arribeños',
            u'Psje. Arribeños',
            u'Arribeños pje'
        ]
        for caso in casos:
            res = self.nd.normalizar(caso)
            self.assertTrue(isinstance(res, list))
            self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
            self._checkCalle(res[0], 79350, u'Arribeños', 'jose_c_paz', u'José C. Paz')
