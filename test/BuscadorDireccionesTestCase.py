# coding: UTF-8
import unittest
import sys, os

sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from test_commons import cargarCallejeroEstatico

from NormalizadorDirecciones import *
from Partido import Partido
from Errors import *

class BuscadorDireccionesTestCase(unittest.TestCase):
    p = Partido('lomas_de_zamora', u'Lomas de Zamora', u'Partido de Lomas de Zamora', 2400639)
    nd = NormalizadorDirecciones(p)
    cargarCallejeroEstatico(nd.c)
    
    def test_Buscar_en_texto_vacio(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, '')

    def test_Buscar_en_texto_sin_y_e_o_numeros(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Este texto no tiene dirección.')

    def test_Buscar_en_texto_con_palabra_con_y(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Este texto no tiene dirección, pero tiene yeeee.')
