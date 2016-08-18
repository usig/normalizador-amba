# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.settings import CALLE_Y_CALLE, CALLE_ALTURA
from usig_normalizador_amba.Errors import ErrorTextoSinDireccion

from test_commons import cargarCallejeroEstatico


class BuscadorDireccionesAMBATestCase(unittest.TestCase):
    nd = NormalizadorDireccionesAMBA()
    for n in nd.normalizadores:
        if n.c.partido.nombre != u'CABA':
            cargarCallejeroEstatico(n.c)

    def _checkDireccionCalleAltura(self, direccion, codigo_calle, nombre_calle, altura_calle, codigo_partido, localidad):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.tipo, CALLE_ALTURA)
        self.assertEqual(direccion.calle.codigo, codigo_calle)
        self.assertEqual(direccion.calle.nombre, nombre_calle)
        self.assertEqual(direccion.altura, altura_calle)
        self.assertEqual(direccion.partido.codigo, codigo_partido)
        self.assertEqual(direccion.localidad, localidad)

    def _checkDireccionCalleYCalle(self, direccion, codigo_calle, nombre_calle, codigo_cruce, nombre_cruce, codigo_partido, localidad):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.tipo, CALLE_Y_CALLE)
        self.assertEqual(direccion.calle.codigo, codigo_calle)
        self.assertEqual(direccion.calle.nombre, nombre_calle)
        self.assertEqual(direccion.cruce.codigo, codigo_cruce)
        self.assertEqual(direccion.cruce.nombre, nombre_cruce)
        self.assertEqual(direccion.partido.codigo, codigo_partido)
        self.assertEqual(direccion.localidad, localidad)

    def test_Error_en_texto_vacio(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, '')

    def test_Error_en_texto_sin_y_e_o_numeros(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Este texto no tiene dirección.')

    def test_Error_en_texto_con_palabra_con_y(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Este texto no tiene dirección, pero tiene yeeee.')

################
# Calle altura #
################
    def test_CalleAltura_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion(u'Loria 341, Lomas de Zamora')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], u'Loria 341')
        self._checkDireccionCalleAltura(res[0][0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', u'Lomas de Zamora')

    def test_CalleAltura_muchas_direcciones_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion(u'martin garcia 350, caba | independencia 635  Tigre | irigoyen 272 (Temperley)')
        self.assertEqual(len(res), 3)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], u'martin garcia 350')
        self._checkDireccionCalleAltura(res[0][0]['direcciones'][0], 7032, u'GARCIA, MARTIN AV.', 350, 'caba', u'CABA')

        self.assertEqual(res[1][0]['posicion'], 51)
        self.assertEqual(res[1][0]['texto'], u'| irigoyen 272')
        self._checkDireccionCalleAltura(res[1][0]['direcciones'][0], 35506, u'Bernardo de irigoyen', 272, 'lomas_de_zamora', u'Temperley')

        self.assertEqual(res[2][0]['posicion'], 24)
        self.assertEqual(res[2][0]['texto'], u'| independencia 635')
        self._checkDireccionCalleAltura(res[2][0]['direcciones'][0], 1540, u'Independencia', 635, 'tigre', u'Troncos del Talar')
        self._checkDireccionCalleAltura(res[2][0]['direcciones'][1], 193400, u'Independencia', 635, 'tigre', u'Dique Luján')

    def test_CalleAltura_sin_localidad(self):
        res = self.nd.buscarDireccion(u'Loria 341')
        self.assertEqual(len(res), 5)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], u'Loria 341')
        self._checkDireccionCalleAltura(res[0][0]['direcciones'][0], 12137, u'SANCHEZ DE LORIA', 341, 'caba', u'CABA')
        self._checkDireccionCalleAltura(res[1][0]['direcciones'][0], 139266, u'Loria', 341, 'almirante_brown', u'Glew')
        self._checkDireccionCalleAltura(res[2][0]['direcciones'][0], 109525, u'Loria', 341, 'ezeiza', u'Ezeiza')
        self._checkDireccionCalleAltura(res[3][0]['direcciones'][0], 141693, u'130 - Sanchez de Loria', 341, 'florencio_varela', u'Florencio Varela')
        self._checkDireccionCalleAltura(res[4][0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', u'Lomas de Zamora')

#################
# Calle y calle #
#################
    def test_CalleCalle_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion(u'Loria e Italia, Lomas de Zamora')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], u'Loria e Italia,')
        self._checkDireccionCalleYCalle(res[0][0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18119, u'Italia', 'lomas_de_zamora', u'Lomas de Zamora')

    def test_CalleCalle_muchas_direcciones_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion(u'Martin Garcia y Av. Patricios, caba | Triunvirato y Caseros  Tigre | Irigoyen y Juncal (Temperley)')
        self.assertEqual(len(res), 3)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], u'Martin Garcia y Av. Patricios,')
        self._checkDireccionCalleYCalle(res[0][0]['direcciones'][0], 7032, u'GARCIA, MARTIN AV.', 17034, u'REGIMIENTO DE PATRICIOS AV.', 'caba', u'CABA')

        self.assertEqual(res[1][0]['posicion'], 67)
        self.assertEqual(res[1][0]['texto'], u'| Irigoyen y Juncal')
        self._checkDireccionCalleYCalle(res[1][0]['direcciones'][0], 35506, u'Bernardo de irigoyen', 20254, u'Juncal', 'lomas_de_zamora', u'Temperley')

        self.assertEqual(res[2][0]['posicion'], 36)
        self.assertEqual(res[2][0]['texto'], u'| Triunvirato y Caseros ')
        self._checkDireccionCalleYCalle(res[2][0]['direcciones'][0], 191186, u'Triunvirato', 190846, u'Caseros', 'tigre', u'Troncos del Talar')

    def test_CalleCalle_sin_localidad(self):
        res = self.nd.buscarDireccion(u'Corrientes y Esmeralda')
        self.assertEqual(len(res), 4)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], u'Corrientes y Esmeralda')
        self._checkDireccionCalleYCalle(res[0][0]['direcciones'][0], 3174, u'CORRIENTES AV.', 5072, u'ESMERALDA', 'caba', u'CABA')
        self._checkDireccionCalleYCalle(res[1][0]['direcciones'][0], 211085, u'Corrientes', 210855, u'Esmeralda', 'escobar', u'Maquinista Savio')
        self._checkDireccionCalleYCalle(res[2][0]['direcciones'][0], 171900, u'Corrientes', 171851, u'La Esmeralda', 'merlo', u'San Antonio de Padua')
        self._checkDireccionCalleYCalle(res[3][0]['direcciones'][0], 93176, u'Corrientes', 122722, u'Esmeralda (393)', 'quilmes', u'Quilmes')
