# coding: UTF-8
import unittest
import sys, os
from urllib2 import HTTPError
sys.path.append(os.path.join('..','src'))

from Callejero import Callejero
from Partido import Partido
from Calle import Calle
from Errors import *

class CallejeroTestCase(unittest.TestCase):
    p = Partido('jose_c_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
    c = Callejero(p)

## Lo deshabilito porque tarda mucho
#    def testCallejero_callejero_inexistent(self):
#        p = Partido('jose_paz', u'José C. Paz', u'Partido de José C. Paz', 2430431)
#        self.assertRaises(HTTPError, Callejero, p)
            
    def testCallejero_matcheaCalle_calle_inexistente(self):
        res = self.c.matcheaCalle('kokusai dori')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 0, u'No debería haber matching.')
        
    def testCallejero_matcheaCalle_unica_calle_existente(self):
        res = self.c.matcheaCalle(u'Santiago de Compostela')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 30417877)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_matcheaCalle_nombre_permutado(self):
        res = self.c.matcheaCalle(u'Compostela Santiago de')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 30417877)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_matcheaCalle_nombre_incompleto(self):
        res = self.c.matcheaCalle(u'Compos Santi')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 30417877)
        self.assertEqual(calle.nombre, u'Santiago de Compostela')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_matcheaCalle_nombre_con_acento_y_case(self):
        res = self.c.matcheaCalle(u'PoToSÍ')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 solo matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.codigo, 182271149)
        self.assertEqual(calle.nombre, u'Potosí')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_matcheaCalle_nombre_con_enie(self):
        res = self.c.matcheaCalle(u'Roque Saenz Peña')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matching.')
        calle = res[0]
        self.assertTrue(isinstance(calle, Calle))
        self.assertEqual(calle.nombre, u'Roque Sáenz Peña')
        self.assertEqual(calle.partido.codigo, 'jose_c_paz')

    def testCallejero_matcheaCalle_calle_con_varios_tramos(self):
        res = self.c.matcheaCalle(u'Santiago de Liniers')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertEqual(calle.nombre, u'Santiago de Liniers')
    
    def testCallejero_matcheaCalle_multiples_calles_existentes(self):
        res = self.c.matcheaCalle(u'San')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 7, u'Debería haber 7 matchings.')
        resCalles = [u'San Nicolás', u'Santiago de Compostela', u'San Luis', u'San Lorenzo', u'Santiago del Estero', u'Santiago de Liniers']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testCallejero_matcheaCalle_calles_con_y_01(self):
        res = self.c.matcheaCalle(u'Gelly y Obes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
        resCalles = [u'Gelly y Obes']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)
            
        res = self.c.matcheaCalle(u'g y o')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
        resCalles = [u'Gelly y Obes']
        for calle in res:
            self.assertTrue(isinstance(calle, Calle))
            self.assertTrue(calle.nombre in resCalles)

    def testCallejero_matcheaCalle_calles_con_y_02(self):
        res = self.c.matcheaCalle(u'Juan de Torres de Vera y Aragon')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Juan de Torres de Vera y Aragon')
        
        res = self.c.matcheaCalle(u'Ju de To Vera  Ara')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1, u'Debería haber 1 matching.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Juan de Torres de Vera y Aragon')

    def testCallejero_matcheaCalle_calles_con_y_03(self):
        res = self.c.matcheaCalle(u'Vicente López y Planes')
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 2, u'Debería haber 2 matchings.')
        self.assertTrue(isinstance(res[0], Calle))
        self.assertTrue(res[0].nombre == u'Vicente López y Planes')

    def testCallejero_buscarCodigo_codigo_valido(self):
        res = self.c.buscarCodigo(190141705)
        self.assertTrue(isinstance(res, list))
        self.assertTrue(res[0] == 190141705)
        self.assertTrue(res[1] == u'Avenida Derqui (M) / Fray Antonio Marchena (JCP)')

    def testCallejero_buscarCodigo_codigo_invalido(self):
        res = self.c.buscarCodigo(666)
        self.assertTrue(res == None)

    def testCallejero_matcheaCalle_sinonimos_01(self):
        res1 = self.c.matcheaCalle(u'11')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.c.matcheaCalle(u'once')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo,res2[0].codigo)

        res1 = self.c.matcheaCalle(u'3')
        self.assertTrue(isinstance(res1, list))
        self.assertEqual(len(res1), 1, u'Debería haber 1 matching.')
        res2 = self.c.matcheaCalle(u'tres')
        self.assertTrue(isinstance(res2, list))
        self.assertEqual(len(res2), 1, u'Debería haber 1 matching.')
        self.assertEqual(res1[0].codigo,res2[0].codigo)

        
#    def testCalleConEnieEscritaConNConAlturaValida2(self):
#        res = self.nd.normalizar("el nandu 3144")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 5041)
#        self.assertEqual(d.getCalle().nom, u"EL ÑANDU")
#        self.assertEqual(d.getAltura(), 3144)
#
#    def testCalleConDieresisConAlturaValida(self):
#        res = self.nd.normalizar("agüero 2144")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 1022)
#        self.assertEqual(d.getCalle().nom, "AGUERO")
#        self.assertEqual(d.getAltura(), 2144)
#         
#    def testCalleConDieresisConAlturaValida2(self):
#        res = self.nd.normalizar("AGÜERO 2144")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 1022)
#        self.assertEqual(d.getCalle().nom, "AGUERO")
#        self.assertEqual(d.getAltura(), 2144)
#
#    def testCalleConApostrofeConAlturaValida(self):
#        res = self.nd.normalizar("o'higgins 2144")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 16009)
#        self.assertEqual(d.getCalle().nom, u"O'HIGGINS")
#        self.assertEqual(d.getAltura(), 2144)
#
#    def testCalleQueEsAvPeroElNombreNoDice(self):
#        res = self.nd.normalizar("av montes de oca 100")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 13115)
#        self.assertEqual(d.getCalle().nom, "MONTES DE OCA, MANUEL")
#        self.assertEqual(d.getAltura(), 100)
#
#    def testCalleQueEsAvPeroNoALaAlturaQueDice(self):
#        res = self.nd.normalizar("av. monroe 2224")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 4111)
#        self.assertEqual(d.getCalle().nom, "MONROE")
#        self.assertEqual(d.getAltura(), 2224)
#        
#    def testCalleQueEsAvPeroNoALaAlturaQueDice2(self):
#        self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd.normalizar, "Av. Sarmiento 2550")
#
#    def testCalleQueEsAvPeroNoALaAlturaQueDice3(self):
#        self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd.normalizar, "Av. San Martin 550")
#
#    def testCalleQueEsAvPeroNoALaAlturaQueDice4(self):
#        res = self.nd.normalizar("OLLEROS AV. 3718")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 16022)
#        self.assertEqual(d.getCalle().nom, "OLLEROS")
#        self.assertEqual(d.getAltura(), 3718)
#    
#    def testCalleQueEsPasajePeroElNombreNoDice(self):
#        res = self.nd.normalizar("pasaje portugal 530")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 17113)
#        self.assertEqual(d.getCalle().nom, "PORTUGAL")
#        self.assertEqual(d.getAltura(), 530)
#
#    def testCalleQueEsPasajePeroElNombreNoDice2(self):
#        res = self.nd.normalizar("portugal pje 530")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 17113)
#        self.assertEqual(d.getCalle().nom, "PORTUGAL")
#        self.assertEqual(d.getAltura(), 530)
#
#    def testCalleValidaQueNoTieneAlturas(self):
#        self.assertRaises(ErrorCalleSinAlturas, self.nd.normalizar, "aerolineas argentinas 550")
#
#    def testCalleValidaQueNoTieneAlturas2(self):
#        self.assertRaises(ErrorCalleSinAlturas, self.nd.normalizar, "de los italianos 850")
#    
#    def testAlturasSN1(self):
#        self.nd.aceptarCallesSinAlturas = True
#
#        res = self.nd.normalizar("de los italianos s/n")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 4046)
#        self.assertEqual(d.getCalle().nom, "DE LOS ITALIANOS AV.")
#        self.assertEqual(d.getAltura(), 0)
#        
#        res = self.nd.normalizar("de los italianos S/n")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 4046)
#        self.assertEqual(d.getCalle().nom, "DE LOS ITALIANOS AV.")
#        self.assertEqual(d.getAltura(), 0)
#        
#        res = self.nd.normalizar("de los italianos S\\N")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 4046)
#        self.assertEqual(d.getCalle().nom, "DE LOS ITALIANOS AV.")
#        self.assertEqual(d.getAltura(), 0)
#        
#        res = self.nd.normalizar("aerolineas argentinas s/N")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 1002)
#        self.assertEqual(d.getCalle().nom, "AEROLINEAS ARGENTINAS")
#        self.assertEqual(d.getAltura(), 0)
#        
#        self.nd.aceptarCallesSinAlturas = False
#
#    def testAlturasSN2(self):
#        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "de los italianos s/n")
#
#    def testAlturasSN3(self):
#        self.nd.aceptarCallesSinAlturas = True
#        self.assertRaises(ErrorCalleInexistenteAEsaAltura, self.nd.normalizar, "callao s/n")
#        self.nd.aceptarCallesSinAlturas = False
#
#    def testCalleConYSinAltura1(self):
#        self.nd.aceptarCallesSinAlturas = True
#        
#        res = self.nd.normalizar("serrano s/n")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 20136)
#        self.assertEqual(d.getCalle().nom, "SERRANO, ENRIQUE (NO OFICIAL)")
#        self.assertEqual(d.getAltura(), 0)
#
#        self.nd.aceptarCallesSinAlturas = False
#        
#    def testCalleConYSinAltura2(self):
#        self.nd.aceptarCallesSinAlturas = True
#        
#        res = self.nd.normalizar("serrano 300")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 20090)
#        self.assertEqual(d.getCalle().nom, "SERRANO")
#        self.assertEqual(d.getAltura(), 300)
#
#        self.nd.aceptarCallesSinAlturas = False
#
#    def testCalleConYSinAltura3(self):
#        self.nd.aceptarCallesSinAlturas = False
#        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "serrano s/n")
#
#    def testCalleConYSinAltura4(self):
#        self.nd.aceptarCallesSinAlturas = False
#
#        res = self.nd.normalizar("serrano 300")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 20090)
#        self.assertEqual(d.getCalle().nom, "SERRANO")
#        self.assertEqual(d.getAltura(), 300)
#
#    def testCallesConY1(self):
#        res = self.nd.normalizar("PI Y MARGALL 1256")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 17094)
#        self.assertEqual(d.getCalle().nom, "PI Y MARGALL")
#        self.assertEqual(d.getAltura(), 1256)
#
#    def testCallesConY2(self):
#        res = self.nd.normalizar("RAMON Y CAJAL 1250")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 19006)
#        self.assertEqual(d.getCalle().nom, "RAMON Y CAJAL")
#        self.assertEqual(d.getAltura(), 1250)
#
#    def testCalleConMuchosEspacios(self):
#        res = self.nd.normalizar("      pasaje    portugal       530       ")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 17113)
#        self.assertEqual(d.getCalle().nom, "PORTUGAL")
#        self.assertEqual(d.getAltura(), 530)
#        
#    def testCalleConParentesis(self):
#        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "Asamblea (bajo autopista)")
#
#    def testCalleConCaracteresRaros(self):
#        self.assertRaises(ErrorCalleInexistente, self.nd.normalizar, "|°¬!#$%&/()=?\¿¡*¸+~{[^}]'`-_.:,;<>·@")
#
#    def testCalleConSeparadoresYyE01(self):
#        res = self.nd.normalizar("URIBURU JOSE E., Pres. 1003")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 22012)
#        self.assertEqual(d.getCalle().nom, "URIBURU JOSE E., Pres.")
#        self.assertEqual(d.getAltura(), 1003)
#
#    def testCalleConSeparadoresYyE02(self):
#        res = self.nd.normalizar("BATLLE Y ORDOÑEZ, JOSE P.T. 5105")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 20117)
#        self.assertEqual(d.getCalle().nom, u"BATLLE Y ORDOÑEZ, JOSE P.T.")
#        self.assertEqual(d.getAltura(), 5105)
#
#    def testCalleConSeparadoresYyE03(self):
#        res = self.nd.normalizar("BENEDETTI, OSVALDO E., Dip.Nac. 14")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 12031)
#        self.assertEqual(d.getCalle().nom, "BENEDETTI, OSVALDO E., Dip.Nac.")
#        self.assertEqual(d.getAltura(), 14)
#
#    def testCalleConSeparadoresYyE04(self):
#        res = self.nd.normalizar("BUTTY, E., Ing. 240")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 17147)
#        self.assertEqual(d.getCalle().nom, "BUTTY, E., Ing.")
#        self.assertEqual(d.getAltura(), 240)
#
#    def testCalleConSeparadoresYyE05(self):
#        res = self.nd.normalizar("CARBALLIDO, JOSE E. 6310")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 3066)
#        self.assertEqual(d.getCalle().nom, "CARBALLIDO, JOSE E.")
#        self.assertEqual(d.getAltura(), 6310)
#
#    def testCalleConSeparadoresYyE06(self):
#        res = self.nd.normalizar("FREYRE, MARCELINO E., Cnel. AV. 3800")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 6056)
#        self.assertEqual(d.getCalle().nom, "FREYRE, MARCELINO E., Cnel. AV.")
#        self.assertEqual(d.getAltura(), 3800)
#
#    def testCalleConSeparadoresYyE07(self):
#        res = self.nd.normalizar("FRIAS, EUSTOQUIO, TTE. GENERAL 120")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 6058)
#        self.assertEqual(d.getCalle().nom, "FRIAS, EUSTAQUIO, TTE. GENERAL")
#        self.assertEqual(d.getAltura(), 120)
#
#    def testCalleConSeparadoresYyE08(self):
#        res = self.nd.normalizar("GUIDO y SPANO, CARLOS 1107")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 7103)
#        self.assertEqual(d.getCalle().nom, "GUIDO y SPANO, CARLOS")
#        self.assertEqual(d.getAltura(), 1107)
#
#    def testCalleConSeparadoresYyE09(self):
#        res = self.nd.normalizar("MATORRAS de SAN MARTIN, GREGORIA 2211")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 13051)
#        self.assertEqual(d.getCalle().nom, "MATORRAS de SAN MARTIN, GREGORIA")
#        self.assertEqual(d.getAltura(), 2211)
#
#    def testCalleConSeparadoresYyE10(self):
#        res = self.nd.normalizar("PAZ Y FIGUEROA, MARIA ANTONIA de la 4541")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 17046)
#        self.assertEqual(d.getCalle().nom, "PAZ Y FIGUEROA, MARIA ANTONIA de la")
#        self.assertEqual(d.getAltura(), 4541)
#
#    def testCalleConSeparadoresYyE11(self):
#        res = self.nd.normalizar("PELLEGRINI, CARLOS E. 6042")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 17053)
#        self.assertEqual(d.getCalle().nom, "PELLEGRINI, CARLOS E.")
#        self.assertEqual(d.getAltura(), 6042)
#
#    def testCalleConSeparadoresYyE12(self):
#        res = self.nd.normalizar("RODO, JOSE E. 3729")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 19064)
#        self.assertEqual(d.getCalle().nom, "RODO, JOSE E.")
#        self.assertEqual(d.getAltura(), 3729)
#
#    def testCalleConSeparadoresYyE13(self):
#        res = self.nd.normalizar("MATORRAS de SAN MARTIN, Gregoria 2222")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 13051)
#        self.assertEqual(d.getCalle().nom, "MATORRAS de SAN MARTIN, GREGORIA")
#        self.assertEqual(d.getAltura(), 2222)
#
#    def testCalleConSeparadoresYyE14(self):
#        res = self.nd.normalizar("VIDAL EMERIC E. 1583")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 23050)
#        self.assertEqual(d.getCalle().nom, "VIDAL EMERIC E.")
#        self.assertEqual(d.getAltura(), 1583)
#
#    def testOtraCalleConE01(self):
#        res = self.nd.normalizar("VIDELA, NICOLAS E. 430")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 23052)
#        self.assertEqual(d.getCalle().nom, "VIDELA, NICOLAS E.")
#        self.assertEqual(d.getAltura(), 430)
#
#    def testOtraCalleConE02(self):
#        res = self.nd.normalizar("RODO, JOSE E. 5400")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 19064)
#        self.assertEqual(d.getCalle().nom, "RODO, JOSE E.")
#        self.assertEqual(d.getAltura(), 5400)
#
#
#    def testMatchComienzoDePalabra(self):
#        res = self.nd.normalizar("Dob 105")
#        self.assertTrue(isinstance(res, list))
#        self.assertEqual(len(res), 1, "Deberia haber un unico matching")
#        d = res[0]
#        self.assertTrue(isinstance(d, Direccion))
#        self.assertEqual(d.getCalle().cod, 4079)
#        self.assertEqual(d.getCalle().nom, "DOBLAS")
#        self.assertEqual(d.getAltura(), 105)