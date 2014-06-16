# coding: UTF-8
'''
Created on Apr 29, 2010

@author: hernan
@note: Version de documentacion hasta revision 1717
'''

import re, copy

from StringDireccion import StringDireccion
from Callejero import Callejero
from Errors import *
from Direccion import Direccion
from settings import *


class NormalizadorDirecciones:
    '''
    NormalizadorDirecciones
    Esta clase implementa integramente un normalizador de direcciones que utiliza el Callejero de USIG para transformar un string en una direccion normalizada.
    @ivar aceptarCallesSinAlturas: Indica al normalizador si debe permitir como altura S/N para las calles sin numero. Por defecto es False. Ej: de los italianos S/N
    @type aceptarCallesSinAlturas: Boolean  
    '''
    aceptarCallesSinAlturas = False 
    c = None
    maxPalabras = 8
    rExps =   [u'Á',u'É',u'Í',u'Ó',u'Ú',u'Ü']
    repChar = [u'A',u'E',u'I',u'O',u'U',u'U']
    regexps = {
        'cruceCalles': (r'\s+y\s+',re.I),
        'calleAltura': [re.compile(r"(\d+(\s+(\w|\d|\xc3\xa1|\xc3\xa9|\xc3\xad|\xc3\xb3|\xc3\xba|\xc3\xbc|\xc3\xb1|\xb1\xc3|\xbc\xc3|\xba\xc3|\xb3\xc3|\xad\xc3|\xa9\xc3|\xa1\xc3|'|`|,|\.)+){"+str(i)+"})",re.I|re.U) for i in range(maxPalabras)],
        'calle': [re.compile(r"(\w|\d|\xc3\xa1|\xc3\xa9|\xc3\xad|\xc3\xb3|\xc3\xba|\xc3\xbc|\xc3\xb1|\xb1\xc3|\xbc\xc3|\xba\xc3|\xb3\xc3|\xad\xc3|\xa9\xc3|\xa1\xc3|'|`|,|\.)+(\s+(\w|\d|\xc3\xa1|\xc3\xa9|\xc3\xad|\xc3\xb3|\xc3\xba|\xc3\xbc|\xc3\xb1|\xb1\xc3|\xbc\xc3|\xba\xc3|\xb3\xc3|\xad\xc3|\xa9\xc3|\xa1\xc3|'|`|,|\.)+){"+str(i-1)+"}",re.I|re.U) for i in range(maxPalabras)]}
    partido = None
    
    def __init__(self, partido, aceptarCallesSinAlturas = False):
        '''
        @param partido: Indica el partido del callejero
        @type partido: Partido
        @param aceptarCallesSinAlturas: Indica al normalizador si debe permitir como altura S/N para las calles sin numero. Por defecto es False. Ej: de los italianos S/N
        @type aceptarCallesSinAlturas: Boolean  
        '''
        self.aceptarCallesSinAlturas = aceptarCallesSinAlturas
        try:
            if partido == None:
                raise Exception('Debe indicar el partido.')
            self.c = Callejero(partido)
            self.partido = partido
        except Exception, e:
            raise e
        
    def normalizar(self, direccion, maxOptions = 10):
        ''' 
        @param direccion: La cadena a ser transformada en direccion
        @type direccion: String
        @param maxOptions: Maximo numero de opciones a retornar. Por defecto es 10.
        @type maxOptions: Integer
        @return: Las opciones halladas que se corresponden con dir
        @rtype: Array de Direccion
        '''
        
#        direccion = direccion.upper()
        if type(direccion) != unicode:
            direccion = unicode(direccion, 'utf-8')
        
        strDir = StringDireccion(direccion, self.aceptarCallesSinAlturas)
        res = []
        if strDir.tipo == CALLE:
            res = self.c.buscarCalle(strDir.strInput, maxOptions)
#        elif strDir.tipo == CALLE_ALTURA:
#            res = self.normalizarCalleAltura(strDir, maxOptions)
        elif strDir.tipo == CALLE_Y_CALLE:
            res = self.normalizarCalleYCalle(strDir, maxOptions)
#            if len(res) == 0:
#                strDir.setearCalleAltura()
#                res = self.normalizarCalleAltura(strDir, maxOptions)
        elif strDir.tipo == INVALIDO:
            res = []
        if isinstance(res, list):
            if(len(res) > 0):
                return res
            else:
                raise ErrorCalleInexistente(strDir)
        else:
            return res

#    def normalizarCalleAltura(self, strDir, maxOptions):
#        '''
#        Normaliza una direccion de tipo Calle-altura
#        @param strDir: La direccion a ser normalizada
#        @type strDir: StringDireccion
#        @param maxOptions: Maximo numero de opciones a retornar.
#        @type maxOptions: Integer
#        @return: Las opciones halladas que se corresponden con dir
#        @rtype: Array
#        '''
#        calles = self.c.buscarCalle(strDir.strCalles)
#        try:
#            opts = self.validarAlturas(strDir, calles, maxOptions)
#        except ErrorCalleSinAlturas, e:
#            raise e
#        if(len(opts) == 0 and len(calles) > 0):
#            strDir.quitarAvsCalle()
#            calles = self.c.buscarCalle(strDir.strCalles)
#            try:
#                opts = self.validarAlturas(strDir, calles, maxOptions)
#            except Exception,  e:
#                raise e
#            opts = self.filtrarCallesQueNoSonAv(opts)
#            if(len(opts) == 0):
#                raise ErrorCalleInexistenteAEsaAltura(strDir.strCalles, calles, strDir.strAltura)
#        elif(len(opts) == 0 and len(calles) == 0):
#            strDir.quitarPasajes()
#            calles = self.c.buscarCalle(strDir.strCalles)
#            try:
#                opts = self.validarAlturas(strDir, calles, maxOptions)
#            except Exception,  e:
#                raise e
#        return opts

#    def validarAlturas(self, strDir, calles, maxOptions):
#        '''
#        Verifica si la altura es valida para las calles matcheadas
#        @param strDir: La direccion a ser verificada
#        @type strDir: StringDireccion
#        @param calles: Calles que matchean con strDir
#        @type calles: Array de Calle
#        @param maxOptions: Maximo numero de opciones a retornar.
#        @type maxOptions: Integer
#        @return: Las Calles que matchean y que son validas a la altura especificada
#        @rtype: Array de Direccion
#        '''
#        retval = []
#        hayCalleSN = False
#        for i in range(len(calles)):
#            try:
#                if(calles[i].alturaValida(strDir.strAltura)):
#                    retval.append(Direccion(calles[i],strDir.strAltura))
#            except ErrorCalleSinAlturas:
#                if(self.aceptarCallesSinAlturas and strDir.esAlturaSN(strDir.strAltura)):
#                    retval.append(Direccion(calles[i],0))
#                hayCalleSN = True
#                    
#            if(maxOptions != 0 and len(retval) >= int(maxOptions)):
#                break
#        if(hayCalleSN and len(retval) == 0):
#            raise ErrorCalleSinAlturas(strDir.strInput)
#        return retval
        
    def filtrarCallesQueNoSonAv(self, dirs, getFunc='getCalle'):
        '''
        Verifica si las direcciones en dirs tienen tramos como avenidi
        @param dirs: Lista de direcciones a verificar
        @type dirs: Array de Direccion
        @param getFunc: Nombre del metodo para obtener la calle de la Direccion
        @type getFunc: String
        @return: Lista de Calle que tienen tramo como avenida
        @rtype: Array de Direccion
        '''
        opts=[]
        for i in range(len(dirs)):
## Se puede hacer directamente sin usar if?
            if(getFunc=='getCalle'):
                dir = dirs[i].getCalle()
            elif(getFunc=='getCalleCruce'):
                dir = dirs[i].getCalleCruce()
            if(self.c.tieneTramosComoAv(dir)):
                opts.append(dirs[i])
        return opts

    def normalizarCalleYCalle(self, strDir, maxOptions):
        '''
        Normaliza una direccion de tipo calle-calle
        @param strDir: La direccion a ser normalizada
        @type strDir: StringDireccion
        @param maxOptions: Maximo numero de opciones a retornar. Por defecto es 10.
        @type maxOptions: Integer
        @return: Las opciones halladas que se corresponden con dir
        @rtype: Array de Direccion 
        '''
        calles1 = self.c.buscarCalle(strDir.strCalles[0], 50)
        calles2 = self.c.buscarCalle(strDir.strCalles[1], 50)

# Armo una lista tabu para evitar agregar 2 veces una interseccion
# de una calle con otra que es calle y avenida a la vez
# Ej. CIUDAD DE LA PAZ y MONROE y CIUDAD DE LA PAZ y MONROE AV.
        matches = []
        opts = []
        for i in range(len(calles1)):
            for j in range(len(calles2)):
                if((calles1[i].codigo != calles2[j].codigo) and (not self.matchCode(calles1[i], calles2[j]) in matches) and (calles1[i].seCruzaCon(calles2[j]) and calles2[j].seCruzaCon(calles1[i]))):
                    opts.append(Direccion(calles1[i], 0, calles2[j]))
                    matches.append(self.matchCode(calles1[i],calles2[j]))
                    if(len(opts) >= maxOptions):
                        break
            if(len(opts) >= maxOptions):
                break

        if(len(opts) == 0 and len(calles1) > 0 and len(calles2) > 0):
            palabrasCalle1 = strDir.strCalles[0].split(u' ')
            palabrasCalle2 = strDir.strCalles[1].split(u' ')
# Pasarlo a funcion
            if((u'AV' in palabrasCalle1 ) or (u'AVDA' in palabrasCalle1) or (u'AVENIDA' in palabrasCalle1)):
                strDir1 = copy.copy(strDir)
                strDir1.quitarAvsCalle()
                try:
                    opts1 = self.normalizarCalleYCalle(strDir1, maxOptions) 
                except:
                    raise ErrorCruceInexistente(strDir.strCalles[0], calles1, strDir.strCalles[1], calles2)
                self.filtrarCallesQueNoSonAv(opts1)
                if(isinstance(opts1, list)):
                    return opts1
# Pasarlo a funcion
            if((u'AV' in palabrasCalle2 ) or (u'AVDA' in palabrasCalle2) or (u'AVENIDA' in palabrasCalle2)):
                strDir2 = copy.copy(strDir)
                strDir2.quitarAvsCalleCruce()
                try:
                    opts2 = self.normalizarCalleYCalle(strDir2, maxOptions) 
                except:
                    raise ErrorCruceInexistente(strDir.strCalles[0], calles1, strDir.strCalles[1], calles2)
                self.filtrarCallesQueNoSonAv(opts2)
                if(isinstance(opts2, list)):
                    return opts2

# Esto es para salvar el caso de calles con Y en el nombre pero
# que aun no estan escritas completas
# Ej. ORTEGA Y GA
        if(len(opts) < maxOptions):
            calles = self.c.buscarCalle(strDir.strInput)
            for i in range(len(calles)):
                opts.append(calles[i])
                if(len(opts) >= maxOptions):
                    break
        if(len(opts) == 0 and len(calles1) > 0 and len(calles2) > 0):
            raise ErrorCruceInexistente(strDir.strCalles[0], calles1, strDir.strCalles[1], calles2)
        return opts
    
    def matchCode(self, calle1, calle2):
        return min(calle1.codigo, calle2.codigo)+max(calle1.codigo, calle2.codigo)
            
    def __sinAcentos(self, s):
        if type(s) != unicode:
            s = unicode(s, 'utf-8')
        for i in range(len(self.rExps)):
            s = s.replace(self.rExps[i],self.repChar[i])
        return s
    
    def __verificarBusquedaDireccion(self, posibleDireccion, matcheo):
        pMatcheo = self.__sinAcentos(matcheo.upper()).split(' ')
        pCalle = re.sub(r'[,.]','',posibleDireccion.toString()).split(' ')
        for m in pMatcheo:
            for c in pCalle:
                if m == c and len(m) > 3:
                    return True
        return False
    
    def __buscarCalleAltura(self,texto):
        textoDireccion = texto[::-1]
        direccion = ""
        rDireccion = []
        try:
            try:
                for i in range(1,self.maxPalabras):
                    direccion = self.regexps['calleAltura'][i].search(textoDireccion)
                    if direccion.start() != 0:
                        raise Exception('Direccion no valida')
                    rDireccion = self.normalizar(direccion.group()[::-1], 2)
            except Exception, e:
                direccion = self.regexps['calleAltura'][i-1].search(textoDireccion)
            if self.__verificarBusquedaDireccion(rDireccion[0], direccion.group()[::-1]):
                return {
                    "match": rDireccion[0],
                    "start": len(textoDireccion) - direccion.end(),
                    "end": len(textoDireccion)}
        except Exception, e:
            return False
        return False
    
    def __buscarCruceCalles(self, texto, startConector, endConector):
        textoCalle = texto[:startConector][::-1]
        textoCruce = texto[endConector:]
        conector = texto[startConector:endConector]
        calle = cruce = ""
        rCalle = rCruce = []
        try:
            try:
                for i in range(1,self.maxPalabras):
                    cruce = self.regexps['calle'][i].search(textoCruce)
                    if cruce.start() != 0:
                        raise Exception('Direccion no valida')
                    rCruce = self.normalizar(cruce.group(), 2)
            except Exception, e:
                cruce = self.regexps['calle'][i-1].search(textoCruce)
            try:
                for i in range(1,self.maxPalabras):
                    calle = self.regexps['calle'][i].search(textoCalle)
                    if calle.start() != 0:
                        raise Exception('Direccion no valida')
                    rCruce = self.normalizar(calle.group()[::-1], 2)
            except Exception, e:
                calle = self.regexps['calle'][i-1].search(textoCalle)
            resultados = self.normalizar(calle.group()[::-1] + conector + cruce.group(), 2)
            if self.__verificarBusquedaDireccion(resultados[0], calle.group()[::-1] + conector + cruce.group()):
                return {
                    "match": resultados[0],
                    "start": calle.start(),
                    "end": len(texto) - cruce.start()}
            else:
                return False
        except Exception, e:
            return False
        return False
    
    def __buscarDirecciones(self, texto, maxResults):
        resultados = []
        posiblesDirecciones = re.compile(r'((\s+y\s+)|(\s+\d+))',re.I).finditer(texto)
        res = False
        for posibleDireccion in posiblesDirecciones:
            try:
                float(posibleDireccion.group())
                res = self.__buscarCalleAltura(texto[:posibleDireccion.end()])
            except Exception, e:
                if 'float' in e.message:
                    res = self.__buscarCruceCalles(texto, posibleDireccion.start(), posibleDireccion.end())
                else:
                    raise e
            if res:
                if len(resultados) > 0:
                    if res['start'] == resultados[-1]['start'] and res['match'].toString() == resultados[-1]['match'].toString():
                        if res['end'] > resultados[-1]['end']:
                            resultados[-1]=res
                    else:
                        resultados.extend([res])
                else:
                    resultados.extend([res])
            if not (len(resultados) < maxResults):
                return resultados
        if len(resultados) > 0:
            return resultados
        else:
            return False
        
    def buscarDireccion(self, texto):
        res = self.__buscarDirecciones(texto, 1)
        if res:
            return res[0]
    
    def buscarDirecciones(self, texto, maxResults = 'Todos'):
        if len(texto) > 0:
            if type(texto) != unicode:
                texto = unicode(texto, 'utf-8')
            res = self.__buscarDirecciones(texto, maxResults)
            if res:
                return res
        return False