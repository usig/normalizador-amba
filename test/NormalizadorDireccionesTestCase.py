# coding: UTF-8
import unittest
import sys, os
import simplejson as json
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from NormalizadorDirecciones import *
from Partido import Partido
from Calle import Calle
from Errors import *

class NormalizadorDireccionesTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    nd = NormalizadorDirecciones(p)

    # Cargo los callejeros congelados
    with open('callejeros/jose_c_paz.callejero') as data_file:
        data = json.load(data_file)
    nd.c.data = data
    nd.c.data.sort()
    nd.c.osm_ids = [k[0] for k in nd.c.data]

    def testNormalizador_nomalizar_calle_inexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori')
        
    def testNormalizador_normalizar_unica_calle_existente(self):
        res = self.nd.normalizar(u'Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 53658)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_permutado(self):
        res = self.nd.normalizar(u'Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 53658)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_incompleto(self):
        res = self.nd.normalizar(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 53658)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_con_acento_y_case(self):
        res = self.nd.normalizar(u'PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 341221)
        self.assertEqual(calle.nombre, u'Potosí')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_nombre_con_enie(self):
        res = self.nd.normalizar(u'Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.nombre, u'Roque Sáenz Peña')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_normalizar_multiples_calles_existentes(self):
        res = self.nd.normalizar(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, u'Debería haber 10 matchings.')
        resCalles = [u'San Lorenzo',u'San Nicolás',u'San Blas',u'San Salvador',u'San Luis',u'San Marino',
                     u'San Agustín',u'Santiago del Estero',u'Santiago de Compostela',u'Santiago L. Copello']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testNormalizador_normalizar_calles_con_y_01(self):
        res = self.nd.normalizar(u'Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        resCalles = [u'Gelly y Obes']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)
            
    def testNormalizador_normalizar_calles_con_y_03(self):
        res = self.nd.normalizar(u'Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Vicente López y Planes')

    def testNormalizador_buscarCalle_calles_con_e_01(self):
        res = self.nd.normalizar(u'Jose e Rodo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].codigo == 78817) #José E. Rodó

    def testNormalizador_normalizar_sinonimos_01(self):
        res1 = self.nd.normalizar(u'11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.nd.normalizar(u'once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo,res2[0].codigo)

    def testNormalizador_normalizar_sinonimos_02(self):
        res1 = self.nd.normalizar(u'3') # 3 de Febrero, Tres Sargentos y Las Tres Marías
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 3, u'Debería haber 1 matching.')
        self.assertTrue(res1[0].codigo in [78879,53341,237007])
        self.assertTrue(res1[1].codigo in [78879,53341,237007])
        self.assertTrue(res1[2].codigo in [78879,53341,237007])

    def testNormalizador_normalizar_muchos_espacios(self):
        res1 = self.nd.normalizar(u'  puerto    principe         ')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 183044)
        
    def testNormalizador_normalizar_calle_con_parentesis(self):
        res1 = self.nd.normalizar(u'Coliqueo (JCP)')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 186501) #Intendente Arricau (SM) / Cacique Coliqueo (JCP)

    def testNormalizador_normalizar_caracteres_raros(self):
        res1 = self.nd.normalizar(u'puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 183044)
