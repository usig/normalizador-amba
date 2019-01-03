# coding: UTF-8

import unittest

from usig_normalizador_amba.Callejero import Callejero
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Calle import Calle

from tests.test_commons import cargarCallejeroEstatico


class CallejeroTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', 'José C. Paz', 'Partido de José C. Paz', 2430431)
    c = Callejero(p)
    cargarCallejeroEstatico(c)

    p = Partido('general_san_martin', 'General San Martin', 'Partido de General San Martin', 1719022)
    c_san_martin = Callejero(p)
    cargarCallejeroEstatico(c_san_martin)

    def _checkCalle(self, calle, codigo, nombre, codigo_partido, localidad):
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, codigo)
        self.assertEqual(calle.nombre, nombre)
        self.assertEqual(calle.partido.codigo, codigo_partido)
        self.assertEqual(calle.localidad, localidad)

    def testCallejero_callejero_inexistent(self):
        p = Partido('jose_paz', 'José C. Paz', 'Partido de José C. Paz', 2430431)
        self.assertRaises(ValueError, Callejero, p)

    def testCallejero_buscarCalle_calle_inexistente(self):
        res = self.c.buscarCalle('kokusai dori')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 0, 'No debería haber matching.')

    def testCallejero_buscarCalle_unica_calle_existente(self):
        res = self.c.buscarCalle('Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, 'Santiago de Compostela', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_nombre_permutado(self):
        res = self.c.buscarCalle('Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, 'Santiago de Compostela', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_nombre_incompleto(self):
        res = self.c.buscarCalle('Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 53658, 'Santiago de Compostela', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_nombre_con_acento_y_case(self):
        res = self.c.buscarCalle('PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 solo matching.')
        self._checkCalle(res[0], 341221, 'Potosí', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_nombre_con_enie(self):
        res = self.c.buscarCalle('Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 77440, 'Roque Sáenz Peña', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_multiples_calles_existentes(self):
        res = self.c.buscarCalle('San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 16, 'Debería haber 16 matchings.')
        resCalles = ['San Lorenzo', 'San Nicolás', 'San Blas', 'San Salvador', 'San Luis', 'San Marino', 'San Agustín',
                     'Santiago del Estero', 'Santiago de Compostela', 'Santiago L. Copello', 'Santa Marta', 'Santo Domingo',
                     'Santa Ana', 'Santiago de Liniers', 'Santa María', 'Santiago Davobe']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testCallejero_buscarCalle_calles_con_y_01(self):
        res = self.c.buscarCalle('Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matchings.')
        self._checkCalle(res[0], 77481, 'Gelly y Obes', 'jose_c_paz', 'José C. Paz')

        res = self.c.buscarCalle('g y o')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matchings.')
        self._checkCalle(res[0], 77481, 'Gelly y Obes', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_calles_con_y_02(self):
        res = self.c.buscarCalle('Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matchings.')
        self._checkCalle(res[0], 11702, 'Vicente López y Planes', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_calles_con_e_01(self):
        res = self.c.buscarCalle('Jose e Rodo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 78817, 'José E. Rodó', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCodigo_codigo_valido(self):
        res = self.c.buscarCodigo(314724)
        self.assertTrue(isinstance(res, list))
        self.assertTrue(res[0][0] == 314724)
        self.assertTrue(res[0][1] == 'Avenida Derqui (M) / Fray Antonio Marchena (JCP)')

    def testCallejero_buscarCodigo_codigo_invalido(self):
        res = self.c.buscarCodigo(666)
        self.assertTrue(res == [])

    def testCallejero_buscarCalle_sinonimos_01(self):
        res1 = self.c.buscarCalle('11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, 'Debería haber 1 matching.')
        res2 = self.c.buscarCalle('once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, 'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, res2[0].codigo)

    def testCallejero_buscarCalle_sinonimos_02(self):
        res1 = self.c.buscarCalle('3')  # 3 de Febrero, Tres Sargentos y Las Tres Marías
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 3, 'Debería haber 1 matching.')
        self.assertTrue(res1[0].codigo in [78879, 53341, 237007])
        self.assertTrue(res1[1].codigo in [78879, 53341, 237007])
        self.assertTrue(res1[2].codigo in [78879, 53341, 237007])

    def testCallejero_buscarCalle_muchos_espacios(self):
        res = self.c.buscarCalle('  puerto    principe         ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, 'Puerto Príncipe', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_calle_con_parentesis(self):
        res = self.c.buscarCalle('Coliqueo (JCP)')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 186501, 'Intendente Arricau (SM) / Cacique Coliqueo (JCP)', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_caracteres_raros(self):
        res = self.c.buscarCalle('puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 183044, 'Puerto Príncipe', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_calle_con_acente_escrito_sin_acento(self):
        res = self.c.buscarCalle('potosi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 341221, 'Potosí', 'jose_c_paz', 'José C. Paz')

    def testCallejero_buscarCalle_calle_con_numeros(self):
        res = self.c_san_martin.buscarCalle('26 de Julio de 1890')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
        self._checkCalle(res[0], 70996, '103 - 26 de Julio de 1890', 'general_san_martin', 'General San Martín')
