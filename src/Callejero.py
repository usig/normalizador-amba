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

    def cargarCallejero(self):
        '''
        Carga las calles en el atributo data sin los cruces 
        '''
        try:
            data = urllib2.urlopen(self.server).read()
            self.data = json.loads(data, "utf8")

            for i in range(len(self.data)):
                self.data[i][2] = normalizarTexto(self.data[i][1], separador=' ', lower=False)
                self.data[i][2] = self.agregarSinonimos(self.data[i][2])
            
#                if isinstance(self.data[i][2], str):
#                    self.data[i][2] = unicode(self.data[i][2])
#                self.data[i][2] = ''.join((c for c in unicodedata.normalize('NFD', self.data[i][2]) if unicodedata.category(c) != 'Mn'))

        except urllib2.HTTPError, e:
            e.detalle = 'Se produjo un error al intentar cargar la información de calles.'
            raise e
        except Exception, e:
            print e, self.data[i][2], i

    def agregarSinonimos(self, texto):
        diccionario = [
                       [['DOCTOR','DR'],['DOCTOR','DR']],
                       [['AVENIDA','AV','AVD','AVDA'],['AVENIDA','AVDA']],
                       [['PASAJE','PJE'],['PASAJE','PJE']],
                       [['GENERAL','GRAL'],['GENERAL','GRAL']],
                       [['PRES'],['PRESIDENTE']],
                       [['CORONEL','CNEL'],['CORONEL','CNEL']],
                       [['DIAG'],['DIAGONAL']],
                       [['2','DOS'],['2','DOS']],
                       [['3','TRES'],['3','TRES']],
                       [['11','ONCE'],['11','ONCE']],
       ]
        
        words = texto.split(' ')

        for sinonimos in diccionario:
            for sinonimo in sinonimos[0]:
                if sinonimo in words:
                    i = words.index(sinonimo)
                    words.pop(i)
                    words.extend(sinonimos[1])
                    break
        return ' '.join(words)

    def buscarCodigo(self, codigo):
        '''
        Busca calle por codigo y devuelve una instancia de Calle
        @param codigo: Codigo de calle
        @type calle: Int
        @return: instancias de Calle
        @rtype: Calle
        '''
        for calle in self.data:
            if calle[0] == codigo:
                return calle
        return None
    
    def buscarCalle(self, calle, limit=0):
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
            return self.minicache[1] if limit == 0 else self.minicache[1][:limit]
        
        res = [[],[],[],[]]
        calleNorm1 = normalizarTexto(calle, separador=' ', lower=False)
        words1 = set(calleNorm1.split(' '))
        regexps1 = map(lambda x: re.compile(ur'^{0}| {1}'.format(re.escape(x), re.escape(x))), words1)
## No utilizo commons.matcheaTexto por cuestiones de optimizacion
## No podo la busqueda en limit para buscar las mejores soluciones
        for data in self.data:
            if calle == data[1]: # Match exacto con el nombre
                res[0].append(Calle(data[0], data[1], data[3], data[4], self.partido))
            else: # Match permutado con el nombre
                calleNorm2 = normalizarTexto(data[1], separador=' ', lower=False)
                words2 = set(calleNorm2.split(' '))
                if (words1 == words2):
                    res[1].append(Calle(data[0], data[1], data[3], data[4], self.partido))
                elif (words1 == words1 & words2): # Match incluido con el nombre
                        res[2].append(Calle(data[0], data[1], data[3], data[4], self.partido))
                else: # Match con las keywords de la calle
                    match = True
                    for regexp in regexps1:
                        if regexp.search(data[2]) == None:
                            match = False
                            break
                    if match:
                        res[3].append(Calle(data[0], data[1], data[3], data[4], self.partido))
        
        res = res[0]+res[1]+res[2]+res[3]
        self.minicache = [calle, res]

        return res if limit == 0 else res[:limit] 
#        return self._recortarRespuesta(res, limit)
    
#    def _recortarRespuesta(self, resCalles, limit):
#        if limit == 0:
#            return resCalles
#        else:
#            retval = [[],[],[],[]]
#            cant = limit
#            for i in range(len(retval)):
#                retval[i] = resCalles[i][:cant]
#                cant -= len(resCalles[i])
#                if cant < 0:
#                    cant = 0
#            return retval
                
#    matcheaCalle = buscarCalle
    
### DEPRECADO
#    def matcheaCalle(self, calle, limit=0):
#        '''
#        Busca calles cuyo nombre se corresponda con calle y devuelve un array con todas las instancias de Calle halladas
#        @param calle: String a matchear
#        @type calle: String
#        @param limit: Maximo numero de respuestas a devolver. Cero es sin limite.
#        @type limit: Integer
#        @return: Array de instancias de Calle que matchearon calle
#        @rtype: Array de Calle 
#        '''
#        if self.minicache[0] == calle:
#            return self.minicache[1]
#        
#        opts = []
#        if isinstance(calle, str):
#            calle = unicode(calle)
#        input = ''.join((c for c in unicodedata.normalize('NFD', calle) if unicodedata.category(c) != 'Mn'))
#        input = input.upper()
#        words = input.split(' ')
#        print words
#        words = map(lambda x: re.compile(ur'^{0}| {0}'.format(re.escape(x))), words)
#        for data in self.data:
#            if(self.matchea(words, data)):
#                opts.append(Calle(data[0], data[1], data[3], data[4], self.partido))
#                if(limit != 0 and len(opts) >= int(limit)):
#                    break
#
#        self.minicache = [calle, opts]
#        return opts
#
### DEPRECADO        
#    def matchea(self, words, calle):
#        '''
#        Busca las palabra de la lista words en la keyword de la calle
#        @param words: palabras a buscar
#        @type words: List of Compiled Regular Expression
#        @param calle: calle
#        @type calle: List of String
#        @return: Indica si las palabras estan en las keywords de calle
#        @rtype: Boolean
#        '''
#        match = True
#        for word in words:
#            if word.search(calle[2]) == None:
#                match = False
#                break
#        return match
     
#class BusquedaCallejero():
#    '''
#    Resultado de la busqueda en el callejero
#    '''
#    resultado = [[],[],[],[]]
#    
#    def __init__(self):
#        pass
#    
#    def agregar(self,nivel,valor):
#        try:
#            self.resultado[nivel].append(valor)
#        except Exception, e:
#            raise e
#    
#    def aplanar(self):
#        return self.resultado[0]+self.resultado[1]+self.resultado[2]+self.resultado[3]
#
#    def recortar(self, limit=0):
#        if limit == 0:
#            return self.resultado
#        else:
#            retval = [[],[],[],[]]
#            cant = limit
#            for i in range(len(retval)):
#                retval[i] = resCalles[i][:cant]
#                cant -= len(resCalles[i])
#                if cant < 0:
#                    cant = 0
#            return retval

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