# coding: UTF-8
import unittest
import sys, os
import simplejson as json
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from NormalizadorDirecciones import *
from Partido import Partido
from Errors import *
from settings import *

class CalleAlturaTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    nd = NormalizadorDirecciones(p)

    # Cargo los callejeros congelados
    with open('callejeros/jose_c_paz.callejero') as data_file:
        data = json.load(data_file)
    nd.c.data = data
    nd.c.data.sort()
    nd.c.osm_ids = [k[0] for k in nd.c.data]

    def _checkDireccion(self, direccion, codigo, nombre, altura):
        self.assertTrue(isinstance(direccion, Direccion))
        self.assertEqual(direccion.calle.codigo, codigo)
        self.assertEqual(direccion.calle.nombre, nombre)
        self.assertEqual(direccion.altura, altura)

    def testCalleInexistente(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "Evergreen Terrace 742")
         
    def testCalleInexistente2(self):
        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "av arcos 1234")
 
    def testUnicaCalleExistente(self):
        res = self.nd.normalizar(u'Roque Sáenz Peña 5050')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0],77440,u'Roque Sáenz Peña', 5050)
 
    def testUnicaCalleExistenteConAlturaInexistente(self):
        self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd.normalizar, u'Roque Sáenz Peña 505')
 
    def testMuchasCallesSinAlturaValida(self):
        try:
            res = self.nd.normalizar(u'santiago 5000')
            self.assertTrue(False, "Si llega aca es que no tiro la excepcion")
        except Exception, e:
            self.assertTrue(isinstance(e, ErrorCalleInexistenteAEsaAltura))
 
    def testMuchasCallesUnaConAlturaValida(self):
        res = self.nd.normalizar(u'santiago 4000')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[0], 11840, u'Santiago del Estero', 4000)
         
    def testMuchasCallesVariasConAlturaValida(self):
        res = self.nd.normalizar(u'santiago 3500')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, "Deberia haber 2 matchings")
        self._checkDireccion(res[0], 11840, u'Santiago del Estero', 3500)
        self._checkDireccion(res[1], 77662, u'Santiago L. Copello', 3500)
 
    def testCalleConPuntoConAlturaValida(self):
        res = self.nd.normalizar("Santiago L. Copello 817")
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
        self._checkDireccion(res[1], 77662, u'Santiago L. Copello', 817)
 
#     def testCalleConEnieConAlturaValida(self):
#         res = self.nd.normalizar('ñandú 3144')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 5041)
#         self.assertEqual(d.getCalle().nom, u"EL ÑANDU")
#         self.assertEqual(d.getAltura(), 3144)
#         
#     def testCalleConEnieConAlturaValida2(self):
#         res = self.nd.normalizar("el.ñandú 3144")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 5041)
#         self.assertEqual(d.getCalle().nom, u"EL ÑANDU")
#         self.assertEqual(d.getAltura(), 3144)
#         
#     def testCalleConEnieEscritaConNConAlturaValida2(self):
#         res = self.nd.normalizar("el nandu 3144")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 5041)
#         self.assertEqual(d.getCalle().nom, u"EL ÑANDU")
#         self.assertEqual(d.getAltura(), 3144)
# 
#     def testCalleConDieresisConAlturaValida(self):
#         res = self.nd.normalizar("agüero 2144")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 1022)
#         self.assertEqual(d.getCalle().nom, "AGUERO")
#         self.assertEqual(d.getAltura(), 2144)
#          
#     def testCalleConDieresisConAlturaValida2(self):
#         res = self.nd.normalizar("AGÜERO 2144")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 1022)
#         self.assertEqual(d.getCalle().nom, "AGUERO")
#         self.assertEqual(d.getAltura(), 2144)
# 
#     def testCalleConApostrofeConAlturaValida(self):
#         res = self.nd.normalizar("o'higgins 2144")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 16009)
#         self.assertEqual(d.getCalle().nom, u"O'HIGGINS")
#         self.assertEqual(d.getAltura(), 2144)
# 
#     def testCalleQueEsAvPeroElNombreNoDice(self):
#         res = self.nd.normalizar("av montes de oca 100")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 13115)
#         self.assertEqual(d.getCalle().nom, "MONTES DE OCA, MANUEL")
#         self.assertEqual(d.getAltura(), 100)
# 
#     def testCalleQueEsAvPeroNoALaAlturaQueDice(self):
#         res = self.nd.normalizar("av. monroe 2224")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 4111)
#         self.assertEqual(d.getCalle().nom, "MONROE")
#         self.assertEqual(d.getAltura(), 2224)
#         
#     def testCalleQueEsAvPeroNoALaAlturaQueDice2(self):
#         self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd.normalizar, "Av. Sarmiento 2550")
# 
#     def testCalleQueEsAvPeroNoALaAlturaQueDice3(self):
#         self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd.normalizar, "Av. San Martin 550")
# 
#     def testCalleQueEsAvPeroNoALaAlturaQueDice4(self):
#         res = self.nd.normalizar("OLLEROS AV. 3718")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 16022)
#         self.assertEqual(d.getCalle().nom, "OLLEROS")
#         self.assertEqual(d.getAltura(), 3718)
#     
#     def testCalleQueEsPasajePeroElNombreNoDice(self):
#         res = self.nd.normalizar("pasaje portugal 530")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 17113)
#         self.assertEqual(d.getCalle().nom, "PORTUGAL")
#         self.assertEqual(d.getAltura(), 530)
# 
#     def testCalleQueEsPasajePeroElNombreNoDice2(self):
#         res = self.nd.normalizar("portugal pje 530")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 17113)
#         self.assertEqual(d.getCalle().nom, "PORTUGAL")
#         self.assertEqual(d.getAltura(), 530)
# 
#     def testCalleValidaQueNoTieneAlturas(self):
#         self.assertRaises(ErrorCalleSinAlturas, self.nd.normalizar, "aerolineas argentinas 550")
# 
#     def testCalleValidaQueNoTieneAlturas2(self):
#         self.assertRaises(ErrorCalleSinAlturas, self.nd.normalizar, "de los italianos 850")
#     
#     def testAlturasSN1(self):
#         self.nd.aceptarCallesSinAlturas = True
# 
#         res = self.nd.normalizar("de los italianos s/n")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 4046)
#         self.assertEqual(d.getCalle().nom, "DE LOS ITALIANOS AV.")
#         self.assertEqual(d.getAltura(), 0)
#         
#         res = self.nd.normalizar("de los italianos S/n")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 4046)
#         self.assertEqual(d.getCalle().nom, "DE LOS ITALIANOS AV.")
#         self.assertEqual(d.getAltura(), 0)
#         
#         res = self.nd.normalizar("de los italianos S\\N")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 4046)
#         self.assertEqual(d.getCalle().nom, "DE LOS ITALIANOS AV.")
#         self.assertEqual(d.getAltura(), 0)
#         
#         res = self.nd.normalizar("aerolineas argentinas s/N")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 1002)
#         self.assertEqual(d.getCalle().nom, "AEROLINEAS ARGENTINAS")
#         self.assertEqual(d.getAltura(), 0)
#         
#         self.nd.aceptarCallesSinAlturas = False
# 
#     def testAlturasSN2(self):
#         self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "de los italianos s/n")
# 
#     def testAlturasSN3(self):
#         self.nd.aceptarCallesSinAlturas = True
#         self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd.normalizar, "callao s/n")
#         self.nd.aceptarCallesSinAlturas = False
# 
#     def testCalleConYSinAltura1(self):
#         self.nd.aceptarCallesSinAlturas = True
#         
#         res = self.nd.normalizar("serrano s/n")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 20136)
#         self.assertEqual(d.getCalle().nom, "SERRANO, ENRIQUE (NO OFICIAL)")
#         self.assertEqual(d.getAltura(), 0)
# 
#         self.nd.aceptarCallesSinAlturas = False
#         
#     def testCalleConYSinAltura2(self):
#         self.nd.aceptarCallesSinAlturas = True
#         
#         res = self.nd.normalizar("serrano 300")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 20090)
#         self.assertEqual(d.getCalle().nom, "SERRANO")
#         self.assertEqual(d.getAltura(), 300)
# 
#         self.nd.aceptarCallesSinAlturas = False
# 
#     def testCalleConYSinAltura3(self):
#         self.nd.aceptarCallesSinAlturas = False
#         self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "serrano s/n")
# 
#     def testCalleConYSinAltura4(self):
#         self.nd.aceptarCallesSinAlturas = False
# 
#         res = self.nd.normalizar("serrano 300")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 20090)
#         self.assertEqual(d.getCalle().nom, "SERRANO")
#         self.assertEqual(d.getAltura(), 300)
# 
#     def testCallesConY1(self):
#         res = self.nd.normalizar("PI Y MARGALL 1256")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 17094)
#         self.assertEqual(d.getCalle().nom, "PI Y MARGALL")
#         self.assertEqual(d.getAltura(), 1256)
# 
#     def testCallesConY2(self):
#         res = self.nd.normalizar("RAMON Y CAJAL 1250")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 19006)
#         self.assertEqual(d.getCalle().nom, "RAMON Y CAJAL")
#         self.assertEqual(d.getAltura(), 1250)
# 
#     def testCalleConMuchosEspacios(self):
#         res = self.nd.normalizar("      pasaje    portugal       530       ")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 17113)
#         self.assertEqual(d.getCalle().nom, "PORTUGAL")
#         self.assertEqual(d.getAltura(), 530)
#         
#     def testCalleConParentesis(self):
#         self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "Asamblea (bajo autopista)")
# 
#     def testCalleConCaracteresRaros(self):
#         self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "|°¬!#$%&/()=?\¿¡*¸+~{[^}]'`-_.:,;<>·@")
# 
#     def testCalleConSeparadoresYyE01(self):
#         res = self.nd.normalizar("URIBURU JOSE E., Pres. 1003")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 22012)
#         self.assertEqual(d.getCalle().nom, "URIBURU JOSE E., Pres.")
#         self.assertEqual(d.getAltura(), 1003)
# 
#     def testCalleConSeparadoresYyE02(self):
#         res = self.nd.normalizar("BATLLE Y ORDOÑEZ, JOSE P.T. 5105")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 20117)
#         self.assertEqual(d.getCalle().nom, u"BATLLE Y ORDOÑEZ, JOSE P.T.")
#         self.assertEqual(d.getAltura(), 5105)
# 
#     def testCalleConSeparadoresYyE03(self):
#         res = self.nd.normalizar("BENEDETTI, OSVALDO E., Dip.Nac. 14")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 12031)
#         self.assertEqual(d.getCalle().nom, "BENEDETTI, OSVALDO E., Dip.Nac.")
#         self.assertEqual(d.getAltura(), 14)
# 
#     def testCalleConSeparadoresYyE04(self):
#         res = self.nd.normalizar("BUTTY, E., Ing. 240")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 17147)
#         self.assertEqual(d.getCalle().nom, "BUTTY, E., Ing.")
#         self.assertEqual(d.getAltura(), 240)
# 
#     def testCalleConSeparadoresYyE05(self):
#         res = self.nd.normalizar("CARBALLIDO, JOSE E. 6310")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 3066)
#         self.assertEqual(d.getCalle().nom, "CARBALLIDO, JOSE E.")
#         self.assertEqual(d.getAltura(), 6310)
# 
#     def testCalleConSeparadoresYyE06(self):
#         res = self.nd.normalizar("FREYRE, MARCELINO E., Cnel. AV. 3800")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 6056)
#         self.assertEqual(d.getCalle().nom, "FREYRE, MARCELINO E., Cnel. AV.")
#         self.assertEqual(d.getAltura(), 3800)
# 
#     def testCalleConSeparadoresYyE07(self):
#         res = self.nd.normalizar("FRIAS, EUSTOQUIO, TTE. GENERAL 120")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 6058)
#         self.assertEqual(d.getCalle().nom, "FRIAS, EUSTAQUIO, TTE. GENERAL")
#         self.assertEqual(d.getAltura(), 120)
# 
#     def testCalleConSeparadoresYyE08(self):
#         res = self.nd.normalizar("GUIDO y SPANO, CARLOS 1107")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 7103)
#         self.assertEqual(d.getCalle().nom, "GUIDO y SPANO, CARLOS")
#         self.assertEqual(d.getAltura(), 1107)
# 
#     def testCalleConSeparadoresYyE09(self):
#         res = self.nd.normalizar("MATORRAS de SAN MARTIN, GREGORIA 2211")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 13051)
#         self.assertEqual(d.getCalle().nom, "MATORRAS de SAN MARTIN, GREGORIA")
#         self.assertEqual(d.getAltura(), 2211)
# 
#     def testCalleConSeparadoresYyE10(self):
#         res = self.nd.normalizar("PAZ Y FIGUEROA, MARIA ANTONIA de la 4541")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 17046)
#         self.assertEqual(d.getCalle().nom, "PAZ Y FIGUEROA, MARIA ANTONIA de la")
#         self.assertEqual(d.getAltura(), 4541)
# 
#     def testCalleConSeparadoresYyE11(self):
#         res = self.nd.normalizar("PELLEGRINI, CARLOS E. 6042")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 17053)
#         self.assertEqual(d.getCalle().nom, "PELLEGRINI, CARLOS E.")
#         self.assertEqual(d.getAltura(), 6042)
# 
#     def testCalleConSeparadoresYyE12(self):
#         res = self.nd.normalizar("RODO, JOSE E. 3729")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 19064)
#         self.assertEqual(d.getCalle().nom, "RODO, JOSE E.")
#         self.assertEqual(d.getAltura(), 3729)
# 
#     def testCalleConSeparadoresYyE13(self):
#         res = self.nd.normalizar("MATORRAS de SAN MARTIN, Gregoria 2222")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 13051)
#         self.assertEqual(d.getCalle().nom, "MATORRAS de SAN MARTIN, GREGORIA")
#         self.assertEqual(d.getAltura(), 2222)
# 
#     def testCalleConSeparadoresYyE14(self):
#         res = self.nd.normalizar("VIDAL EMERIC E. 1583")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 23050)
#         self.assertEqual(d.getCalle().nom, "VIDAL EMERIC E.")
#         self.assertEqual(d.getAltura(), 1583)
# 
#     def testOtraCalleConE01(self):
#         res = self.nd.normalizar("VIDELA, NICOLAS E. 430")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 23052)
#         self.assertEqual(d.getCalle().nom, "VIDELA, NICOLAS E.")
#         self.assertEqual(d.getAltura(), 430)
# 
#     def testOtraCalleConE02(self):
#         res = self.nd.normalizar("RODO, JOSE E. 5400")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 19064)
#         self.assertEqual(d.getCalle().nom, "RODO, JOSE E.")
#         self.assertEqual(d.getAltura(), 5400)
# 
# 
#     def testMatchComienzoDePalabra(self):
#         res = self.nd.normalizar("Dob 105")
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.getCalle().cod, 4079)
#         self.assertEqual(d.getCalle().nom, "DOBLAS")
#         self.assertEqual(d.getAltura(), 105)
# 
# 
# 
# 
# 
# 
# 
# 
#     
#     def testCalleInexistente01(self):
#         self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'Elm street y Roque Sáenz Peña')
# 
#     def testCalleInexistente02(self):
#         self.assertRaises(ErrorCruceInexistente, self.nd.normalizar, u'Roque Sáenz Peña y kokusai dori')
# 
#     def testCalle1UnicaCalle2UnicaCruceInexistente(self):
#         try:
#             self.nd.normalizar('Mateo Bootz y pavon')
#         except Exception, e:
#             self.assertTrue(isinstance(e, ErrorCruceInexistente))
# 
#     def testCalle1MuchasCalle2MuchasCruceInexistente(self):
#         try:
#             self.nd.normalizar(u'saenz peña y gaspar campos')
#         except Exception, e:
#             self.assertTrue(isinstance(e, ErrorCruceInexistente))
# 
#     def testCalle1UnicaCalle2UnicaCruceExistente(self):
#         res = self.nd.normalizar(u'Suecia y libano')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 182539)
#         self.assertEqual(d.calle.nombre, u'Suecia')
#         self.assertEqual(d.cruce.codigo, 231716)
#         self.assertEqual(d.cruce.nombre, u'Líbano')
# 
#     def testCalle1UnicaCalle2MuchasCruceExistenteUnico(self):
#         res = self.nd.normalizar(u'líbano y Avenida')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 231716)
#         self.assertEqual(d.calle.nombre, u'Líbano')
#         self.assertEqual(d.cruce.codigo, 78155)
#         self.assertEqual(d.cruce.nombre, 'Avenida Croacia')
# 
#     def testCalle1MuchasCalle2UnicaCruceExistenteUnico(self):
#         res = self.nd.normalizar(u'Avenida y líbano')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 78155)
#         self.assertEqual(d.calle.nombre, u'Avenida Croacia')
#         self.assertEqual(d.cruce.codigo, 231716)
#         self.assertEqual(d.cruce.nombre, u'Líbano')
# 
#     def testCalleConY01(self):
#         res = self.nd.normalizar(u'Arias y Gelly y Obes')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 77242)
#         self.assertEqual(d.calle.nombre, 'Coronel Arias')
#         self.assertEqual(d.cruce.codigo, 77481)
#         self.assertEqual(d.cruce.nombre, u'Gelly y Obes')
# 
#     def testCalleConY02(self):
#         res = self.nd.normalizar(u'Gelly y Obes y Arias')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 77481)
#         self.assertEqual(d.calle.nombre, u'Gelly y Obes')
#         self.assertEqual(d.cruce.codigo, 77242)
#         self.assertEqual(d.cruce.nombre, 'Coronel Arias')
# 
#     def testCalleConY03(self):
#         res = self.nd.normalizar(u'Gel y Ob y Coronel Arias')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 77481)
#         self.assertEqual(d.calle.nombre, u'Gelly y Obes')
#         self.assertEqual(d.cruce.codigo, 77242)
#         self.assertEqual(d.cruce.nombre, 'Coronel Arias')
# 
#     def testCalleConYParcial01(self):
#         res = self.nd.normalizar(u'Arias y Gel y Ob')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 77242)
#         self.assertEqual(d.calle.nombre, 'Coronel Arias')
#         self.assertEqual(d.cruce.codigo, 77481)
#         self.assertEqual(d.cruce.nombre, u'Gelly y Obes')
# 
#     def testDireccionSeparadaPorE01(self):
#         res = self.nd.normalizar(u'pinero e iglesia')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber un unico matching')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 53491)
#         self.assertEqual(d.calle.nombre, u'Piñero')
#         self.assertEqual(d.cruce.codigo, 53648)
#         self.assertEqual(d.cruce.nombre, u'Iglesias')
# 
#     def testCalle1MuchasCalle2MuchasCruceExistenteMulti(self):
#         res = self.nd.normalizar(u'santiago y are')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 2, 'Deberia haber 2 matchings')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 53658) #Santiago de Compostela
#         self.assertEqual(d.cruce.codigo, 53565) #Gral Arenales
#         d = res[1]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 77662) #Santiago L. Copello
#         self.assertEqual(d.cruce.codigo, 53565) #Arturo Illia
#         
#     def testCalleConE02(self):
#         res = self.nd.normalizar(u'José E. Rodó y Paula Albarracín')
#         self.assertTrue(isinstance(res, list))
#         self.assertEqual(len(res), 1, 'Deberia haber 1 matchings')
#         d = res[0]
#         self.assertTrue(isinstance(d, Direccion))
#         self.assertEqual(d.tipo, CALLE_Y_CALLE )
#         self.assertEqual(d.calle.codigo, 78817) #José E. Rodó
#         self.assertEqual(d.cruce.codigo, 52665) #Paula Albarracín
# 
#     def testDireccionSeparadaPorECalleNoEmpiezaConI(self):
#         self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, u'miranda e arregui')

