# coding: UTF-8

import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.settings import CALLE_ALTURA

from tests.test_commons import cargarCallejeroEstatico


class NormalizadorDireccionesAMBAConCabaTestCase(unittest.TestCase):
    partidos = ['caba', 'lomas_de_zamora', 'jose_c_paz']
    nd = NormalizadorDireccionesAMBA(include_list=partidos)
    for n in nd.normalizadores:
        if n.partido.codigo != 'caba':
            cargarCallejeroEstatico(n.c)

    def _checkDireccion(self, direccion, codigo_calle, nombre_calle, altura, codigo_partido, localidad):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.tipo, CALLE_ALTURA)
        self.assertEqual(direccion.calle.codigo, codigo_calle)
        self.assertEqual(direccion.calle.nombre, nombre_calle)
        self.assertEqual(direccion.altura, altura)
        self.assertEqual(direccion.partido.codigo, codigo_partido)
        self.assertEqual(direccion.localidad, localidad)

    def testDireccionEnCabaYConurbano(self):
        res = self.nd.normalizar('Arenales 806')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 3, 'Debería haber 3 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 1104, 'ARENALES', 806, 'caba', 'CABA')
        self._checkDireccion(res[1], 53565, 'Gral Arenales', 806, 'jose_c_paz', 'José C. Paz')
        self._checkDireccion(res[2], 360326, 'General Arenales', 806, 'lomas_de_zamora', 'Lomas de Zamora')

    def testDireccionSoloEnCaba(self):
        res = self.nd.normalizar('Callao 1536')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 3030, 'CALLAO AV.', 1536, 'caba', 'CABA')

    def testDireccionSoloEnConurbano(self):
        res = self.nd.normalizar('Laprida 890')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, 'Debería haber 2 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 156179, 'Laprida', 890, 'jose_c_paz', 'José C. Paz')
        self._checkDireccion(res[1], 18028, 'Laprida', 890, 'lomas_de_zamora', 'Lomas de Zamora')

    def testDireccionEnCabaYConurbanoConFiltroEnCaba(self):
        res = self.nd.normalizar('Arenales 806, caba')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 1104, 'ARENALES', 806, 'caba', 'CABA')

    def testDireccionEnCabaYConurbanoConFiltroEnConurbano1(self):
        res = self.nd.normalizar('Arenales 806, lomas')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 360326, 'General Arenales', 806, 'lomas_de_zamora', 'Lomas de Zamora')

    def testDireccionEnCabaYConurbanoConFiltroEnConurbano2(self):
        res = self.nd.normalizar('Arenales 806, Jose c Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, 'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 53565, 'Gral Arenales', 806, 'jose_c_paz', 'José C. Paz')

    def testNormalizador_normalizar_calles_como_av_o_pje(self):
        casos = [
            'Avenida Paraná 853, caba',
            'Paraná avenida 853, caba',
            'Paraná avda 853, caba',
            'AV. Paraná 853, caba',
            'Pasaje Paraná 853, caba',
            'Psje. Paraná 853, caba',
            'Paraná pje. 853, caba'
        ]
        for caso in casos:
            res = self.nd.normalizar(caso)
            self.assertTrue(isinstance(res, list))
            self.assertEqual(len(res), 1, 'Debería haber 1 matching.')
            self._checkDireccion(res[0], 17018, 'PARANA', 853, 'caba', 'CABA')
