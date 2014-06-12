# coding: UTF-8
import unittest
import sys, os
from urllib2 import HTTPError
sys.path.append(os.path.join('..','src'))

from NormalizadorDireccionesGBA import *

class NormalizadorGBATestCase(unittest.TestCase):
    nd = NormalizadorDireccionesGBA(include_list=['jose_c_paz','hurlingham','ituzaingo'])

    def testNDGBA_nomalizar_calle_inexistente(self):
        res = self.nd.normalizar('kokusai dori')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 0, u'No debería haber matching.')
        
        
        
#    def testCallejero_buscarCalle_unica_calle_existente(self):
#        res = self.c.buscarCalle(u'Santiago de Compostela')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
#        calle = res[0]
#        self.assertTrue(isinstance(calle, Calle))
#        self.assertEqual(calle.codigo, 30417877)
#        self.assertEqual(calle.nombre, u'Santiago de Compostela')
#        self.assertEqual(calle.partido.codigo, 'jose_c_paz')
#
#    def testCallejero_buscarCalle_nombre_permutado(self):
#        res = self.c.buscarCalle(u'Compostela Santiago de')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
#        calle = res[0]
#        self.assertTrue(isinstance(calle, Calle))
#        self.assertEqual(calle.codigo, 30417877)
#        self.assertEqual(calle.nombre, u'Santiago de Compostela')
#        self.assertEqual(calle.partido.codigo, 'jose_c_paz')
#
#    def testCallejero_buscarCalle_nombre_incompleto(self):
#        res = self.c.buscarCalle(u'Compos Santi')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
#        calle = res[0]
#        self.assertTrue(isinstance(calle, Calle))
#        self.assertEqual(calle.codigo, 30417877)
#        self.assertEqual(calle.nombre, u'Santiago de Compostela')
#        self.assertEqual(calle.partido.codigo, 'jose_c_paz')
#
#    def testCallejero_buscarCalle_nombre_con_acento_y_case(self):
#        res = self.c.buscarCalle(u'PoToSÍ')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
#        calle = res[0]
#        self.assertTrue(isinstance(calle, Calle))
#        self.assertEqual(calle.codigo, 182271149)
#        self.assertEqual(calle.nombre, u'Potosí')
#        self.assertEqual(calle.partido.codigo, 'jose_c_paz')
#
#    def testCallejero_buscarCalle_nombre_con_enie(self):
#        res = self.c.buscarCalle(u'Roque Saenz Peña')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 2, u'Debería haber 2 matching.')
#        calle = res[0]
#        self.assertTrue(isinstance(calle, Calle))
#        self.assertEqual(calle.nombre, u'Roque Sáenz Peña')
#        self.assertEqual(calle.partido.codigo, 'jose_c_paz')
#
#    def testCallejero_buscarCalle_calle_con_varios_tramos(self):
#        res = self.c.buscarCalle(u'Santiago de Liniers')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
#        for calle in res:
#            self.assertTrue(isinstance(calle, Calle))
#            self.assertEqual(calle.nombre, u'Santiago de Liniers')
#    
#    def testCallejero_buscarCalle_multiples_calles_existentes(self):
#        res = self.c.buscarCalle(u'San')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 7, u'Debería haber 7 matchings.')
#        resCalles = [u'San Nicolás', u'Santiago de Compostela', u'San Luis', u'San Lorenzo', u'Santiago del Estero', u'Santiago de Liniers']
#        for calle in res:
#            self.assertTrue(isinstance(calle, Calle))
#            self.assertTrue(calle.nombre in resCalles)
#
#    def testCallejero_buscarCalle_calles_con_y_01(self):
#        res = self.c.buscarCalle(u'Gelly y Obes')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
#        resCalles = [u'Gelly y Obes']
#        for calle in res:
#            self.assertTrue(isinstance(calle, Calle))
#            self.assertTrue(calle.nombre in resCalles)
#            
#        res = self.c.buscarCalle(u'g y o')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
#        resCalles = [u'Gelly y Obes']
#        for calle in res:
#            self.assertTrue(isinstance(calle, Calle))
#            self.assertTrue(calle.nombre in resCalles)
#
#    def testCallejero_buscarCalle_calles_con_y_02(self):
#        res = self.c.buscarCalle(u'Juan de Torres de Vera y Aragon')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
#        self.assertTrue(isinstance(res[0], Calle))
#        self.assertTrue(res[0].nombre == u'Juan de Torres de Vera y Aragon')
#        
#        res = self.c.buscarCalle(u'Ju de To Vera  Ara')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
#        self.assertTrue(isinstance(res[0], Calle))
#        self.assertTrue(res[0].nombre == u'Juan de Torres de Vera y Aragon')
#
#    def testCallejero_buscarCalle_calles_con_y_03(self):
#        res = self.c.buscarCalle(u'Vicente López y Planes')
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
#        self.assertTrue(isinstance(res[0], Calle))
#        self.assertTrue(res[0].nombre == u'Vicente López y Planes')
#
#    def testCallejero_buscarCodigo_codigo_valido(self):
#        res = self.c.buscarCodigo(190141705)
#        self.assertTrue(isinstance(res, list))
#        self.assertTrue(res[0] == 190141705)
#        self.assertTrue(res[1] == u'Avenida Derqui (M) / Fray Antonio Marchena (JCP)')
#
#    def testCallejero_buscarCodigo_codigo_invalido(self):
#        res = self.c.buscarCodigo(666)
#        self.assertTrue(res == None)
#
#    def testCallejero_buscarCalle_sinonimos_01(self):
#        res1 = self.c.buscarCalle(u'11')
#        self.assertTrue(isinstance(res1, list))
#        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
#        res2 = self.c.buscarCalle(u'once')
#        self.assertTrue(isinstance(res2, list))
#        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
#        self.assertEqual(res1[0].codigo,res2[0].codigo)
#
#        res1 = self.c.buscarCalle(u'3')
#        self.assertTrue(isinstance(res1, list))
#        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
#        res2 = self.c.buscarCalle(u'tres')
#        self.assertTrue(isinstance(res2, list))
#        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
#        self.assertEqual(res1[0].codigo,res2[0].codigo)
#
#    def testCallejero_buscarCalle_muchos_espacios(self):
#        res1 = self.c.buscarCalle(u'  puerto    principe         ')
#        self.assertTrue(isinstance(res1, list))
#        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
#        self.assertEqual(res1[0].codigo, 223070537)
#        
#    def testCallejero_buscarCalle_calle_con_parentesis(self):
#        res1 = self.c.buscarCalle(u'montevideo (norte)')
#        self.assertTrue(isinstance(res1, list))
#        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
#        self.assertEqual(res1[0].codigo, 57688378)
#
#    def testCallejero_buscarCalle_caracteres_raros(self):
#        res1 = self.c.buscarCalle(u'puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
#        self.assertTrue(isinstance(res1, list))
#        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
#        self.assertEqual(res1[0].codigo, 223070537)

