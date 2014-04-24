# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
'''
import urllib2
import simplejson as json

from NormalizadorDirecciones import NormalizadorDirecciones
from settings import CALLEJERO_GBA_SERVER
from Partido import *

class NormalizadorDireccionesGBA:
    server = CALLEJERO_GBA_SERVER
    normalizadores = []
    
    def __init__(self, include_list=[], exclude_list=[]):
        try:
            data = urllib2.urlopen(self.server).read()
            partidos_json = json.loads(data, "utf8")
            
            for p in partidos_json:
                if p[1] not in exclude_list and (len(include_list) == 0 or p[1] in include_list):
                    partido = Partido(p[1], p[2], p[3], p[0])
                    nd = NormalizadorDirecciones(partido)
                    self.normalizadores.append(nd)
            
        except urllib2.HTTPError, e:
            e.detalle = 'Se produjo un error al intentar cargar la información de partidos.'
            raise e
    
    def normalizar(self, direccion):
        res = []
        for nd in self.normalizadores:
            try:
                res += nd.normalizar(direccion)
            except Exception, e:
                print e
                pass
        return res
