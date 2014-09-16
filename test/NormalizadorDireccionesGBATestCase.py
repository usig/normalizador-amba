# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','normalizador_direcciones_gba'))

from NormalizadorDireccionesGBA import *
from Partido import Partido
from Calle import Calle
from Errors import *

class NormalizadorDireccionesGBATestCase(unittest.TestCase):
    partidos = ['jose_c_paz','hurlingham','ituzaingo','san_isidro','san_miguel']
#    partidos = ['jose_c_paz','hurlingham','ituzaingo']
    nd = NormalizadorDireccionesGBA(include_list=partidos)

    def testNormalizador_NomalizarCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori')
            
    def testNormalizador_NormalizarCalleExistenteEnTodoPartidos(self):
        res = self.nd.normalizar(u'acevedo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, u'Debería haber 10 matching/s. Hay {0}'.format(len(res)))

        self.assertEqual(res[0].codigo, 30311337) #Acevedo Eduardo
        self.assertEqual(res[0].partido.codigo, 'hurlingham')

        self.assertEqual(res[1].codigo, 191657818) #Manuel Acevedo
        self.assertEqual(res[1].partido.codigo, 'ituzaingo')

        self.assertEqual(res[9].codigo, 56255777) #Manuel Acevedo
        self.assertEqual(res[9].partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarCalleExistentePorPartido01(self):
        res = self.nd.normalizar(u'acevedo, hurlingham')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 30311337) #Acevedo Eduardo        
        self.assertEqual(res[0].partido.codigo, 'hurlingham')        

        res = self.nd.normalizar(u'acevedo, hur')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 30311337) #Acevedo Eduardo        
        self.assertEqual(res[0].partido.codigo, 'hurlingham')        

    def testNormalizador_NormalizarCalleExistentePorPartido02(self):
        res = self.nd.normalizar(u'acevedo, ituzaingo')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 8, u'Debería haber 8 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 191657818) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'ituzaingo')        

        res = self.nd.normalizar(u'acevedo, itu')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 8, u'Debería haber 8 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 191657818) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'ituzaingo')        

    def testNormalizador_NormalizarCalleExistentePorPartido03(self):
        res = self.nd.normalizar(u'acevedo, Jose C Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 56255777) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'jose_c_paz')

        res = self.nd.normalizar(u'acevedo, Jose')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 56255777) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarNombresPermutado(self):
        res = self.nd.normalizar(u'acevedo manuel, c Paz jose')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 56255777) #Manuel Acevedo, José C. Paz
        self.assertEqual(res[0].partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarNombreIncompleto(self):
        res = self.nd.normalizar(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 30417877)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarNombreConAcentoYCase(self):
        res = self.nd.normalizar(u'PoToSÍ, José')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 182271149) # Potosí
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarNombreConEnie(self):
        res = self.nd.normalizar(u'Roque Saenz Peña, Jose')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.nombre, u'Roque Sáenz Peña')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarCallesConY_01(self):
        res = self.nd.normalizar(u'Gelly y Obes, Jose C Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        resCalles = [u'Gelly y Obes']
        resCodigos = [ 46779820,150429162]
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)
            self.assertTrue(calle.codigo in resCodigos)
            
    def testNormalizador_NormalizarCallesConY_02(self):
        res = self.nd.normalizar(u'Juan de Torres de Vera y Aragon')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Juan de Torres de Vera y Aragon')
    
    def testNormalizador_NormalizarCalleConComa_01(self):
        res = self.nd.normalizar(u'Acevedo, Manuel, José C Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].codigo, 56255777) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarCalleConComa_02(self):
        res = self.nd.normalizar(u'Acevedo, Manuel')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 9, u'Debería haber 9 matching/s. Hay {0}'.format(len(res)))

        self.assertEqual(res[0].codigo, 191657818) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'ituzaingo')        

        self.assertEqual(res[8].codigo, 56255777) #Manuel Acevedo        
        self.assertEqual(res[8].partido.codigo, 'jose_c_paz')

    def testNormalizador_NormalizarCalleConComa_03(self):
        res = self.nd.normalizar(u'O\'Higgins, San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 4, u'Debería haber 4 matching/s. Hay {0}'.format(len(res)))

        self.assertEqual(res[0].codigo, 46773324) #Manuel Acevedo        
        self.assertEqual(res[0].partido.codigo, 'san_isidro')        
        self.assertEqual(res[1].codigo, 46773346) #Manuel Acevedo        
        self.assertEqual(res[1].partido.codigo, 'san_isidro')        
        self.assertEqual(res[2].codigo, 46773340) #Manuel Acevedo        
        self.assertEqual(res[2].partido.codigo, 'san_isidro')        

        self.assertEqual(res[3].codigo, 46833916) #Manuel Acevedo        
        self.assertEqual(res[3].partido.codigo, 'san_miguel')

    def testNormalizador_NormalizarConLimite(self):
        res = self.nd.normalizar(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10, u'Debería haber 10 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar(u'San', 25)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 25, u'Debería haber 25 matching/s. Hay {0}'.format(len(res)))

        res = self.nd.normalizar(u'San', 200)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 170, u'Debería haber 170 matching/s. Hay {0}'.format(len(res)))
