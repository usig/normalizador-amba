# coding: UTF-8
'''
Created on May 12, 2014

@author: hernan
'''
from __future__ import absolute_import
import re
import unicodedata

from usig_normalizador_amba.settings import NO_MATCH, MATCH, MATCH_INCLUIDO, MATCH_PERMUTADO, MATCH_EXACTO


def matcheaTexto(txt1, txt2, normalizar=True):
    '''
    Verifica si las palabras de txt1 estan contenidas en txt2
    @param txt1: texto a buscar
    @type txt1: unicode
    @param txt2: texto en donde buscar
    @type txt2: unicode
    @return: Indica si las palabras en txt1 estan en txt2
    @rtype: Int
    '''
    try:
        if normalizar:
            txt1 = normalizarTexto(txt1)
            txt2 = normalizarTexto(txt2)

        if txt1 == txt2:
            return MATCH_EXACTO

        words1 = set(txt1.split(' '))
        words2 = set(txt2.split(' '))
        if (words1 == words2):
            return MATCH_PERMUTADO

        if (words1 == words1 & words2):
            return MATCH_INCLUIDO

        regexps1 = map(lambda x: re.compile(ur'^{0}| {0}'.format(re.escape(x))), words1)
        for regexp in regexps1:
            if regexp.search(txt2) is None:
                return NO_MATCH

        return MATCH

    except Exception, e:
        raise e


# normaliza un string quitándole acentos y caracteres especiales
def normalizarTexto(texto, separador=' ', lower=True):
    texto = texto.lower() if lower else texto.upper()
    texto = unicode(texto)
    texto = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))  # reemplazamos ñ y acentos por n y sin acentos
    texto = re.sub(r'[^a-zA-Z0-9 ]', ' ', texto)  # reemplazamos caracteres especiales por espacios
    texto = texto.strip()  # stripeo
    texto = re.sub(r'\s+', separador, texto)  # reemplazamos cadenas de espacios por un espacio

    return texto
