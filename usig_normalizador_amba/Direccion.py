# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
'''
from __future__ import absolute_import
import re

from usig_normalizador_amba.settings import CALLE_ALTURA, CALLE_Y_CALLE, INVALIDO
from usig_normalizador_amba.Calle import Calle


class Direccion:
    '''
    @ivar calle: Calle de la direccion
    @type calle: Calle
    @ivar altura: Altura de la calle
    @type altura: Integer
    @ivar cruce: Calle con la que se cruza
    @type cruce: Calle
    @ivar tipo:  tipo de la calle
    @type tipo: {CALLE_ALTURA = 0, CALLE_Y_CALLE = 1}
    @ivar smp: Seccion-Manzana-Parcela
    @type smp: String
    @ivar coordenadas: Geocodificacion
    @type coordenadas: Punto
    @ivar partido: Partido de la direccion
    @type partido: Partido
    '''
    calle = None
    altura = 0
    cruce = None
    tipo = INVALIDO
    coordenadas = None
    partido = None
    localidad = ''

    def __init__(self, calle, altura=0, cruce=None):
        '''
        @ivar calle: Calle de la direccion
        @type calle: Calle
        @ivar altura: Altura de la calle
        @type altura: Integer
        @ivar cruce: Calle con la que se cruza
        @type cruce: Calle
        '''
        try:
            if(isinstance(calle, Calle)):
                self.calle = calle
                self.partido = calle.partido
                self.localidad = calle.localidad
            else:
                raise TypeError('calle must be a Calle object.')

            self.altura = int(altura)

            if (cruce is None or isinstance(cruce, Calle)):
                self.cruce = cruce
            else:
                raise TypeError('cruce must be a Calle object.')

            if self.altura > 0:
                self.tipo = CALLE_ALTURA
            elif cruce is not None:
                self.tipo = CALLE_Y_CALLE
            else:
                self.tipo = INVALIDO

        except Exception, e:
            raise e

    def __str__(self):
        return self.__unicode__().encode('utf8', 'ignore')

    def __unicode__(self):
        retval = u'''-- Dirección
    calle = {0}
    altura = {1}
    cruce = {2}
    coordenadas = {3}
    partido = {4}
    localidad = {5}'''
        return retval.format(self.calle.nombre,
                             self.altura,
                             self.cruce.nombre if self.cruce is not None else '',
                             self.coordenadas,
                             self.partido.nombre,
                             self.localidad)

    def toString(self):
        '''
        Devuelve un string con la direccion escrita correctamente para mostrar
        @return: Direccion como texto
        @rtype: String
        '''
        if (self.tipo == CALLE_ALTURA):
            if(self.altura > 0):
                altura = self.altura
            else:
                altura = 'S/N'
            retval = u'{0} {1}, {2}'.format(self.calle.nombre, altura, self.partido.nombre)
        elif (self.tipo == CALLE_Y_CALLE):
            if(re.match('(?i)(I|Hi|HI)', self.cruce.nombre) is not None):
                separador = 'e'
            else:
                separador = 'y'
            retval = u'{0} {1} {2}, {3}'.format(self.calle.nombre, separador, self.cruce.nombre, self.partido.nombre)
        else:
            retval = ''

        return retval
