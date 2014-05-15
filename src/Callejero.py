# coding: UTF-8
'''
Created on Apr 21, 2014

@author: hernan
'''
 
import urllib2, urllib, re, unicodedata
import simplejson as json
from Calle import Calle
from bisect import bisect_left

from settings import *
from commons import *

class Callejero:
    '''
    @cvar server: URL del servidor de datos de calles. Tiene un valor por defecto.
    @type server: String 
    @cvar data: La base de datos del callejero [id_calle, nombre_calle, keywords, array_de_rango_de_alturas, array_de_cruces]
    @type data: Array
#    @cvar codigos: Array con los codigos de calle para la busqueda binaria [id_calle]
#    @type codigos: Array
    @ivar partido: Partido de la direccion
    @type partido: Partido
    '''
    server = ''
    data = []
#    codigos = []
    partido = None
    
    # Minicache [calle, opts]
    # calle: la calle ingresada por parametro a matcheaCalle
    # opts: el resultado que devuelve
    minicache = ['gslgimigawakaranaigslg',[]]
        
    def __init__(self, partido):
        '''
        Carga el callejero
        '''
        try:
            self.partido = partido
            self.server = CALLEJERO_GBA_SERVER + partido.codigo
            self.cargarCallejero()
#            self.cargarCruces()
#            self.codigos = [k[0] for k in self.data]
        except Exception, e:
            raise e
            
    def matcheaCalle(self, calle, limit=0):
        '''
        Busca calles cuyo nombre se corresponda con calle y devuelve un array con todas las instancias de Calle halladas
        @param calle: String a matchear
        @type calle: String
        @param limit: Maximo numero de respuestas a devolver. Cero es sin limite.
        @type limit: Integer
        @return: Array de instancias de Calle que matchearon calle
        @rtype: Array de Calle 
        '''
        if self.minicache[0] == calle:
            return self.minicache[1]
        
        opts = []
        if isinstance(calle, str):
            calle = unicode(calle)
        input = ''.join((c for c in unicodedata.normalize('NFD', calle) if unicodedata.category(c) != 'Mn'))
        input = input.upper()
        words = input.split(' ')
        words = map(lambda x: re.compile("^%s| %s" % (re.escape(x), re.escape(x))), words)
        for data in self.data:
            if(self.matchea(words, data)):
                opts.append(Calle(data[0], data[1], data[3], data[4], self.partido))
                if(limit != 0 and len(opts) >= int(limit)):
                    break

        self.minicache = [calle, opts]
        return opts
        
    def matchea(self, words, calle):
        '''
        Busca las palabra de la lista words en la keyword de la calle
        @param words: palabras a buscar
        @type words: List of Compiled Regular Expression
        @param calle: calle
        @type calle: List of String
        @return: Indica si las palabras estan en las keywords de calle
        @rtype: Boolean
        '''
        match = True
        for word in words:
            if word.search(calle[2]) == None:
                match = False
                break
        return match
     
    def cargarCallejero(self):
        '''
        Carga las calles en el atributo data sin los cruces 
        '''
        try:
            data = urllib2.urlopen(self.server).read()
            self.data = json.loads(data, "utf8")

            for i in range(len(self.data)):
                self.data[i][2] = normalizarTexto(self.data[i][1], separador=' ', lower=False)
                #self.agregarSinonimos
            
#                if isinstance(self.data[i][2], str):
#                    self.data[i][2] = unicode(self.data[i][2])
#                self.data[i][2] = ''.join((c for c in unicodedata.normalize('NFD', self.data[i][2]) if unicodedata.category(c) != 'Mn'))

        except urllib2.HTTPError, e:
            e.detalle = 'Se produjo un error al intentar cargar la información de calles.'
            raise e
#        except Exception, e:
#            print e, self.data[i][2], i
    
    def buscarCodigo(self, codigo):
        for calle in self.data:
            if calle[0] == codigo:
                return calle
        return None
        
        
#    def cargarCruces(self):
#        '''
#        Carga los cruces de calles en el atributo data 
#        '''
#        try:
#            params = urllib.urlencode({"full": "1", "cruces": "1" })
#            data = urllib2.urlopen(self.server, params).read()
#            cruces = json.loads(data, "latin-1")
#            self.mergeDatosCruces(cruces)
#        except urllib2.HTTPError, e:
#            e.detalle = 'Se produjo un error al intentar cargar la información de los cruces de calles.'
#            raise e
#
#    def mergeDatosCruces(self, cruces):
#        if(len(self.data) != len(cruces)):
#            raise urllib2.HTTPError
#        for i in range(len(cruces)):
#            self.data[i].append(cruces[i])
#    
#    def tieneTramosComoAv(self, calle):
#        ''' 
#        Determina si una calle tiene tramos como Av.
#        @attention: ATTENTI RAGAZZI
#        Esto funciona estrictamente porque la base de calles viene ordenada por codigo de calles y
#        la unica posibilidad de que una calle tenga tramos como av y calle simultaneamente es que
#        haya un par de registros consecutivos con el mismo codigo (uno para c/caso)
#        @param calle: Instancia de Calle
#        @type calle: Calle
#        @return: Retorna True en caso de que la calle tenga tramos como Av.
#        @rtype: Boolean
#        '''
#        retval = False
#        pos = bisect_left(self.codigos, calle.cod)
#        if(pos < len(self.codigos) and self.codigos[pos] == calle.cod):
#            retval = (self.codigos[pos-1] == calle.cod or self.codigos[pos+1] == calle.cod)
#        return retval