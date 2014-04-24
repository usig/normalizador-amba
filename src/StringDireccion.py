# coding: UTF-8
'''
Created on Apr 29, 2010

@author: hernan
@note: Version de documentacion hasta revision 1717
'''
#from string import maketrans
import re
from settings import *

class StringDireccion:
    '''
    Parsea un string que presuntamente representa una direccion; lo tipifica y lo separa en tokens.
    Luego de instanciada la propiedad publica "tipo" puede asumir los siguientes valores:
     - CALLE
     - CALLE_ALTURA
     - CALLE_Y_CALLE
     - INVALIDO
    @ivar aceptarCallesSinAlturas: Indica si debe permitir como altura S/N para las calles sin numero. Por defecto es False. Ej: de los italianos S/N
    @type aceptarCallesSinAlturas: Boolean 
    @ivar strInput: El texto a analizar
    @type strInput: String
    @ivar tipo: Constante que indica la tipificacion asignada al string de entrada
    @type tipo: Integer
    @ivar strCalles: String que representa el presunto nombre de la calle o array de strings que representan las presuntas calles que se intersectan
    @type strCalles: String [Array]
    @ivar strAltura: Presunta altura de la calle
    @type strAltura: Integer
    '''

    aceptarCallesSinAlturas = False
    strInput = '' 

    tipo = INVALIDO
    strCalles = ''
    strAltura = ''

    def __init__(self, strInput, aceptarCallesSinAlturas = False):
        self.aceptarCallesSinAlturas = aceptarCallesSinAlturas
        # t = maketrans(".,","  ")
        # self.strInput = strInput.translate(t,"\"").upper().strip()
            
        self.strInput = strInput.upper()
        self.strInput = re.sub(unicode(r'[.,\"\']', 'utf-8'), lambda mo: ' ', self.strInput)
        self.strInput = re.sub(unicode(re.escape("("),'utf-8'),' ',self.strInput)
        self.strInput = re.sub(unicode(re.escape(")"),'utf-8'),' ',self.strInput)
        self.strInput = re.sub(unicode(r'\s+','utf-8'),' ',self.strInput).strip()

        if(len(self.strInput) > 0):
            palabras = self.strInput.split(" Y ")
            if(len(palabras) >= 2):
                s = self.fixCallesConY(self.strInput)
                palabras = s.split(" Y ")
                if(len(palabras) >= 2):
                    self.tipo = CALLE_Y_CALLE
                    calle1 = self.replaceWords(palabras[0], [(' & ', ' Y ')])
                    calle2 = self.replaceWords(palabras[1], [(' & ', ' Y ')])
                    self.strCalles = [calle1, calle2]
            palabras = self.strInput.split(" E ")
            if(len(palabras) >= 2):
                if(not palabras[len(palabras)-1].isdigit()):
                    self.tipo = CALLE_Y_CALLE
                    self.strCalles = palabras
            if(self.tipo == INVALIDO):
                self.setearCalleAltura()
        else:
            self.tipo = INVALIDO

    def setearCalleAltura(self):
        '''
        Configura el objeto como "calle altura" o como "calle" a partir del strInput
        '''
        palabras = self.strInput.split(" ")
        cantPalabras = len(palabras)
        if(cantPalabras > 1 and self.esTipoAltura(palabras[cantPalabras - 1], self.aceptarCallesSinAlturas)):
            self.tipo = CALLE_ALTURA
            self.strAltura = palabras.pop()
            self.strCalles = ' '.join(palabras)
        else:
            self.tipo = CALLE
            self.strCalles = self.strInput                
    
    def __str__(self):
        retval = "- CLASE: StringDireccion\n"
        retval += "\taceptarCallesSinAlturas: %s \n"%str(self.aceptarCallesSinAlturas)
        retval += "\tstrInput: %s \n"%self.strInput
        retval += "\ttipo: %s\n"%str(self.tipo)
        retval += "\tstrCalles: %s\n"%self.strCalles
        retval += "\tstrAltura: %s\n"%self.strAltura
        return retval

    def esAlturaSN(self, str):
        return (re.match('(?i)s(/|\\\\)n$',str) != None)

    def esTipoAltura(self, str, aceptarCallesSinAlturas):
        return str.isdigit() or (self.aceptarCallesSinAlturas and self.esAlturaSN(str))

    def removeWords(self, str, words):
        '''
        Utility function that allows you to easily replace certain words from a string.
        Return a copy of string str with all occurrences of substring old replaced by new.
        '''
        strSplit = str.split(" ")
        for word in words:
            for i in range(len(strSplit)):
                if(word == strSplit[i]):
                    strSplit.pop(i)
                    break
        return " ".join(strSplit)

    def replaceWords(self, str, findReplace):
        for tupla in findReplace:
            str = str.replace(tupla[0], tupla[1])
        return str

    def fixCallesConY(self, str):
        calles = [("GELLY Y OBES", "GELLY & OBES"),
                   ("MENENDEZ Y PELAYO", "MENENDEZ & PELAYO"),
                   ("OLAGUER Y FELIU", "OLAGUER & FELIU"),
                   ("ORTEGA Y GASSET", "ORTEGA & GASSET"),
                   ("PAULA Y RODRIGUEZ", "PAULA & RODRIGUEZ"),
                   ("PAZ Y FIGUEROA", "PAZ & FIGUEROA"),
                   ("PI Y MARGALL", "PI & MARGALL"),
                   ("RAMON Y CAJAL", "RAMON & CAJAL"),
                   ("TORRES Y TENORIO", "TORRES & TENORIO"),
                   ("TREINTA Y TRES", "TREINTA & TRES"),]
        return self.replaceWords(str, calles)

    def quitarAvsCalle(self):
        '''
        Elimina las palabras 'AV', 'AVDA' y 'AVENIDA' de la calle
        '''
        avs = [u'AV', u'AVDA', u'AVENIDA']
        if(self.tipo == CALLE_ALTURA):
            self.strCalles = self.removeWords(self.strCalles, avs)
        elif(self.tipo == CALLE_Y_CALLE):
            self.strCalles[0] = self.removeWords(self.strCalles[0], avs)

    def quitarAvsCalleCruce(self):
        '''
        Elimina las palabras 'AV', 'AVDA' y 'AVENIDA' del cruce
        '''
        avs = [u'AV', u'AVDA', u'AVENIDA']
        if(self.tipo == CALLE_Y_CALLE):
            self.strCalles[1] = self.removeWords(self.strCalles[1], avs)

    def quitarPasajes(self):
        '''
        Elimina las palabras 'PJE', 'PSJE' y 'PASAJE' de strCalles
        '''
        pje = [u'PJE', u'PSJE', u'PASAJE']
        if(self.tipo == CALLE_ALTURA):
            self.strCalles = self.removeWords(self.strCalles, pje)
        elif(self.tipo == CALLE_Y_CALLE):
            self.strCalles[0] = self.removeWords(self.strCalles[0], pje)
            self.strCalles[1] = self.removeWords(self.strCalles[1], pje)
