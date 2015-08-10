# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from NormalizadorDireccionesAMBA import *
from Partido import Partido
from Calle import Calle
from Errors import *

class NormalizadorDireccionesAMBACalleYCalleTestCase(unittest.TestCase):
    partidos = ['hurlingham','ituzaingo','jose_c_paz','san_isidro','san_miguel']
    nd = NormalizadorDireccionesAMBA(include_list=partidos)
    for n in nd.normalizadores:
        with open('callejeros/{0}.callejero'.format(n.partido.codigo)) as data_file:
            data = json.load(data_file)
        n.c.data = data
        n.c.data.sort()
        n.c.osm_ids = [k[0] for k in n.c.data]

    def testNormalizador_NomalizarCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori')
            
    def testNormalizador_NormalizarCalleExistenteEnTodoPartidos(self):
        res = self.nd.normalizar(u'acevedo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 3, u'Debería haber 3 matching/s. Hay {0}'.format(len(res)))
        partidos = set()
        self.assertIn('hurlingham', partidos)
        self.assertIn('ituzaingo', partidos)
        self.assertIn('san_isidro', partidos)

    def testNormalizador_NormalizarCalleExistentePorPartido01(self):
        res = self.nd.normalizar(u'acevedo, hurlingham')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 52498) #Acevedo Eduardo        
        self.assertEqual(res[0].partido.codigo, 'hurlingham')        

        res = self.nd.normalizar(u'acevedo, hur')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 52498) #Acevedo Eduardo        
        self.assertEqual(res[0].partido.codigo, 'hurlingham')        

    def testNormalizador_NormalizarCalleExistentePorPartido02(self):
        res = self.nd.normalizar(u'acevedo, ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 174423)
        self.assertEqual(res[0].nombre, 'Manuel Acevedo')
        self.assertEqual(res[0].partido.nombre, u'Ituzaingó')

        res = self.nd.normalizar(u'acevedo, itu')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 174423)
        self.assertEqual(res[0].nombre, 'Manuel Acevedo')
        self.assertEqual(res[0].partido.nombre, u'Ituzaingó')

    def testNormalizador_NormalizarCalleExistentePorPartido03(self):
        res = self.nd.normalizar(u'acevedo, Beccar')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 49987) #Padre Acevedo        
        self.assertEqual(res[0].partido.codigo, 'san_isidro')

        res = self.nd.normalizar(u'acevedo, padre')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 49987) #Padre Acevedo        
        self.assertEqual(res[0].partido.codigo, 'san_isidro')

    def testNormalizador_NormalizarNombresPermutado(self):
        res = self.nd.normalizar(u'acevedo manuel, ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 174423) #Manuel Acevedo, ituzaingo
        self.assertEqual(res[0].partido.codigo, 'ituzaingo')

    def testNormalizador_NormalizarNombreIncompleto(self):
        res = self.nd.normalizar(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 53658)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarNombreConAcentoYCase(self):
        res = self.nd.normalizar(u'PoToSÍ, José')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 341221) # Potosí
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarNombreConEnie(self):
        res = self.nd.normalizar(u'Roque Saenz Peña, Jose')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.nombre, u'Roque Sáenz Peña')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarCallesConY_01(self):
        res = self.nd.normalizar(u'Gelly y Obes, Jose C Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertTrue(isinstance(res[0], Calle))
        self.assertEqual(res[0].nombre, 'Gelly y Obes')
        self.assertEqual(res[0].codigo, 77481)
            
    def testNormalizador_NormalizarCalleConComa_01(self):
        res = self.nd.normalizar(u'Acevedo, Manuel, Ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 174423) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'ituzaingo')

    def testNormalizador_NormalizarCalleConComa_02(self):
        res = self.nd.normalizar(u'Acevedo, Manuel')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 174423)         
        self.assertEqual(res[0].nombre, 'Manuel Acevedo')        
        self.assertEqual(res[0].partido.codigo, 'ituzaingo')

    def testNormalizador_NormalizarCalleConComa_03(self):
        res = self.nd.normalizar(u'O\'Higgins, San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 15350)         
        self.assertEqual(res[0].nombre, 'O\'Higgins')        
        self.assertEqual(res[0].partido.codigo, 'san_isidro')
        
        self.assertEqual(res[1].codigo, 79669)         
        self.assertEqual(res[1].nombre, 'O\'Higgins')        
        self.assertEqual(res[1].partido.codigo, 'san_miguel')

    def testNormalizador_NormalizarConLimite(self):
        res = self.nd.normalizar(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, u'Debería haber 10 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar(u'San', 25)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 25, u'Debería haber 25 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar(u'San', 200)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 103, u'Debería haber 103 matching/s. Hay {0}'.format(len(res)))
