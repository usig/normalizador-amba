# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.NormalizadorDirecciones import NormalizadorDirecciones
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.Errors import ErrorCalleInexistenteAEsaAltura, ErrorCalleInexistente

from test_commons import cargarCallejeroEstatico


class CalleAlturaTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    nd_jcp = NormalizadorDirecciones(p)
    cargarCallejeroEstatico(nd_jcp.c)

    p = Partido('la_plata', u'La Plata', u'Partido de La Plata', 2499263)
    nd_lp = NormalizadorDirecciones(p)
    cargarCallejeroEstatico(nd_lp.c)

    def _checkDireccion(self, direccion, codigo, nombre, altura):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.calle.codigo, codigo)
        self.assertEqual(direccion.calle.nombre, nombre)
        self.assertEqual(direccion.altura, altura)

    def testCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd_jcp.normalizar, "Evergreen Terrace 742")

    def testCalleInexistente2(self):
        self.assertRaises(ErrorCalleInexistente, self.nd_jcp.normalizar, "av arcos 1234")

    def testUnicaCalleExistente(self):
        res = self.nd_jcp.normalizar(u'Roque Sáenz Peña 5050')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 77440, u'Roque Sáenz Peña', 5050)

    def testUnicaCalleExistenteConAlturaInexistente(self):
        self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd_jcp.normalizar, u'Roque Sáenz Peña 505')

    def testMuchasCallesSinAlturaValida(self):
        try:
            self.nd_jcp.normalizar(u'santiago 5000')
            self.assertTrue(False, "Si llega aca es que no tiro la excepcion")
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCalleInexistenteAEsaAltura))

    def testMuchasCallesUnaConAlturaValida(self):
        res = self.nd_jcp.normalizar(u'santiago 4000')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0],  11840, u'Santiago del Estero', 4000)

    def testMuchasCallesVariasConAlturaValida(self):
        res = self.nd_jcp.normalizar(u'santiago 3500')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, "Deberia haber 2 matchings")
        self._checkDireccion(res[0], 11840, u'Santiago del Estero', 3500)
        self._checkDireccion(res[1], 77662, u'Santiago L. Copello', 3500)

    def testCalleConPuntoConAlturaValida(self):
        res = self.nd_jcp.normalizar("Santiago L. Copello 817")
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 77662, u'Santiago L. Copello', 817)

    def testCalleConEnieConAlturaValida(self):
        res = self.nd_jcp.normalizar(u'Roque Sáenz Peña 5050')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 77440, u'Roque Sáenz Peña', 5050)

    def testCalleConEnieEscritaConNConAlturaValida2(self):
        res = self.nd_jcp.normalizar(u'Roque Sáenz Pena 5050')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 77440, u'Roque Sáenz Peña', 5050)

    def testCalleConDieresisConAlturaValida(self):
        res = self.nd_jcp.normalizar(u'echagüe 2144')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 182799, u'Juan Pablo Echagüe', 2144)

        res = self.nd_jcp.normalizar('echague 2144')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 182799, u'Juan Pablo Echagüe', 2144)

    def testCalleConApostrofe(self):
        res = self.nd_jcp.normalizar(u'D\'Elía 4321')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 53381, u'Maestro Ángel D\'Elía', 4321)

        res = self.nd_jcp.normalizar(u'D Elía 4321')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 53381, u'Maestro Ángel D\'Elía', 4321)

        res = self.nd_jcp.normalizar(u'Delía 4321')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 53381, u'Maestro Ángel D\'Elía', 4321)

    def testCallesConY(self):
        res = self.nd_jcp.normalizar(u'gelly y obes 4375')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 77481, u'Gelly y Obes', 4375)

        res = self.nd_jcp.normalizar(u'vicente lopez y planes 4375')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 11702, u'Vicente López y Planes', 4375)

    def testCalleConMuchosEspacios(self):
        res = self.nd_jcp.normalizar(u' tomas    guido    5000      ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 185640, u'Tomás Guido', 5000)

    def testCalleConCaracteresRaros(self):
        res = self.nd_jcp.normalizar(u'tomas guido 5000 |°¬!#$%&/()=?\¿¡*¸+~{[^}]`-_.:,;<>·@')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 185640, u'Tomás Guido', 5000)

    def testCalleConSeparadoresE(self):
        res = self.nd_jcp.normalizar(u'jose e rodo 3888')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 78817, u'José E. Rodó', 3888)

    def testCalleConSinonimosAvenida(self):
        res = self.nd_jcp.normalizar(u'Avenida Maestro Ferreyra 3800')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 301342, u'Av. Maestro Ferreyra', 3800)

        res = self.nd_jcp.normalizar(u'Avda Maestro Ferreyra 3800')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 301342, u'Av. Maestro Ferreyra', 3800)

    def testCalleConSinonimosDoctor(self):
        res = self.nd_jcp.normalizar(u'Dr. Angel Gallardo 5800')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 331441, u'Dr. Angel Gallardo', 5800)

        res = self.nd_jcp.normalizar(u'Doctor Angel Gallardo 5800')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 331441, u'Dr. Angel Gallardo', 5800)

    def testCalleConSinonimosDoce(self):
        res = self.nd_jcp.normalizar(u'doce de octubre 50')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 369059, u'12 de Octubre', 50)

        res = self.nd_jcp.normalizar(u'12 de octubre 50')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 369059, u'12 de Octubre', 50)

    def testMatchComienzoDePalabra(self):
        res = self.nd_jcp.normalizar(u'Ave Mae Fer 3800')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 301342, u'Av. Maestro Ferreyra', 3800)

    def testCallesQueTienenNumerosEnSuNombre01(self):
        res = self.nd_jcp.normalizar(u'18 de Octubre 3250')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 77462, u'18 de Octubre', 3250)

    def testCallesQueTienenNumerosEnSuNombre02(self):
        res = self.nd_lp.normalizar(u'Avenida 44 2000')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 356811, u'Avenida 44', 2000)

    def testCallesQueTienenNumerosEnSuNombre03(self):
        res = self.nd_lp.normalizar(u'58 1600')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 123404, u'58', 1600)
