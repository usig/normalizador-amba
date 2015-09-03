# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from NormalizadorDireccionesAMBA import *
from Partido import Partido
from Direccion import Direccion
from Calle import Calle
from Errors import *

class NormalizadorDireccionesAMBACalleAlturaTestCase(unittest.TestCase):
    partidos = ['almirante_brown','jose_c_paz','lomas_de_zamora','quilmes','san_isidro','vicente_lopez']
    nd = NormalizadorDireccionesAMBA(include_list=partidos)
    for n in nd.normalizadores:
        with open('callejeros/{0}.callejero'.format(n.partido.codigo)) as data_file:
            data = json.load(data_file)
        n.c.data = data
        n.c.data.sort()
        n.c.osm_ids = [k[0] for k in n.c.data]
    
    
    def _checkDireccion(self, direccion, codigo, nombre, altura, codigo_partido, localidad):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.calle.codigo, codigo)
        self.assertEqual(direccion.calle.nombre, nombre)
        self.assertEqual(direccion.altura, altura)
        self.assertEqual(direccion.partido.codigo, codigo_partido)
        self.assertEqual(direccion.localidad, localidad)
        
    def testNormalizador_NomalizarCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori 1865')

    def testNormalizador_NomalizarDireccionInexistenteEnPartido(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'O\'Higgins 1479, Lomas de Zamora')

    def testNormalizador_RestaurantDeLosKao(self):
        res = self.nd.normalizar(u'O\'Higgins 1479, Florida')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0],4882,u'O\'Higgins',1479,'vicente_lopez',u'Florida')

    def testNormalizador_DireccionEnVariosPartidos(self):
        res = self.nd.normalizar(u'pavón 4450')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self._checkDireccion(res[0],278904,u'Pavón',4450,'jose_c_paz',u'José C. Paz')
        self._checkDireccion(res[1],214876,u'Diagonal Pavón',4450,'vicente_lopez',u'Florida Oeste')
