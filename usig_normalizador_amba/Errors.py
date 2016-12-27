# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
@note: Excepciones:
    - ErrorCalleInexistente
    - ErrorCalleSinAlturas
    - ErrorCalleInexistenteAEsaAltura
    - ErrorCruceInexistente
    - ErrorTextoSinDireccion
'''
from __future__ import absolute_import
import unicodedata

class ErrorNormalizacion(Exception):
    def __init__(self):
        raise Exception()

    def __unicode__(self):
        raise Exception()

    def getErrorMessage(self):
        raise Exception()


class ErrorCalleInexistente(Exception):
    '''
    Excepcion para calle inexistente.
    '''
    calle = ''

    def __init__(self, calle):
        '''
        Constructor de la clase.
        @param calle: Nombre oficial de la calle
        @type calle: String
        '''
        self.calle = calle

    def __str__(self):
        '''
        Devuelve un mensaje de error con el nombre de la calle
        @return: Mensaje de error
        @rtype: String
        '''
        return self.__unicode__().encode('utf8', 'ignore')

    def __unicode__(self):
        return u'Calle inexistente: {0}'.format(self.calle)

    def getErrorMessage(self):
        '''
        Devuelve un mensaje de error mas descriptivo y amigable
        @return: Mensaje de error
        @rtype: String
        '''
        return u'No pudo hallarse ninguna calle existente que coincidiera con "{0}".'.format(self.calle)


class ErrorCalleInexistenteAEsaAltura(Exception):
    '''
    Excepcion para altura inexistente para una calle con altura.
    '''
    calle = ""
    matchings = []
    altura = 0

    def __init__(self, calle, matchings, altura):
        '''
        Constructor
        @param calle: Nombre oficial de la calle
        @type calle: String
        @param matchings: Array de instancias de Calle que matchean el string 'calle'
        @type matchings: Array de Calle
        @param altura: Altura invalida de la calle
        @type altura: Integer
        '''
        self.calle = calle
        self.matchings = matchings
        self.altura = altura

    def __str__(self):
        '''
        Devuelve un mensaje de error con el nombre de la calle
        @return: Mensaje de error
        @rtype: String
        '''
        return u'La calle {0} no existe a la altura {1}'.format(self.calle, self.altura)

    def getCalle(self):
        '''
        Devuelve el nombre de la calle
        @return: Nombre de la calle
        @rtype:  String
        '''
        return self.calle

    def getMatchings(self):
        '''
        Devuelve el array de matchings para la calle
        @return: Instancias de Calle que matchean 'calle'
        @rtype: Array de Calle
        '''
        return self.matchings

    def getAltura(self):
        '''
        Devuelve la altura invalida de la calle
        @return: Altura
        @rtype: Integer
        '''
        return self.altura

    def getErrorMessage(self):
        '''
        Devuelve un mensaje de error mas descriptivo y amigable
        @return: Mensaje de error
        @rtype: String
        '''
        msg = 'La altura indicada no es v&aacute;lida para la calle ingresada. A continuaci&oacute;n se muestran algunas opciones v&aacute;lidas halladas:<ul>'
        for calle in self.matchings:
            tramos = calle.getTramos()
            for tramo in tramos:
                msg += '<li>' + calle.nombre + ' ' + tramo[0] + '-' + tramo[1] + '</li>'
        msg += '</ul>'
        return msg


class ErrorCalleSinAlturas(Exception):
    '''
    Excepcion para calle sin alturas.
    '''
    calle = ""

    def __init__(self, calle):
        '''
        @param calle: Nombre oficial de la calle
        @type calle: String
        '''
        self.calle = calle

    def __str__(self):
        '''
        Devuelve un mensaje de error con el nombre de la calle
        @return: Mensaje de error
        @rtype: String
        '''
        return "La calle '" + self.calle + "' no posee alturas oficiales. Utilice intersecciones para hallar direcciones sobre esta calle."

    def getNombreCalle(self):
        '''
        Devuelve el nombre de la calle
        @return: Nombre de la calle
        @rtype:  String
        '''
        return self.calle

    def getErrorMessage(self):
        '''
        Devuelve un mensaje de error mas descriptivo y amigable
        @return: Mensaje de error
        @rtype: String
        '''
        msg = 'La calle ' + self.calle + ' no posee alturas oficiales. Utilice intersecciones para hallar direcciones v&aacute;lidas sobre esta calle o escriba S/N en lugar de la altura. Tenga en cuenta que si utiliza S/N no podr&aacute; geocodificar esta direcci&oacute;n.'
        return msg


class ErrorCruceInexistente(Exception):
    '''
    Excepcion para calles que no se cruzan.
    '''
    calle1 = ""
    matchingsCalle1 = []
    calle2 = ""
    matchingsCalle2 = []

    def __init__(self, calle1, matchingsCalle1, calle2, matchingsCalle2):
        '''
        @param calle1: Nombre oficial de la primera calle
        @type calle1:  String
        @param matchingsCalle1: Array de instancias de Calle que matchean el string 'calle1'
        @type matchingsCalle1: Array de calle
        @param calle2: Nombre oficial de la segunda calle
        @type calle2:  String
        @param matchingsCalle2: Array de instancias de Calle que matchean el string 'calle2'
        @type matchingsCalle2: Array de calle
        '''
        self.calle1 = calle1
        self.matchingsCalle1 = matchingsCalle1
        self.calle2 = calle2
        self.matchingsCalle2 = matchingsCalle2

    def __str__(self):
        '''
        Devuelve un mensaje de error con el nombre de la calle
        @return: Mensaje de error
        @rtype: String
        '''
        return "Cruce inexistente: " + self.calle1 + " y " + self.calle2

    def getCalle1(self):
        '''
        Devuelve el nombre de la calle
        @return: Nombre de la primera calle
        @rtype: String
        '''
        return self.calle1

    def getCalle2(self):
        '''
        Devuelve el nombre de la calle
        @return: Nombre de la segunda calle
        @rtype: String
        '''
        return self.calle2

    def getMatchingsCalle1(self):
        '''
        Devuelve el array de matchings para la primera calle
        @return: Instancias de Calle que matchean 'calle1'
        @rtype: Array de calle
        '''
        return self.matchingsCalle1

    def getMatchingsCalle2(self):
        '''
        Devuelve el array de matchings para la primera calle
        @return: Instancias de Calle que matchean 'calle2'
        @rtype: Array de calle
        '''
        return self.matchingsCalle2

    def getErrorMessage(self):
        '''
        Devuelve un mensaje de error mas descriptivo y amigable
        @return: Mensaje de error
        @rtype: String
        '''
        msg = 'El cruce de calles indicado no existe. A continuaci&oacute;n se muestran algunas calles que coinciden con su b&uacute;squeda.'
        msg += '<br/>Algunas calles halladas que coinciden con la 1ra calle ingresada son:<ul>'
        for calle in self.matchingsCalle1:
            msg += '<li>' + calle.nombre + '</li>'
        msg += '</ul>'
        msg += 'Algunas calles halladas que coinciden con la 2da calle ingresada son:<ul>'
        for calle in self.matchingsCalle2:
            msg += '<li>' + calle.nombre + '</li>'
        msg += '</ul>'
        return msg


class ErrorTextoSinDireccion(Exception):
    '''
    Excepción para textos sin direcciones.
    '''
    def __init__(self, *args):
        '''
        @param texto: texto de búsqueda de dirección
        @type calle1:  String
        '''
        self.texto = args[0]
        self.message = u'No se encontró dirección: "{0}"'.format(self.texto)

    def __unicode__(self):
        '''
        Devuelve un mensaje de error con el texto ingresado
        @return: Mensaje de error
        @rtype: String
        '''
        return self.message

    def __str__(self):
        '''
        Devuelve un mensaje de error con el nombre de la calle
        @return: Mensaje de error
        @rtype: String
        '''
        msg = unicodedata.normalize('NFKD', self.message).encode('ascii', 'ignore')
        return str(msg)
