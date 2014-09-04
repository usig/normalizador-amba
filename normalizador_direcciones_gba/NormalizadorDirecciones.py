# coding: UTF-8
'''
Created on Jun 17, 2014

@author: hernan
'''

import re, copy

from StringDireccion import StringDireccion
from Callejero import Callejero
from Errors import *
from Direccion import Direccion
from settings import *
from commons import *

class NormalizadorDirecciones:
    '''
    NormalizadorDirecciones
    Esta clase implementa integramente un normalizador de direcciones que utiliza un Callejero de USIG para transformar un string en una direccion normalizada.
    @ivar c: El callejero del partido
    @type c: Callejero
    @ivar partido: El partido del callejero que se quiere instanciar
    @type partido: Partido
    '''
    c = None
    partido = None

    def __init__(self, partido):
        '''
        @param partido: Indica el partido del callejero
        @type partido: Partido
        '''
        try:
            if partido == None:
                raise Exception(u'Debe indicar el partido.')
            self.c = Callejero(partido)
            self.partido = partido
        except Exception, e:
            raise e

    def recargarCallejero(self):
        try:
            self.c.cargarCallejero()
        except Exception, e:
            raise e

    def normalizar(self, direccion, maxOptions = 10):
        ''' 
        @param direccion: La cadena a ser transformada en direccion
        @type direccion: Unicode
        @param maxOptions: Maximo numero de opciones a retornar. Por defecto es 10.
        @type maxOptions: Integer
        @return: Las opciones halladas que se corresponden con direccion
        @rtype: Array de Direccion
        '''
        res = []
        error = None
        
        if direccion == '':
            raise ErrorCalleInexistente(u'')
        
        if type(direccion) != unicode:
            direccion = unicode(direccion, encoding='utf-8', errors='ignore')
        strDir = StringDireccion(direccion)
        
        for candidato in strDir.candidatos:
            if candidato['tipo'] == CALLE:
                res += self.buscarCalle(candidato['calle'], maxOptions)
            elif candidato['tipo'] == CALLE_Y_CALLE:
                try:
                    res += self.normalizarCalleYCalle(candidato['calle'],candidato['cruce'],maxOptions)
                except Exception, error:
                    pass

        # TODO: Si no hay match eliminar de inCalle e inCruce keywords (AV, AVENIDA, PJS, PASAJE, etc) y volver a buscar. 
        # pasar removeWords a commons y usarlo con [(AV, AVENIDA, PJS, PASAJE, etc)]
#        if not res:
#            dirFiltrada = self._filtrarDireccion(strDir.strNormalizado)
#            if strDir.strNormalizado != dirFiltrada:
#                try:
#                    res = self.normalizar(dirFiltrada, maxOptions)
#                except:
#                    pass

        if isinstance(res, list):
            if res:
                return res
            else:
                if error:
                    raise error
                else:
                    raise ErrorCalleInexistente(strDir.strOriginal)
        else:
            return res

    def buscarCalle(self, inCalle, maxOptions):
        res = self.c.buscarCalle(inCalle, maxOptions)
        return res
    
    def normalizarCalleYCalle(self, inCalle, inCruce, maxOptions=10):
        '''
        Normaliza una direccion de tipo calle-calle
        @param inCalle: Calle a ser normalizada
        @type inCalle: String
        @param inCruce: Cruce a ser normalizado
        @type inCruce: String
        @param maxOptions: Maximo numero de opciones a retornar. Por defecto es 10.
        @type maxOptions: Integer
        @return: Las opciones halladas que se corresponden con dir
        @rtype: Array de Direccion 
        '''
        calles = self.c.buscarCalle(inCalle)
        cruces = self.c.buscarCalle(inCruce)

        # Armo una lista (matches) tabu para evitar agregar 2 veces una interseccion
        matches = []
        opts = []
        for calle in calles:
            for cruce in cruces:
                if (calle.codigo != cruce.codigo) and (not self._matchCode(calle, cruce) in matches) and (calle.seCruzaCon(cruce)) and (cruce.seCruzaCon(calle)):
                    opts.append(Direccion(calle, 0, cruce))
                    matches.append(self._matchCode(calle, cruce))
                    if(len(opts) >= maxOptions):
                        break
            if(len(opts) >= maxOptions):
                break

        if(len(opts) == 0 and len(calles) > 0 and len(cruces) > 0):
            raise ErrorCruceInexistente(inCalle, calles, inCruce, cruces)
        return opts

    def _matchCode(self, calle1, calle2):
        return min(calle1.codigo, calle2.codigo)+max(calle1.codigo, calle2.codigo)
