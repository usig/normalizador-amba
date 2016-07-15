# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.Callejero import Callejero
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Calle import Calle

from test_commons import cargarCallejeroEstatico


class CallejeroTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    c = Callejero(p)
    cargarCallejeroEstatico(c)

    p = Partido('general_san_martin', u'General San Martin', u'Partido de General San Martin', 1719022)
    c_san_martin = Callejero(p)
    cargarCallejeroEstatico(c_san_martin)

    def _checkCalle(self, calle, codigo, nombre, codigo_partido, localidad):
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, codigo)
        self.assertEqual(calle.nombre, nombre)
        self.assertEqual(calle.partido.codigo, codigo_partido)
        self.assertEqual(calle.localidad, localidad)

    def testCallejero_callejero_inexistent(self):
        p = Partido('jose_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
        self.assertRaises(ValueError, Callejero, p)

    def testCallejero_buscarCalle_calle_inexistente(self):
        res = self.c.buscarCalle('kokusai dori')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 0, u'No debería haber matching.')

    def testCallejero_buscarCalle_unica_calle_existente(self):
        res = self.c.buscarCalle(u'Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, u'Santiago de Compostela', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_nombre_permutado(self):
        res = self.c.buscarCalle(u'Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, u'Santiago de Compostela', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_nombre_incompleto(self):
        res = self.c.buscarCalle(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, u'Santiago de Compostela', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_nombre_con_acento_y_case(self):
        res = self.c.buscarCalle(u'PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 341221, u'Potosí', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_nombre_con_enie(self):
        res = self.c.buscarCalle(u'Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 77440, u'Roque Sáenz Peña', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_multiples_calles_existentes(self):
        res = self.c.buscarCalle(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 16, u'Debería haber 16 matchings.')
        resCalles = [u'San Lorenzo', u'San Nicolás', u'San Blas', u'San Salvador', u'San Luis', u'San Marino', u'San Agustín',
                     u'Santiago del Estero', u'Santiago de Compostela', u'Santiago L. Copello', u'Santa Marta', u'Santo Domingo',
                     u'Santa Ana', u'Santiago de Liniers', u'Santa María', u'Santiago Davobe']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testCallejero_buscarCalle_calles_con_y_01(self):
        res = self.c.buscarCalle(u'Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self._checkCalle(res[0], 77481, u'Gelly y Obes', 'jose_c_paz', u'José C. Paz')

        res = self.c.buscarCalle(u'g y o')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self._checkCalle(res[0], 77481, u'Gelly y Obes', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_calles_con_y_02(self):
        res = self.c.buscarCalle(u'Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self._checkCalle(res[0], 11702, u'Vicente López y Planes', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_calles_con_e_01(self):
        res = self.c.buscarCalle(u'Jose e Rodo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 78817, u'José E. Rodó', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCodigo_codigo_valido(self):
        res = self.c.buscarCodigo(314724)
        self.assertTrue(isinstance(res, list))
        self.assertTrue(res[0][0] == 314724)
        self.assertTrue(res[0][1] == u'Avenida Derqui (M) / Fray Antonio Marchena (JCP)')

    def testCallejero_buscarCodigo_codigo_invalido(self):
        res = self.c.buscarCodigo(666)
        self.assertTrue(res == [])

    def testCallejero_buscarCalle_sinonimos_01(self):
        res1 = self.c.buscarCalle(u'11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.c.buscarCalle(u'once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, res2[0].codigo)

    def testCallejero_buscarCalle_sinonimos_02(self):
        res1 = self.c.buscarCalle(u'3')  # 3 de Febrero, Tres Sargentos y Las Tres Marías
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 3, u'Debería haber 1 matching.')
        self.assertTrue(res1[0].codigo in [78879, 53341, 237007])
        self.assertTrue(res1[1].codigo in [78879, 53341, 237007])
        self.assertTrue(res1[2].codigo in [78879, 53341, 237007])

    def testCallejero_buscarCalle_muchos_espacios(self):
        res = self.c.buscarCalle(u'  puerto    principe         ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, u'Puerto Príncipe', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_calle_con_parentesis(self):
        res = self.c.buscarCalle(u'Coliqueo (JCP)')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 186501, u'Intendente Arricau (SM) / Cacique Coliqueo (JCP)', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_caracteres_raros(self):
        res = self.c.buscarCalle(u'puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, u'Puerto Príncipe', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_calle_con_acente_escrito_sin_acento(self):
        res = self.c.buscarCalle(u'potosi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 341221, u'Potosí', 'jose_c_paz', u'José C. Paz')

    def testCallejero_buscarCalle_calle_con_numeros(self):
        res = self.c_san_martin.buscarCalle(u'26 de Julio de 1890')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self._checkCalle(res[0], 70996, u'103 - 26 de Julio de 1890', 'general_san_martin', u'General San Martín')
