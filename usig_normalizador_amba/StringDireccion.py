# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
'''
from __future__ import absolute_import
import re

from usig_normalizador_amba.settings import CALLE, CALLE_ALTURA, CALLE_Y_CALLE
from usig_normalizador_amba.commons import normalizarTexto


class StringDireccion:
    '''
    Parsea un string que presuntamente representa una direccion; arma una lista de candidatos a direcciones las tipifica y las separa en tokens.
    Luego de instanciada la propiedad "tipo" puede asumir los siguientes valores:
     - CALLE
     - CALLE_ALTURA
     - CALLE_Y_CALLE
     - INVALIDO
    @ivar strOriginal: El texto a analizar
    @type strOriginal: Unicode
    @ivar candidatos: Lista de candidatos (tipo, calle, [altura|cruce])
    @type tipo: Array
    '''

    strOriginal = ''
    strNormalizado = ''
    candidatos = []

    def __init__(self, strInput):
        self.strOriginal = strInput
        self.strNormalizado = normalizarTexto(strInput, separador=' ', lower=False)
        self.buscarCandidatos()

    def buscarCandidatos(self):
        self.candidatos = []

        # case: CALLE_ALTURA
        res = re.match(ur'^(.+) ([0-9]+)$', self.strNormalizado)
        if res:
            self.candidatos.append({'tipo': CALLE_ALTURA, 'calle': res.group(1), 'altura': int(res.group(2))})

        # case: CALLE_Y_CALLE
        palabras = self.strNormalizado.split(' Y ')
        if(len(palabras) >= 2):
            for i in range(len(palabras) - 1):
                calle = ' Y '.join(palabras[0:i + 1])
                cruce = ' Y '.join(palabras[i + 1:])
                self.candidatos.append({'tipo': CALLE_Y_CALLE, 'calle': calle, 'cruce': cruce})

        palabras = self.strNormalizado.split(' E ')
        if(len(palabras) >= 2):
            for i in range(len(palabras) - 1):
                if re.match(r'^[I|Y|HI|HY].*', palabras[i + 1]):
                    calle = ' E '.join(palabras[0:i + 1])
                    cruce = ' E '.join(palabras[i + 1:])
                    self.candidatos.append({'tipo': CALLE_Y_CALLE, 'calle': calle, 'cruce': cruce})

        # case: CALLE
        self.candidatos.append({'tipo': CALLE, 'calle': self.strNormalizado})

    def __str__(self):
        return self.__unicode__().encode('utf8', 'ignore')

    def __unicode__(self):
        retval = u'''-- StringDireccion
    strOriginal = {0}
    candidatos = {1}'''
        return retval.format(self.strOriginal, self.candidatos)
