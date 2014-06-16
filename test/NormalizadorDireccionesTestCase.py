# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','src'))

from NormalizadorDirecciones import *
from Partido import Partido
from Calle import Calle
from Errors import *

class NormalizadorDireccionesTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    nd = NormalizadorDirecciones(p)

    def testNormalizador_nomalizar_calle_inexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori')
        
    def testNormalizador_normalizar_unica_calle_existente(self):
        res = self.nd.normalizar(u'Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 30417877)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_permutado(self):
        res = self.nd.normalizar(u'Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 30417877)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_incompleto(self):
        res = self.nd.normalizar(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 30417877)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_con_acento_y_case(self):
        res = self.nd.normalizar(u'PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 182271149)
        self.assertEqual(calle.nombre, u'Potosí')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_con_enie(self):
        res = self.nd.normalizar(u'Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.nombre, u'Roque Sáenz Peña')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_calle_con_varios_tramos(self):
        res = self.nd.normalizar(u'Santiago de Liniers')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertEqual(calle.nombre, u'Santiago de Liniers')
    
    def testNormalizador_normalizar_multiples_calles_existentes(self):
        res = self.nd.normalizar(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 7, u'Debería haber 7 matchings.')
        resCalles = [u'San Nicolás', u'Santiago de Compostela', u'San Luis', u'San Lorenzo', u'Santiago del Estero', u'Santiago de Liniers']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testNormalizador_normalizar_calles_con_y_01(self):
        res = self.nd.normalizar(u'Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
        resCalles = [u'Gelly y Obes']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)
            
    def testNormalizador_normalizar_calles_con_y_02(self):
        res = self.nd.normalizar(u'Juan de Torres de Vera y Aragon')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Juan de Torres de Vera y Aragon')
        
        res = self.nd.normalizar(u'Ju de To Vera  Ara')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Juan de Torres de Vera y Aragon')

    def testNormalizador_normalizar_calles_con_y_03(self):
        res = self.nd.normalizar(u'Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Vicente López y Planes')

    def testNormalizador_normalizar_sinonimos_01(self):
        res1 = self.nd.normalizar(u'11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.nd.normalizar(u'once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo,res2[0].codigo)

        res1 = self.nd.normalizar(u'3')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.nd.normalizar(u'tres')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo,res2[0].codigo)

    def testNormalizador_normalizar_muchos_espacios(self):
        res1 = self.nd.normalizar(u'  puerto    principe         ')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 223070537)
        
    def testNormalizador_normalizar_calle_con_parentesis(self):
        res1 = self.nd.normalizar(u'montevideo (norte)')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 57688378)

    def testNormalizador_normalizar_caracteres_raros(self):
        res1 = self.nd.normalizar(u'puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 223070537)
