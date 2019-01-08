# coding: UTF-8

import unittest

from usig_normalizador_amba.NormalizadorDirecciones import NormalizadorDirecciones
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.Errors import ErrorTextoSinDireccion
from usig_normalizador_amba.settings import CALLE_Y_CALLE, CALLE_ALTURA

from tests.test_commons import cargarCallejeroEstatico


class BuscadorDireccionesTestCase(unittest.TestCase):
    p = Partido('lomas_de_zamora', 'Lomas de Zamora', 'Partido de Lomas de Zamora', 2400639)
    nd = NormalizadorDirecciones(p)
    cargarCallejeroEstatico(nd.c)

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

    def test_Error_en_texto_que_no_es_direccion(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Kokusai Doori 1262')

    def test_Error_direccion_con_altura_invalida(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Arenales 2563')

    def test_CalleAltura_al_comienzo_del_texto(self):
        res = self.nd.buscarDireccion('Loria 341, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria 341')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_al_final_del_texto(self):
        res = self.nd.buscarDireccion('Cerca de la estación de lomas. Laprida 11')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 31)
        self.assertEqual(res[0]['texto'], 'Laprida 11')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18028, 'Laprida', 11, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_al_comienzo_y_al_final_del_texto(self):
        res = self.nd.buscarDireccion('Belgrano 840')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Belgrano 840')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34017, 'Belgrano', 840, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltuta_conector_al(self):
        # Sin conector:
        res = self.nd.buscarDireccion('Ubicado en Boedo 150, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Boedo 150')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 323730, 'Mariano Boedo', 150, 'lomas_de_zamora', 'Lomas de Zamora')

        # Con conector:
        res = self.nd.buscarDireccion('Ubicado en Boedo al 150, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Boedo al 150')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 323730, 'Mariano Boedo', 150, 'lomas_de_zamora', 'Lomas de Zamora')

        # Palabra que termina con el conector (al)
        res = self.nd.buscarDireccion('Ubicado en Arenal 53, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Arenal 53')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 360326, 'General Arenales', 53, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_calle_con_y(self):
        res = self.nd.buscarDireccion('Ubicado en Carlos Guido y Spano 701, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Carlos Guido y Spano 701')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 20400, 'Carlos Guido y Spano', 701, 'lomas_de_zamora', 'Temperley')

    def test_CalleAltura_calle_con_1_o_mas_palabras(self):
        # 1 palabra
        res = self.nd.buscarDireccion('Ubicado en Pedernera 86, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Pedernera 86')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34037, 'Pedernera', 86, 'lomas_de_zamora', 'Lomas de Zamora')

        # 2 palabras
        res = self.nd.buscarDireccion('Ubicado en Julio Fonrouge 356, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Julio Fonrouge 356')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 160708, 'Julio Fonrouge', 356, 'lomas_de_zamora', 'Lomas de Zamora')

        # 3 palabras
        res = self.nd.buscarDireccion('Ubicado en Monseñor Alejandro Schell 166, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Monseñor Alejandro Schell 166')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34039, 'Monseñor Alejandro Schell', 166, 'lomas_de_zamora', 'Lomas de Zamora')

        # 4 palabras
        res = self.nd.buscarDireccion('Ubicado en Capitán de Fragata Moyano 701, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Capitán de Fragata Moyano 701')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 30647, 'Capitán de Fragata Moyano', 701, 'lomas_de_zamora', 'Llavallol')

        # un exceso...
        res = self.nd.buscarDireccion('Ubicado en Av. General Carlos María de Alvear 426, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Av. General Carlos María de Alvear 426')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18772, 'Av. General Carlos María de Alvear', 426, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_calle_string_y_unicode(self):
        # string
        res = self.nd.buscarDireccion('Ubicado en sarandi 359.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'sarandi 359')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34004, 'Sarandi', 359, 'lomas_de_zamora', 'Lomas de Zamora')

        # unicode
        res = self.nd.buscarDireccion('Ubicado en sarandí 359.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'sarandí 359')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34004, 'Sarandi', 359, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_2_direcciones(self):
        res = self.nd.buscarDireccion('Ubicado en balcarce 325 y balcarce 327')
        self.assertEqual(len(res), 2)

        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'balcarce 325')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34011, 'Balcarce', 325, 'lomas_de_zamora', 'Lomas de Zamora')

        self.assertEqual(res[1]['posicion'], 26)
        self.assertEqual(res[1]['texto'], 'balcarce 327')
        self._checkDireccionCalleAltura(res[1]['direcciones'][0], 34011, 'Balcarce', 327, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_direccion_ambigua(self):
        res = self.nd.buscarDireccion('Ubicado en la calle martín 731')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 20)
        self.assertEqual(res[0]['texto'], 'martín 731')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18763, 'General José de San Martín', 731, 'lomas_de_zamora', 'Lomas de Zamora')
        self._checkDireccionCalleAltura(res[0]['direcciones'][1], 19098, 'Martín Capello', 731, 'lomas_de_zamora', 'Banfield')
        self._checkDireccionCalleAltura(res[0]['direcciones'][2], 19144, 'Av. General Martín Rodríguez', 731, 'lomas_de_zamora', 'Villa Centenario')

    def test_CalleAltura_direccion_con_calle_con_numero(self):
        res = self.nd.buscarDireccion('12 de octubre 535')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], '12 de octubre 535')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18579, '12 de Octubre', 535, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_ejemplos_que_motivaron_esta_funcion_y_otros(self):
        # Direccion con piso y depto
        res = self.nd.buscarDireccion('Loria 341 piso 5 dpto C.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria 341')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con varias alturas
        res = self.nd.buscarDireccion('Dirección: Portela 576/578/580')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Portela 576')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18287, 'Francisco Portela', 576, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con codigo postal
        res = self.nd.buscarDireccion('boedo 367, cp 1832')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'boedo 367')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 323730, 'Mariano Boedo', 367, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion formato calle al altura
        res = self.nd.buscarDireccion('Palacios al 1200')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Palacios al 1200')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 628, 'General Palacios', 1200, 'lomas_de_zamora', 'Banfield')

        # Direccion con calles laterales
        res = self.nd.buscarDireccion('España 37 - Entre Gorriti y Laprida')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'España 37')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18117, 'España', 37, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con calles laterales
        res = self.nd.buscarDireccion('Av. H. Yrigoyen 9399 esq. Oliden')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Av. H. Yrigoyen 9399')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 252522, 'Avenida Hipólito Yrigoyen', 9399, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con zonas de referencia
        res = self.nd.buscarDireccion('Vicente Oliden 2385 -Parque Barón - Lomas de Zamora')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Vicente Oliden 2385')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18214, 'Vicente Oliden', 2385, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleYCalle_ojo_con_este_caso_calle_con_numeros_al_comienzo(self):
        res = self.nd.buscarDireccion('30 de Septiembre 3750, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], '30 de Septiembre 3750')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 123232, '30 de Septiembre', 3750, 'lomas_de_zamora', 'Temperley')

    def test_CalleYCalle_ojo_con_este_caso_calle_con_numeros_en_medio(self):
        res = self.nd.buscarDireccion('Ubicado en 30 de Septiembre 3750, a metros de la estación.')
        self.assertEqual(len(res), 2)

        self.assertEqual(res[0]['posicion'], 8)
        self.assertEqual(res[0]['texto'], 'en 30')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18586, 'Entre Ríos', 30, 'lomas_de_zamora', 'Lomas de Zamora')
        self._checkDireccionCalleAltura(res[0]['direcciones'][1], 18600, 'Enrique Sántos Discépolo', 30, 'lomas_de_zamora', 'Lomas de Zamora')
        self._checkDireccionCalleAltura(res[0]['direcciones'][2], 45454, 'Blanco Encalada', 30, 'lomas_de_zamora', 'Temperley')

        self.assertEqual(res[1]['posicion'], 11)
        self.assertEqual(res[1]['texto'], '30 de Septiembre 3750')
        self._checkDireccionCalleAltura(res[1]['direcciones'][0], 123232, '30 de Septiembre', 3750, 'lomas_de_zamora', 'Temperley')

#################
# Calle y calle #
#################

    def test_error_en_texto_que_no_es_esquina(self):
        # no calle y no calle
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Kokusai Doori y aoi michi')
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, '国際通り y 青道')
        # calle y no calle
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Laprida y aoi michi')
        # no calle y calle
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Kokusai Doori y Boedo')

    def test_error_en_calles_que_no_se_cruzan(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Fonrouge y Lamadrid')

    def test_CalleYCalle_direccion_en_distintas_parte_del_texto(self):
        # Comienzo
        res = self.nd.buscarDireccion('Loria y Sarmiento, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria y Sarmiento,')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18120, 'Domingo Faustino Sarmiento', 'lomas_de_zamora', 'Lomas de Zamora')
        # Medio
        res = self.nd.buscarDireccion('Ubicado en Loria y Sarmiento, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Loria y Sarmiento,')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18120, 'Domingo Faustino Sarmiento', 'lomas_de_zamora', 'Lomas de Zamora')
        # Final
        res = self.nd.buscarDireccion('Ubicado en Loria y Sarmiento.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'Loria y Sarmiento.')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18120, 'Domingo Faustino Sarmiento', 'lomas_de_zamora', 'Lomas de Zamora')
        # Comienzo y final
        res = self.nd.buscarDireccion('Loria y Sarmiento')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria y Sarmiento')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18120, 'Domingo Faustino Sarmiento', 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleYCalle_direcciones_con_y_y_con_e(self):
        # Con y
        res = self.nd.buscarDireccion('Loria y España')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria y España')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18117, 'España', 'lomas_de_zamora', 'Lomas de Zamora')
        # Con e
        res = self.nd.buscarDireccion('Loria e Italia')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria e Italia')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18119, 'Italia', 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleYCalle_direccion_con_calles_de_una_palabra(self):
        res = self.nd.buscarDireccion('Arenales y Fonrouge')
        self.assertEqual(len(res), 1, 'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Arenales y Fonrouge')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 360326, 'General Arenales', 160708, 'Julio Fonrouge', 'lomas_de_zamora', 'Lomas de Zamora')

        res = self.nd.buscarDireccion('Loria e italia')
        self.assertEqual(len(res), 1, 'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria e italia')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18119, 'Italia', 'lomas_de_zamora', 'Lomas de Zamora')

        res = self.nd.buscarDireccion('malabia y palacios')
        self.assertEqual(len(res), 1, 'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'malabia y palacios')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 553, 'Malabia', 628, 'General Palacios', 'lomas_de_zamora', 'Banfield')

        res = self.nd.buscarDireccion('brown y peron')
        self.assertEqual(len(res), 1, 'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'brown y peron')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 25606, 'Almirante Brown', 196982, 'Av. Eva Perón', 'lomas_de_zamora', 'Temperley')

    def test_CalleYCalle_direccion_con_calles_de_mas_de_una_palabra(self):
        res = self.nd.buscarDireccion('General Arenales y Julio Fonrouge')
        self.assertEqual(len(res), 1, 'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'General Arenales y Julio Fonrouge')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 360326, 'General Arenales', 160708, 'Julio Fonrouge', 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleYCalle_el_orden_de_los_factores_altera_el_producto(self):
        res = self.nd.buscarDireccion('Arenales y Fonrouge')
        self.assertEqual(len(res), 1, 'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 360326, 'General Arenales', 160708, 'Julio Fonrouge', 'lomas_de_zamora', 'Lomas de Zamora')

        res = self.nd.buscarDireccion('Fonrouge y Arenales')
        self.assertEqual(len(res), 1, 'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 160708, 'Julio Fonrouge', 360326, 'General Arenales', 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleYCalle_ojo_con_este_caso_palabra_colada(self):
        res = self.nd.buscarDireccion('Loria y Meeks, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], 'Loria y Meeks, a')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, 'Mariano Sánchez de Loria', 18112, 'Av. Meeks', 'lomas_de_zamora', 'Lomas de Zamora')
