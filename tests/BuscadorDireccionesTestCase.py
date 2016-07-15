# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDirecciones import NormalizadorDirecciones
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.Errors import ErrorTextoSinDireccion
from usig_normalizador_amba.settings import CALLE_Y_CALLE, CALLE_ALTURA

from test_commons import cargarCallejeroEstatico


class BuscadorDireccionesTestCase(unittest.TestCase):
    p = Partido('lomas_de_zamora', u'Lomas de Zamora', u'Partido de Lomas de Zamora', 2400639)
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
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Este texto no tiene dirección.')

    def test_Error_en_texto_con_palabra_con_y(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Este texto no tiene dirección, pero tiene yeeee.')

################
# Calle altura #
################

    def test_Error_en_texto_que_no_es_direccion(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Kokusai Doori 1262')

    def test_Error_direccion_con_altura_invalida(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, 'Arenales 2563')

    def test_CalleAltura_al_comienzo_del_texto(self):
        res = self.nd.buscarDireccion(u'Loria 341, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria 341')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_al_final_del_texto(self):
        res = self.nd.buscarDireccion(u'Cerca de la estación de lomas. Laprida 11')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 31)
        self.assertEqual(res[0]['texto'], u'Laprida 11')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18028, u'Laprida', 11, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_al_comienzo_y_al_final_del_texto(self):
        res = self.nd.buscarDireccion(u'Belgrano 840')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Belgrano 840')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34017, u'Belgrano', 840, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltuta_conector_al(self):
        # Sin conector:
        res = self.nd.buscarDireccion(u'Ubicado en Boedo 150, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Boedo 150')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 323730, u'Mariano Boedo', 150, 'lomas_de_zamora', 'Lomas de Zamora')

        # Con conector:
        res = self.nd.buscarDireccion(u'Ubicado en Boedo al 150, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Boedo al 150')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 323730, u'Mariano Boedo', 150, 'lomas_de_zamora', 'Lomas de Zamora')

        # Palabra que termina con el conector (al)
        res = self.nd.buscarDireccion(u'Ubicado en Arenal 53, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Arenal 53')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 360326, u'General Arenales', 53, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_calle_con_y(self):
        res = self.nd.buscarDireccion(u'Ubicado en Carlos Guido y Spano 701, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Carlos Guido y Spano 701')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 20400, u'Carlos Guido y Spano', 701, 'lomas_de_zamora', 'Temperley')

    def test_CalleAltura_calle_con_1_o_mas_palabras(self):
        # 1 palabra
        res = self.nd.buscarDireccion(u'Ubicado en Pedernera 86, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Pedernera 86')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34037, u'Pedernera', 86, 'lomas_de_zamora', 'Lomas de Zamora')

        # 2 palabras
        res = self.nd.buscarDireccion(u'Ubicado en Julio Fonrouge 356, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Julio Fonrouge 356')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 160708, u'Julio Fonrouge', 356, 'lomas_de_zamora', 'Lomas de Zamora')

        # 3 palabras
        res = self.nd.buscarDireccion(u'Ubicado en Monseñor Alejandro Schell 166, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Monseñor Alejandro Schell 166')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34039, u'Monseñor Alejandro Schell', 166, 'lomas_de_zamora', 'Lomas de Zamora')

        # 4 palabras
        res = self.nd.buscarDireccion(u'Ubicado en Capitán de Fragata Moyano 701, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Capitán de Fragata Moyano 701')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 30647, u'Capitán de Fragata Moyano', 701, 'lomas_de_zamora', 'Llavallol')

        # un exceso...
        res = self.nd.buscarDireccion(u'Ubicado en Av. General Carlos María de Alvear 426, a metros de la estación de Lomas de Zamora.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Av. General Carlos María de Alvear 426')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18772, u'Av. General Carlos María de Alvear', 426, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_calle_string_y_unicode(self):
        # string
        res = self.nd.buscarDireccion('Ubicado en sarandi 359.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], 'sarandi 359')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34004, u'Sarandi', 359, 'lomas_de_zamora', 'Lomas de Zamora')

        # unicode
        res = self.nd.buscarDireccion(u'Ubicado en sarandí 359.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'sarandí 359')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34004, u'Sarandi', 359, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_2_direcciones(self):
        res = self.nd.buscarDireccion(u'Ubicado en balcarce 325 y balcarce 327')
        self.assertEqual(len(res), 2)

        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'balcarce 325')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 34011, u'Balcarce', 325, 'lomas_de_zamora', 'Lomas de Zamora')

        self.assertEqual(res[1]['posicion'], 26)
        self.assertEqual(res[1]['texto'], u'balcarce 327')
        self._checkDireccionCalleAltura(res[1]['direcciones'][0], 34011, u'Balcarce', 327, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_direccion_ambigua(self):
        res = self.nd.buscarDireccion(u'Ubicado en la calle martín 731')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 20)
        self.assertEqual(res[0]['texto'], u'martín 731')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18763, u'General José de San Martín', 731, 'lomas_de_zamora', 'Lomas de Zamora')
        self._checkDireccionCalleAltura(res[0]['direcciones'][1], 19098, u'Martín Capello', 731, 'lomas_de_zamora', 'Banfield')
        self._checkDireccionCalleAltura(res[0]['direcciones'][2], 19144, u'Av. General Martín Rodríguez', 731, 'lomas_de_zamora', 'Villa Centenario')

    def test_CalleAltura_direccion_con_calle_con_numero(self):
        res = self.nd.buscarDireccion(u'12 de octubre 535')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'12 de octubre 535')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18579, u'12 de Octubre', 535, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleAltura_ejemplos_que_motivaron_esta_funcion_y_otros(self):
        # Direccion con piso y depto
        res = self.nd.buscarDireccion(u'Loria 341 piso 5 dpto C.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria 341')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 341, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con varias alturas
        res = self.nd.buscarDireccion(u'Dirección: Portela 576/578/580')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Portela 576')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18287, u'Francisco Portela', 576, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con codigo postal
        res = self.nd.buscarDireccion(u'boedo 367, cp 1832')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'boedo 367')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 323730, u'Mariano Boedo', 367, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion formato calle al altura
        res = self.nd.buscarDireccion(u'Palacios al 1200')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Palacios al 1200')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 628, u'General Palacios', 1200, 'lomas_de_zamora', 'Banfield')

        # Direccion con calles laterales
        res = self.nd.buscarDireccion(u'España 37 - Entre Gorriti y Laprida')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'España 37')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18117, u'España', 37, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con calles laterales
        res = self.nd.buscarDireccion(u'Av. H. Yrigoyen 9399 esq. Oliden')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Av. H. Yrigoyen 9399')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 252522, u'Avenida Hipólito Yrigoyen', 9399, 'lomas_de_zamora', 'Lomas de Zamora')

        # Direccion con zonas de referencia
        res = self.nd.buscarDireccion(u'Vicente Oliden 2385 -Parque Barón - Lomas de Zamora')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Vicente Oliden 2385')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18214, u'Vicente Oliden', 2385, 'lomas_de_zamora', 'Lomas de Zamora')

    def test_CalleYCalle_ojo_con_este_caso_calle_con_numeros_al_comienzo(self):
        res = self.nd.buscarDireccion(u'30 de Septiembre 3750, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'30 de Septiembre 3750')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 123232, u'30 de Septiembre', 3750, 'lomas_de_zamora', 'Temperley')

    def test_CalleYCalle_ojo_con_este_caso_calle_con_numeros_en_medio(self):
        res = self.nd.buscarDireccion(u'Ubicado en 30 de Septiembre 3750, a metros de la estación.')
        self.assertEqual(len(res), 2)

        self.assertEqual(res[0]['posicion'], 8)
        self.assertEqual(res[0]['texto'], u'en 30')
        self._checkDireccionCalleAltura(res[0]['direcciones'][0], 18586, u'Entre Ríos', 30, 'lomas_de_zamora', 'Lomas de Zamora')
        self._checkDireccionCalleAltura(res[0]['direcciones'][1], 18600, u'Enrique Sántos Discépolo', 30, 'lomas_de_zamora', 'Lomas de Zamora')
        self._checkDireccionCalleAltura(res[0]['direcciones'][2], 45454, u'Blanco Encalada', 30, 'lomas_de_zamora', 'Temperley')

        self.assertEqual(res[1]['posicion'], 11)
        self.assertEqual(res[1]['texto'], u'30 de Septiembre 3750')
        self._checkDireccionCalleAltura(res[1]['direcciones'][0], 123232, u'30 de Septiembre', 3750, 'lomas_de_zamora', 'Temperley')

#################
# Calle y calle #
#################

    def test_error_en_texto_que_no_es_esquina(self):
        # no calle y no calle
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Kokusai Doori y aoi michi')
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'国際通り y 青道')
        # calle y no calle
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Laprida y aoi michi')
        # no calle y calle
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Kokusai Doori y Boedo')

    def test_error_en_calles_que_no_se_cruzan(self):
        self.assertRaises(ErrorTextoSinDireccion, self.nd.buscarDireccion, u'Fonrouge y Lamadrid')

    def test_CalleYCalle_direccion_en_distintas_parte_del_texto(self):
        # Comienzo
        res = self.nd.buscarDireccion(u'Loria y Sarmiento, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria y Sarmiento,')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18120, u'Domingo Faustino Sarmiento', 'lomas_de_zamora', u'Lomas de Zamora')
        # Medio
        res = self.nd.buscarDireccion(u'Ubicado en Loria y Sarmiento, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Loria y Sarmiento,')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18120, u'Domingo Faustino Sarmiento', 'lomas_de_zamora', u'Lomas de Zamora')
        # Final
        res = self.nd.buscarDireccion(u'Ubicado en Loria y Sarmiento.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 11)
        self.assertEqual(res[0]['texto'], u'Loria y Sarmiento.')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18120, u'Domingo Faustino Sarmiento', 'lomas_de_zamora', u'Lomas de Zamora')
        # Comienzo y final
        res = self.nd.buscarDireccion(u'Loria y Sarmiento')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria y Sarmiento')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18120, u'Domingo Faustino Sarmiento', 'lomas_de_zamora', u'Lomas de Zamora')

    def test_CalleYCalle_direcciones_con_y_y_con_e(self):
        # Con y
        res = self.nd.buscarDireccion(u'Loria y España')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria y España')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18117, u'España', 'lomas_de_zamora', u'Lomas de Zamora')
        # Con e
        res = self.nd.buscarDireccion(u'Loria e Italia')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria e Italia')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18119, u'Italia', 'lomas_de_zamora', u'Lomas de Zamora')

    def test_CalleYCalle_direccion_con_calles_de_una_palabra(self):
        res = self.nd.buscarDireccion(u'Arenales y Fonrouge')
        self.assertEqual(len(res), 1, u'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Arenales y Fonrouge')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 360326, u'General Arenales', 160708, u'Julio Fonrouge', 'lomas_de_zamora', u'Lomas de Zamora')

        res = self.nd.buscarDireccion(u'Loria e italia')
        self.assertEqual(len(res), 1, u'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria e italia')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18119, u'Italia', 'lomas_de_zamora', u'Lomas de Zamora')

        res = self.nd.buscarDireccion(u'malabia y palacios')
        self.assertEqual(len(res), 1, u'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'malabia y palacios')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 553, u'Malabia', 628, u'General Palacios', 'lomas_de_zamora', u'Banfield')

        res = self.nd.buscarDireccion(u'brown y peron')
        self.assertEqual(len(res), 1, u'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'brown y peron')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 25606, u'Almirante Brown', 196982, u'Av. Eva Perón', 'lomas_de_zamora', u'Temperley')

    def test_CalleYCalle_direccion_con_calles_de_mas_de_una_palabra(self):
        res = self.nd.buscarDireccion(u'General Arenales y Julio Fonrouge')
        self.assertEqual(len(res), 1, u'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'General Arenales y Julio Fonrouge')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 360326, u'General Arenales', 160708, u'Julio Fonrouge', 'lomas_de_zamora', u'Lomas de Zamora')

    def test_CalleYCalle_el_orden_de_los_factores_altera_el_producto(self):
        res = self.nd.buscarDireccion(u'Arenales y Fonrouge')
        self.assertEqual(len(res), 1, u'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 360326, u'General Arenales', 160708, u'Julio Fonrouge', 'lomas_de_zamora', u'Lomas de Zamora')

        res = self.nd.buscarDireccion(u'Fonrouge y Arenales')
        self.assertEqual(len(res), 1, u'Debería haber 1 dirección. Hay {0}'.format(len(res)))
        self.assertEqual(len(res[0]['direcciones']), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res[0]['direcciones'])))
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 160708, u'Julio Fonrouge', 360326, u'General Arenales', 'lomas_de_zamora', u'Lomas de Zamora')

    def test_CalleYCalle_ojo_con_este_caso_palabra_colada(self):
        res = self.nd.buscarDireccion(u'Loria y Meeks, a metros de la estación.')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['posicion'], 0)
        self.assertEqual(res[0]['texto'], u'Loria y Meeks, a')
        self._checkDireccionCalleYCalle(res[0]['direcciones'][0], 18074, u'Mariano Sánchez de Loria', 18112, u'Av. Meeks', 'lomas_de_zamora', u'Lomas de Zamora')
