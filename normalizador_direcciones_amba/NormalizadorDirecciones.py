# coding: UTF-8
'''
Created on Jun 17, 2014

@author: hernan
'''

import re, copy

from StringDireccion import StringDireccion
from Callejero import Callejero
from Calle import Calle
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
            elif candidato['tipo'] == CALLE_ALTURA:
                try:
                    res += self.normalizarCalleAltura(candidato['calle'],candidato['altura'],maxOptions)
                except Exception, error:
                    pass
            elif candidato['tipo'] == CALLE_Y_CALLE:
                try:
                    res += self.normalizarCalleYCalle(candidato['calle'],candidato['cruce'],maxOptions)
                except Exception, error:
                    pass

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

    def normalizarCalleAltura(self, inCalle, inAltura, maxOptions=10):
        '''
        Normaliza una direccion de tipo Calle-altura
        @param inCalle: La calle a ser normalizada
        @type inCalle: String
        @param inAltura: La altura de la calle a ser normalizada
        @type inCalle: int
        @param maxOptions: Maximo numero de opciones a retornar.
        @type maxOptions: Integer
        @return: Las opciones halladas
        @rtype: Array de Direcciones
        '''
        opts = []
        calles = self.c.buscarCalle(inCalle)
        for calle in calles:
            if calle.alturaValida(inAltura):
                d = Direccion(calle, inAltura)
                opts.append(d)

        if(len(opts) == 0 and len(calles) > 0):
            raise ErrorCalleInexistenteAEsaAltura(inCalle, calles, inAltura)

        return opts
    
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
        
        opts = []
        for calle in calles:
            for idCruce in calle.cruces:
                cruce = self.c.buscarCodigo(idCruce)
                if matcheaTexto(inCruce, cruce[2]):
                    objCruce = Calle(cruce[0], cruce[1], [], cruce[4], calle.partido, cruce[5])
                    opts.append(Direccion(calle, 0, objCruce))
                    if(len(opts) >= maxOptions):
                        break
            if(len(opts) >= maxOptions):
                break
        
        
        if(len(opts) == 0 and len(calles) > 0):
            raise ErrorCruceInexistente(inCalle, [], inCruce, [])
        return opts

    def _matchCode(self, calle1, calle2):
        return min(calle1.codigo, calle2.codigo)+max(calle1.codigo, calle2.codigo)
