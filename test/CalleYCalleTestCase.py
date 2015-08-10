# coding: UTF-8
import unittest
import sys, os
import simplejson as json
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from NormalizadorDirecciones import *
from Partido import Partido
from Errors import *
from settings import *

class CalleYCalleTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    nd = NormalizadorDirecciones(p)

    # Cargo los callejeros congelados
    with open('callejeros/jose_c_paz.callejero') as data_file:
        data = json.load(data_file)
    nd.c.data = data
    nd.c.data.sort()
    nd.c.osm_ids = [k[0] for k in nd.c.data]

    
    def testCalleInexistente01(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'Elm street y Roque Sáenz Peña')

    def testCalleInexistente02(self):
        self.assertRaises(ErrorCruceInexistente, self.nd.normalizar, u'Roque Sáenz Peña y kokusai dori')

    def testCalle1UnicaCalle2UnicaCruceInexistente(self):
        try:
            self.nd.normalizar('Mateo Bootz y pavon')
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCruceInexistente))

    def testCalle1MuchasCalle2MuchasCruceInexistente(self):
        try:
            self.nd.normalizar(u'saenz peña y gaspar campos')
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCruceInexistente))

    def testCalle1UnicaCalle2UnicaCruceExistente(self):
        res = self.nd.normalizar(u'Suecia y libano')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 182539)
        self.assertEqual(d.calle.nombre, u'Suecia')
        self.assertEqual(d.cruce.codigo, 231716)
        self.assertEqual(d.cruce.nombre, u'Líbano')

    def testCalle1UnicaCalle2MuchasCruceExistenteUnico(self):
        res = self.nd.normalizar(u'líbano y Avenida')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 231716)
        self.assertEqual(d.calle.nombre, u'Líbano')
        self.assertEqual(d.cruce.codigo, 78155)
        self.assertEqual(d.cruce.nombre, 'Avenida Croacia')

    def testCalle1MuchasCalle2UnicaCruceExistenteUnico(self):
        res = self.nd.normalizar(u'Avenida y líbano')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 78155)
        self.assertEqual(d.calle.nombre, u'Avenida Croacia')
        self.assertEqual(d.cruce.codigo, 231716)
        self.assertEqual(d.cruce.nombre, u'Líbano')

    def testCalleConY01(self):
        res = self.nd.normalizar(u'Arias y Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 77242)
        self.assertEqual(d.calle.nombre, 'Coronel Arias')
        self.assertEqual(d.cruce.codigo, 77481)
        self.assertEqual(d.cruce.nombre, u'Gelly y Obes')

    def testCalleConY02(self):
        res = self.nd.normalizar(u'Gelly y Obes y Arias')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 77481)
        self.assertEqual(d.calle.nombre, u'Gelly y Obes')
        self.assertEqual(d.cruce.codigo, 77242)
        self.assertEqual(d.cruce.nombre, 'Coronel Arias')

    def testCalleConY03(self):
        res = self.nd.normalizar(u'Gel y Ob y Coronel Arias')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 77481)
        self.assertEqual(d.calle.nombre, u'Gelly y Obes')
        self.assertEqual(d.cruce.codigo, 77242)
        self.assertEqual(d.cruce.nombre, 'Coronel Arias')

    def testCalleConYParcial01(self):
        res = self.nd.normalizar(u'Arias y Gel y Ob')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 77242)
        self.assertEqual(d.calle.nombre, 'Coronel Arias')
        self.assertEqual(d.cruce.codigo, 77481)
        self.assertEqual(d.cruce.nombre, u'Gelly y Obes')

    def testDireccionSeparadaPorE01(self):
        res = self.nd.normalizar(u'pinero e iglesia')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 53491)
        self.assertEqual(d.calle.nombre, u'Piñero')
        self.assertEqual(d.cruce.codigo, 53648)
        self.assertEqual(d.cruce.nombre, u'Iglesias')

    def testCalle1MuchasCalle2MuchasCruceExistenteMulti(self):
        res = self.nd.normalizar(u'santiago y are')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, 'Deberia haber 2 matchings')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 53658) #Santiago de Compostela
        self.assertEqual(d.cruce.codigo, 53565) #Gral Arenales
        d = res[1]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 77662) #Santiago L. Copello
        self.assertEqual(d.cruce.codigo, 53565) #Arturo Illia
        
    def testCalleConE02(self):
        res = self.nd.normalizar(u'José E. Rodó y Paula Albarracín')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Deberia haber 1 matchings')
        d = res[0]
        self.assertTrue(isinstance(d, Direccion))
        self.assertEqual(d.tipo, CALLE_Y_CALLE )
        self.assertEqual(d.calle.codigo, 78817) #José E. Rodó
        self.assertEqual(d.cruce.codigo, 52665) #Paula Albarracín

    def testDireccionSeparadaPorECalleNoEmpiezaConI(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'miranda e arregui')

        