# coding: UTF-8
import unittest
import sys, os
from urllib2 import HTTPError
import simplejson as json
from simplejson import JSONDecodeError
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from Callejero import Callejero
from Partido import Partido
from Calle import Calle
from Errors import *

class CallejeroTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    c = Callejero(p)
    p = Partido('general_san_martin', u'General San Martin', u'Partido de General San Martin', 1719022)
    c_san_martin = Callejero(p)
    
    # Cargo los callejeros congelados
    with open('callejeros/jose_c_paz.callejero') as data_file:
        data = json.load(data_file)
    c.data = data
    c.data.sort()
    c.osm_ids = [k[0] for k in c.data]
    
    with open('callejeros/general_san_martin.callejero') as data_file:
        data = json.load(data_file)
    c_san_martin.data = data
    c_san_martin.data.sort()
    c_san_martin.osm_ids = [k[0] for k in c_san_martin.data]

    def testCallejero_callejero_inexistent(self):
        p = Partido('jose_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
        self.assertRaises(JSONDecodeError, Callejero, p)
            
    def testCallejero_buscarCalle_calle_inexistente(self):
        res = self.c.buscarCalle('kokusai dori')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 0, u'No debería haber matching.')
        
    def testCallejero_buscarCalle_unica_calle_existente(self):
        res = self.c.buscarCalle(u'Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 53658)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_buscarCalle_nombre_permutado(self):
        res = self.c.buscarCalle(u'Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 53658)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_buscarCalle_nombre_incompleto(self):
        res = self.c.buscarCalle(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 53658)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_buscarCalle_nombre_con_acento_y_case(self):
        res = self.c.buscarCalle(u'PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 341221)
        self.assertEqual(calle.nombre, u'Potosí')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_buscarCalle_nombre_con_enie(self):
        res = self.c.buscarCalle(u'Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.nombre, u'Roque Sáenz Peña')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_buscarCalle_multiples_calles_existentes(self):
        res = self.c.buscarCalle(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 16, u'Debería haber 16     matchings.')
        resCalles = [u'San Lorenzo',u'San Nicolás',u'San Blas',u'San Salvador',u'San Luis',u'San Marino',u'San Agustín',
                     u'Santiago del Estero',u'Santiago de Compostela',u'Santiago L. Copello',u'Santa Marta',u'Santo Domingo',
                     u'Santa Ana',u'Santiago de Liniers',u'Santa María',u'Santiago Davobe']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testCallejero_buscarCalle_calles_con_y_01(self):
        res = self.c.buscarCalle(u'Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertEqual(res[0].nombre, u'Gelly y Obes')
        self.assertEqual(res[0].codigo, 77481)
        
        res = self.c.buscarCalle(u'g y o')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertEqual(res[0].nombre, u'Gelly y Obes')
        self.assertEqual(res[0].codigo, 77481)

    def testCallejero_buscarCalle_calles_con_y_02(self):
        res = self.c.buscarCalle(u'Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Vicente López y Planes')

    def testCallejero_buscarCalle_calles_con_e_01(self):
        res = self.c.buscarCalle(u'Jose e Rodo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].codigo == 78817) #José E. Rodó

    def testCallejero_buscarCodigo_codigo_valido(self):
        res = self.c.buscarCodigo(314724)
        self.assertTrue(isinstance(res, list))
        self.assertTrue(res[0] == 314724)
        self.assertTrue(res[1] == u'Avenida Derqui (M) / Fray Antonio Marchena (JCP)')

    def testCallejero_buscarCodigo_codigo_invalido(self):
        res = self.c.buscarCodigo(666)
        self.assertTrue(res == None)

    def testCallejero_buscarCalle_sinonimos_01(self):
        res1 = self.c.buscarCalle(u'11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.c.buscarCalle(u'once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo,res2[0].codigo)

    def testCallejero_buscarCalle_sinonimos_02(self):
        res1 = self.c.buscarCalle(u'3') # 3 de Febrero, Tres Sargentos y Las Tres Marías
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 3, u'Debería haber 1 matching.')
        self.assertTrue(res1[0].codigo in [78879,53341,237007])
        self.assertTrue(res1[1].codigo in [78879,53341,237007])
        self.assertTrue(res1[2].codigo in [78879,53341,237007])

    def testCallejero_buscarCalle_muchos_espacios(self):
        res1 = self.c.buscarCalle(u'  puerto    principe         ')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 183044)
        
    def testCallejero_buscarCalle_calle_con_parentesis(self):
        res = self.c.buscarCalle(u'Coliqueo (JCP)')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self.assertEqual(res[0].codigo, 186501) #Intendente Arricau (SM) / Cacique Coliqueo (JCP)

    def testCallejero_buscarCalle_caracteres_raros(self):
        res1 = self.c.buscarCalle(u'puerto principe |°¬!#$%&/()=?\¿¡*¸+~{[^}]\'`-_.:,;<>·@')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 183044)

    def testCallejero_buscarCalle_calle_con_acente_escrito_sin_acento(self):
        res1 = self.c.buscarCalle(u'potosi')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo, 341221) #Potosí

    def testCallejero_buscarCalle_calle_con_numeros(self):
        res = self.c_san_martin.buscarCalle(u'26 de Julio de 1890')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self.assertEqual(res[0].codigo, 70996) #26 de Julio de 1890, General San Martin

