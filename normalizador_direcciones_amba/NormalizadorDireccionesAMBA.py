# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
'''
import urllib2, re
import simplejson as json

from NormalizadorDirecciones import NormalizadorDirecciones
from settings import CALLEJERO_AMBA_SERVER
from Partido import *
from commons import *
from Errors import *

class NormalizadorDireccionesAMBA:
    server = CALLEJERO_AMBA_SERVER
    
    def __init__(self, include_list=[], exclude_list=[]):
        self.normalizadores = []
        try:
            data = urllib2.urlopen(self.server+'partidos').read()
            partidos_json = json.loads(data, 'utf8')
            
            for p in partidos_json:
                if p[1] not in exclude_list and (len(include_list) == 0 or p[1] in include_list):
                    partido = Partido(p[1], p[2], p[3], p[0])
                    nd = NormalizadorDirecciones(partido)
                    self.normalizadores.append(nd)
            
        except urllib2.HTTPError, e:
            e.detalle = u'Se produjo un error al intentar cargar la información de partidos.'
            raise e
    
    def recargarCallejeros(self):
        try:
            for nd in self.normalizadores:
                nd.recargarCallejero()
        except Exception, e:
            raise e
    
    def normalizar(self, direccion, maxOptions = 10):
        res = []
        re_partido = re.match(r'(.*),(.+)', direccion)

        if re_partido:
            try:
                res = self.normalizarPorPartido(re_partido.group(1), re_partido.group(2), maxOptions)
            except Exception, e:
                pass

        if len(res) == 0:
            try:
                res = self.normalizarPorPartido(direccion, maxOptions = maxOptions)
            except Exception, e:
                pass
                
#         for r in res:
#             print r.toString()

        if len(res):
            return res
        else:
            raise e

    def normalizarPorPartido(self, direccion, partido='', maxOptions = 10):
        res = [[],[],[],[]]
        for nd in self.normalizadores:
            try:
                if partido == '':
                    res[2] += nd.normalizar(direccion, maxOptions)
                else:
                    m = matcheaTexto(partido, nd.partido.keywords)
                    if m:
                        result = nd.normalizar(direccion,maxOptions)
                        if m == MATCH_EXACTO:
                            res[0] += result
                        elif m == MATCH_PERMUTADO:
                            res[1] += result
                        elif m == MATCH_INCLUIDO:
                            res[2] += result
                        elif m == MATCH:
                            res[3] += result
            except Exception, e:
                pass

        if len(res[0]+res[1]+res[2]+res[3]):
            res = (res[0]+res[1]+res[2]+res[3])
            if partido != '':
                res = [r for r in res if (matcheaTexto(partido, r.partido.nombre) or matcheaTexto(partido, r.localidad))]
            return res[:maxOptions]
        else:
            raise e

    def normalizarCalleYCalle(self, calle1='', calle2='', partido='', maxOptions = 10):
        res = [[],[],[],[]]
        
        if calle1 == '' or calle2 == '':
            raise Exception('Debe ingresar la calle y el cruce.')
        
        for nd in self.normalizadores:
            try:
                if partido == '':
                    res[2] += nd.normalizarCalleYCalle(calle1, calle2, maxOptions)
                else:
                    m = matcheaTexto(partido, nd.partido.keywords)
                    if m:
                        result = nd.normalizarCalleYCalle(calle1, calle2, maxOptions)
                        if m == MATCH_EXACTO:
                            res[0] += result
                        elif m == MATCH_PERMUTADO:
                            res[1] += result
                        elif m == MATCH_INCLUIDO:
                            res[2] += result
                        elif m == MATCH:
                            res[3] += result
            except Exception, e:
                pass

        if len(res[0]+res[1]+res[2]+res[3]):
            return (res[0]+res[1]+res[2]+res[3])[:maxOptions]
        else:
            raise e
    
    def buscarCodigo(self, codigo):
        for nd in self.normalizadores:
            res = nd.c.buscarCodigo(codigo)
            if res:
                return res
        return None
