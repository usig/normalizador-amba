# coding: UTF-8
import unittest
import sys, os
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from NormalizadorDireccionesAMBA import *
from Partido import Partido
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
                    
    def testNormalizador_NomalizarCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'kokusai dori 1865')

    def testNormalizador_NomalizarDireccionInexistenteEnPartido(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, 'O\'Higgins 1479, Lomas de Zamora')

    def testNormalizador_RestaurantDeLosKao(self):
        res = self.nd.normalizar(u'O\'Higgins 1479, Florida')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].calle.codigo, 4882)
        self.assertEqual(res[0].calle.nombre, 'O\'Higgins')
        self.assertEqual(res[0].calle.localidad, 'Florida')

    def testNormalizador_DireccionEnVariosPartidos(self):
        res = self.nd.normalizar('pavon 4450')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))
        self.assertEqual(res[0].calle.codigo, 278904)
        self.assertEqual(res[0].calle.nombre, u'Pavón')
        self.assertEqual(res[0].calle.localidad, u'José C. Paz')
        self.assertEqual(res[0].altura, 4450)

        self.assertEqual(res[1].calle.codigo, 214876)
        self.assertEqual(res[1].calle.nombre, u'Diagonal Pavón')
        self.assertEqual(res[1].calle.localidad, u'Florida Oeste')
        self.assertEqual(res[1].altura, 4450)

