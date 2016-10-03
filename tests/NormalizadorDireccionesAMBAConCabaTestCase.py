# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.settings import CALLE_ALTURA

from test_commons import cargarCallejeroEstatico


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
        res = self.nd.normalizar(u'Arenales 806')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 3, u'Debería haber 3 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 1104, u'ARENALES', 806, 'caba', u'CABA')
        self._checkDireccion(res[1], 53565, u'Gral Arenales', 806, 'jose_c_paz', u'José C. Paz')
        self._checkDireccion(res[2], 360326, u'General Arenales', 806, 'lomas_de_zamora', u'Lomas de Zamora')

    def testDireccionSoloEnCaba(self):
        res = self.nd.normalizar(u'Callao 1536')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 3030, u'CALLAO AV.', 1536, 'caba', u'CABA')

    def testDireccionSoloEnConurbano(self):
        res = self.nd.normalizar(u'Laprida 890')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 156179, u'Laprida', 890, 'jose_c_paz', u'José C. Paz')
        self._checkDireccion(res[1], 18028, u'Laprida', 890, 'lomas_de_zamora', u'Lomas de Zamora')

    def testDireccionEnCabaYConurbanoConFiltroEnCaba(self):
        res = self.nd.normalizar(u'Arenales 806, caba')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 1104, u'ARENALES', 806, 'caba', u'CABA')

    def testDireccionEnCabaYConurbanoConFiltroEnConurbano1(self):
        res = self.nd.normalizar(u'Arenales 806, lomas')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 360326, u'General Arenales', 806, 'lomas_de_zamora', u'Lomas de Zamora')

    def testDireccionEnCabaYConurbanoConFiltroEnConurbano2(self):
        res = self.nd.normalizar(u'Arenales 806, Jose c Paz')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching/s. Hay {0}'.format(len(res)))

        self._checkDireccion(res[0], 53565, u'Gral Arenales', 806, 'jose_c_paz', u'José C. Paz')

    def testNormalizador_normalizar_calles_como_av_o_pje(self):
        casos = [
            u'Avenida Paraná 853, caba',
            u'Paraná avenida 853, caba',
            u'Paraná avda 853, caba',
            u'AV. Paraná 853, caba',
            u'Pasaje Paraná 853, caba',
            u'Psje. Paraná 853, caba',
            u'Paraná pje. 853, caba'
        ]
        for caso in casos:
            res = self.nd.normalizar(caso)
            self.assertTrue(isinstance(res, list))
            self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
            self._checkDireccion(res[0], 17018, u'PARANA', 853, 'caba', u'CABA')
