# coding: UTF-8

import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.settings import CALLE_Y_CALLE, CALLE_ALTURA
from usig_normalizador_amba.Errors import ErrorTextoSinDireccion

from tests.test_commons import cargarCallejeroEstatico


class BuscadorDireccionesAMBATestCase(unittest.TestCase):
    nd = NormalizadorDireccionesAMBA()
    for n in nd.normalizadores:
        if n.c.partido.nombre != 'CABA':
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
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Este texto no tiene dirección.')

    def test_Error_en_texto_con_palabra_con_y(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Este texto no tiene dirección, pero tiene yeeee.')

################
# Calle altura #
################
    def test_CalleAltura_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion('Loria 341, Lomas de Zamora')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], 'Loria 341')
        self._checkDireccionCalleAltura(res[0][0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_muchas_direcciones_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion('martin garcia 350, caba | independencia 635  Tigre | irigoyen 272 (Temperley)')
        self.assertEqual(len(res), 3)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], 'martin garcia 350')
        self._checkDireccionCalleAltura(res[0][0]['direcciones'][0], 7032, 'GARCIA, MARTIN AV.', 350, 'caba', 'CABA')

        self.assertEqual(res[1][0]['posicion'], 51)
        self.assertEqual(res[1][0]['texto'], '| irigoyen 272')
        self._checkDireccionCalleAltura(res[1][0]['direcciones'][0], 35506, 'Bernardo de irigoyen', 272, 'lomas_de_zamora', 'Temperley')

        self.assertEqual(res[2][0]['posicion'], 24)
        self.assertEqual(res[2][0]['texto'], '| independencia 635')
        self._checkDireccionCalleAltura(res[2][0]['direcciones'][0], 1540, 'Independencia', 635, 'tigre', 'Troncos del Talar')
        self._checkDireccionCalleAltura(res[2][0]['direcciones'][1], 193400, 'Independencia', 635, 'tigre', 'Dique Luján')

    def test_CalleAltura_sin_localidad(self):
        res = self.nd.buscarDireccion('Loria 341')
        self.assertEqual(len(res), 5)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], 'Loria 341')
        self._checkDireccionCalleAltura(res[0][0]['direcciones'][0], 12137, 'SANCHEZ DE LORIA', 341, 'caba', 'CABA')
        self._checkDireccionCalleAltura(res[1][0]['direcciones'][0], 139266, 'Loria', 341, 'almirante_brown', 'Glew')
        self._checkDireccionCalleAltura(res[2][0]['direcciones'][0], 109525, 'Loria', 341, 'ezeiza', 'Ezeiza')
        self._checkDireccionCalleAltura(res[3][0]['direcciones'][0], 141693, '130 - Sanchez de Loria', 341, 'florencio_varela', 'Florencio Varela')
        self._checkDireccionCalleAltura(res[4][0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', 'Lomas de Zamora')

#################
# Calle y calle #
#################
    def test_CalleCalle_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion('Loria e Italia, Lomas de Zamora')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], 'Loria e Italia,')
        self._checkDireccionCalleYCalle(res[0][0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18119, 'Italia', 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleCalle_muchas_direcciones_con_localidad_o_partido(self):
        res = self.nd.buscarDireccion('Martin Garcia y Av. Patricios, caba | Triunvirato y Caseros  Tigre | Irigoyen y Juncal (Temperley)')
        self.assertEqual(len(res), 3)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], 'Martin Garcia y Av. Patricios,')
        self._checkDireccionCalleYCalle(res[0][0]['direcciones'][0], 7032, 'GARCIA, MARTIN AV.', 17034, 'REGIMIENTO DE PATRICIOS AV.', 'caba', 'CABA')

        self.assertEqual(res[1][0]['posicion'], 67)
        self.assertEqual(res[1][0]['texto'], '| Irigoyen y Juncal')
        self._checkDireccionCalleYCalle(res[1][0]['direcciones'][0], 35506, 'Bernardo de irigoyen', 20254, 'Juncal', 'lomas_de_zamora', 'Temperley')

        self.assertEqual(res[2][0]['posicion'], 36)
        self.assertEqual(res[2][0]['texto'], '| Triunvirato y Caseros ')
        self._checkDireccionCalleYCalle(res[2][0]['direcciones'][0], 191186, 'Triunvirato', 190846, 'Caseros', 'tigre', 'Troncos del Talar')

    def test_CalleCalle_sin_localidad(self):
        res = self.nd.buscarDireccion('Corrientes y Esmeralda')
        self.assertEqual(len(res), 4)

        self.assertEqual(res[0][0]['posicion'], 0)
        self.assertEqual(res[0][0]['texto'], 'Corrientes y Esmeralda')
        self._checkDireccionCalleYCalle(res[0][0]['direcciones'][0], 3174, 'CORRIENTES AV.', 5072, 'ESMERALDA', 'caba', 'CABA')
        self._checkDireccionCalleYCalle(res[1][0]['direcciones'][0], 211085, 'Corrientes', 210855, 'Esmeralda', 'escobar', 'Maquinista Savio')
        self._checkDireccionCalleYCalle(res[2][0]['direcciones'][0], 171900, 'Corrientes', 171851, 'La Esmeralda', 'merlo', 'San Antonio de Padua')
        self._checkDireccionCalleYCalle(res[3][0]['direcciones'][0], 93176, 'Corrientes', 122722, 'Esmeralda (393)', 'quilmes', 'Quilmes')
