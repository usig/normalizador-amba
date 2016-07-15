# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
'''
from __future__ import absolute_import

from usig_normalizador_amba.Partido import Partido


class Calle:
    '''
    @ivar codigo: Codigo de calle
    @type codigo: Integer
    @ivar nombre: Nombre oficial de la calle
    @type nombre: Unicode
    @ivar alturas: [optional] Array conteniendo los rangos de altura validos para esta calle
    @type alturas: String [Array]
    @ivar cruces:  [optional] Array conteniendo los id de las calles que se cruzan con esta
    @type cruces: Integer [Array]
    @ivar partido: Partido de la direccion
    @type partido: Partido
    '''
    codigo = 0
    nombre = ""
    alturas = []
    cruces = []
    partido = None
    localidad = ''

    def __init__(self, codigo, nombre, alturas=[], cruces=[], partido=None, localidad=''):
        '''
        @param codigo: Codigo de calle
        @type codigo: Integer
        @param nom: Nombre oficial de la calle
        @type nom: Unicode
        @param alturas: [optional] Array conteniendo los rangos de altura validos para esta calle
        @type alturas: String [Array]
        @param cruces:  [optional] Array conteniendo los id de las calles que se cruzan con esta
        @type cruces: Integer [Array]
        @param partido: Partido de la calle
        @type partido: Partido
        '''
        try:
            self.codigo = int(codigo)
            self.nombre = unicode(nombre)
            if isinstance(alturas, list):
                self.alturas = alturas
            else:
                raise TypeError('alturas must be a list.')
            if isinstance(cruces, list):
                self.cruces = cruces
            else:
                raise TypeError('alturas must be a list.')
            if isinstance(partido, Partido):
                self.partido = partido
            else:
                raise TypeError('partido must be a Partido object.')
            self.localidad = unicode(localidad)

        except Exception, e:
            raise e

    def __str__(self):
        return self.__unicode__().encode('utf8', 'ignore')

    def __unicode__(self):
        retval = u'''-- Calle
    codigo = {0}
    nombre = {1}
    alturas = {2}
    cruces = {3}
    partido = {4}
    localidad = {5}'''
        return retval.format(self.codigo,
                             self.nombre,
                             self.alturas.__str__(),
                             self.cruces.__str__(),
                             self.partido.nombre,
                             self.localidad)

    def alturaValida(self, altura):
        '''
        Verifica si la altura es valida para esta calle.
        @param altura: Altura a validar
        @type altura: Integer
        @return: True si la altura es valida para esta calle
        @rtype: Boolean
        '''
        retval = False

        for rango in self.alturas:
            if ((int(rango[0]) <= altura) and (altura <= int(rango[1]))):
                retval = True
                break
        return retval

    def seCruzaCon(self, calle):
        '''
        Verifica si la calle (instancia de la clase usig.Calle) recibida como parametro se cruza con esta
        @param calle: Calle a verificar si se intersecta con esta
        @type calle: Calle
        @return: True en caso de que exista el cruce correspondiente
        @rtype: Boolean
        '''
        return (calle.codigo in self.cruces)

    def toString(self):
        '''
        Devuelve un string con la calle escrita correctamente para mostrar
        @return: Calle como texto
        @rtype: String
        '''
        return u'{0}, {1}, {2}'.format(self.nombre, self.localidad, self.partido.nombre)
