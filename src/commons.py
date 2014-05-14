# coding: UTF-8
'''
Created on May 12, 2014

@author: hernan
'''
import re, unicodedata


NO_MATCH = 0
MATCH = 1
MATCH_PERMUTADO = 2
MATCH_EXACTO = 3

def matcheaTexto(txt1, txt2):
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
        txt1 = normalizarTexto(txt1)
        txt2 = normalizarTexto(txt2)

        if txt1 == txt2:
            return MATCH_EXACTO

        words1 = txt1.split(' ')
        words2 = txt2.split(' ')
        if (len(words1) == len(words2)):
            intersec = set(words1) & set(words2)
            if (len(words1) == len(intersec)):
                return MATCH_PERMUTADO


        regexps1 = map(lambda x: re.compile(r"^%s| %s" % (re.escape(x), re.escape(x))), txt1.split(' '))
        for regexp in regexps1:
            if regexp.search(txt2) == None:
                return NO_MATCH
        
        return MATCH
        
    except Exception, e:
        raise e
    
# normaliza un string quitándole acentos y caracteres especiales
def normalizarTexto(texto, separador=' ', lower=True):
    texto = texto.lower() if lower else texto.upper()
    texto = unicode(texto)
    texto = ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')) # reemplazamos ñ y acentos por n y sin acentos
    texto = re.sub(r'[^a-zA-Z0-9 ]', ' ', texto) # reemplazamos caracteres especiales por espacios
    texto = texto.strip() # stripeo
    texto = re.sub(r'\s+', separador, texto) # reemplazamos cadenas de espacios por un espacio
    
    return texto
