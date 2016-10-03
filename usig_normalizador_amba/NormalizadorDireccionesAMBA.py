# coding: UTF-8
'''
Created on Apr 16, 2014
Modified on Mar 28, 2016

@author: hernan
'''
from __future__ import absolute_import
import urllib2
import re
import json

from usig_normalizador_amba.NormalizadorDirecciones import NormalizadorDirecciones
from usig_normalizador_amba.settings import default_settings
from usig_normalizador_amba.settings import MATCH, MATCH_INCLUIDO, MATCH_PERMUTADO, MATCH_EXACTO
from usig_normalizador_amba.Partido import Partido
from usig_normalizador_amba.commons import normalizarTexto, matcheaTexto
from usig_normalizador_amba.Errors import ErrorTextoSinDireccion


class NormalizadorDireccionesAMBA:

    def _getPartidosAMBA(self):
        try:
            response = urllib2.urlopen(self.config['callejero_amba_server'] + 'partidos').read()
            partidos = json.loads(response, 'utf8')
            return partidos
        except urllib2.HTTPError, e:
            e.detalle = u'Se produjo un error al intentar cargar la información de partidos.'
            raise e

    def __init__(self, include_list=[], exclude_list=[], config={}):
        # default config
        self.config = default_settings.copy()
        # custom config
        self.config.update(config)

        self.normalizadores = []
        try:
            partidos = self._getPartidosAMBA()
            partidos = [[1, u'caba', u'CABA', u'CABA Ciudad Autónoma de Buenos Aires']] + partidos

            for p in partidos:
                if p[1] not in exclude_list and (len(include_list) == 0 or p[1] in include_list):
                    partido = Partido(p[1], p[2], p[3], p[0])
                    nd = NormalizadorDirecciones(partido, self.config)
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

    def normalizar(self, direccion, maxOptions=10):
        res = []
        re_partido = re.match(r'(.*),(.+)', direccion)

        if re_partido:
            try:
                res = self.normalizarPorPartido(re_partido.group(1), re_partido.group(2), maxOptions)
            except Exception, e:
                pass

        if len(res) == 0:
            try:
                res = self.normalizarPorPartido(direccion, maxOptions=maxOptions)
            except Exception, e:
                pass

        if len(res):
            return res
        else:
            raise e

    def normalizarPorPartido(self, direccion, partido='', maxOptions=10):
        res = [[], [], [], []]
        for nd in self.normalizadores:
            try:
                if partido == '':
                    res[2] += nd.normalizar(direccion, maxOptions)
                else:
                    m = matcheaTexto(partido, nd.partido.keywords)
                    if m:
                        result = nd.normalizar(direccion, maxOptions)
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

        if len(res[0] + res[1] + res[2] + res[3]):
            res = (res[0] + res[1] + res[2] + res[3])
            if partido != '':
                res = [r for r in res if (matcheaTexto(partido, r.partido.nombre) or matcheaTexto(partido, r.localidad))]
            return res[:maxOptions]
        else:
            raise e

    def normalizarCalleYCalle(self, calle1='', calle2='', partido='', maxOptions=10):
        res = [[], [], [], []]

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

        if len(res[0] + res[1] + res[2] + res[3]):
            return (res[0] + res[1] + res[2] + res[3])[:maxOptions]
        else:
            raise e

    def buscarCodigo(self, codigo):
        for nd in self.normalizadores:
            res = nd.c.buscarCodigo(codigo)
            if res:
                return res
        return None

    def _buscarPartidoLocalidad(self, texto, partido, localidad):
        retval = False
        palabras = re.split('\s', normalizarTexto(texto))
        cant_palabras = len(palabras)
        for i in range(cant_palabras):
            texto_cortado = ' '.join(palabras[:i + 1])
            if matcheaTexto(texto_cortado, partido) or matcheaTexto(texto_cortado, localidad):
                retval = True
            else:
                break
        return retval

    def buscarDireccion(self, texto):
        res = []
        for nd in self.normalizadores:
            try:
                res.append(nd.buscarDireccion(texto))
            except Exception:
                pass

        retval = []
        for partido in res:
            new_partido = []
            for match in partido:
                new_match = {'posicion': match['posicion'], 'texto': match['texto'], 'direcciones': []}
                for direccion in match['direcciones']:
                    posicion = match['posicion'] + len(match['texto'])
                    partido_direccion = u'Partido de {0}'.format(direccion.partido.nombre)
                    localidad_direccion = u'Localidad de {0}'.format(direccion.localidad)
                    if self._buscarPartidoLocalidad(texto[posicion:], partido_direccion, localidad_direccion):
                        new_match['direcciones'].append(direccion)
                if new_match['direcciones']:
                    new_partido.append(new_match)
            if new_partido:
                retval.append(new_partido)

        if len(retval):
            return retval
        elif len(res):
            return res
        else:
            raise ErrorTextoSinDireccion(texto)
