# coding: UTF-8
'''
Created on Jun 17, 2014

@author: hernan
'''
from __future__ import absolute_import
import re

from usig_normalizador_amba.StringDireccion import StringDireccion
from usig_normalizador_amba.Callejero import Callejero
from usig_normalizador_amba.Calle import Calle
from usig_normalizador_amba.Errors import ErrorTextoSinDireccion, ErrorCalleInexistente, ErrorCruceInexistente, ErrorCalleInexistenteAEsaAltura
from usig_normalizador_amba.Direccion import Direccion
from usig_normalizador_amba.settings import default_settings
from usig_normalizador_amba.settings import CALLE, CALLE_ALTURA, CALLE_Y_CALLE
from usig_normalizador_amba.settings import MATCH_EXACTO, MATCH_PERMUTADO, MATCH_INCLUIDO, MATCH
from usig_normalizador_amba.commons import matcheaTexto


class NormalizadorDirecciones:
    '''
    NormalizadorDirecciones
    Esta clase implementa integramente un normalizador de direcciones que utiliza un Callejero de USIG para transformar un string en una direccion normalizada.
    @ivar c: El callejero del partido
    @type c: Callejero
    @ivar partido: El partido del callejero que se quiere instanciar
    @type partido: Partido
    '''
    c = None
    partido = None

    def __init__(self, partido, config={}):
        '''
        @param partido: Indica el partido del callejero
        @type partido: Partido
        '''
        # default config
        self.config = default_settings.copy()
        # custom config
        self.config.update(config)

        try:
            if partido is None:
                raise Exception(u'Debe indicar el partido.')
            self.c = Callejero(partido, config)
            self.partido = partido
        except Exception, e:
            raise e

    def recargarCallejero(self):
        try:
            self.c.cargarCallejero()
        except Exception, e:
            raise e

    def normalizar(self, direccion, maxOptions=10):
        '''
        @param direccion: La cadena a ser transformada en direccion
        @type direccion: Unicode
        @param maxOptions: Maximo numero de opciones a retornar. Por defecto es 10.
        @type maxOptions: Integer
        @return: Las opciones halladas que se corresponden con direccion
        @rtype: Array de Direccion
        '''
        res = []
        error = None

        if direccion == '':
            raise ErrorCalleInexistente(u'')

        if type(direccion) != unicode:
            direccion = unicode(direccion, encoding='utf-8', errors='ignore')
        strDir = StringDireccion(direccion)

        for candidato in strDir.candidatos:
            if candidato['tipo'] == CALLE:
                res += self.buscarCalle(candidato['calle'], maxOptions)
            elif candidato['tipo'] == CALLE_ALTURA:
                try:
                    res += self.normalizarCalleAltura(candidato['calle'], candidato['altura'], maxOptions)
                except Exception, error:
                    pass
            elif candidato['tipo'] == CALLE_Y_CALLE:
                try:
                    res += self.normalizarCalleYCalle(candidato['calle'], candidato['cruce'], maxOptions)
                except Exception, error:
                    pass

        if not res:
            direccion_sin_palabras_claves = self._quitarPalabrasClaves(direccion)
            if direccion_sin_palabras_claves != direccion:
                try:
                    res = self.normalizar(direccion_sin_palabras_claves, maxOptions)
                except:
                    pass

        if isinstance(res, list):
            if res:
                return res
            else:
                if error:
                    raise error
                else:
                    raise ErrorCalleInexistente(strDir.strOriginal)
        else:
            return res

    def _quitarPalabrasClaves(self, texto):
        try:
            patrones = [
                '^avenida ', ' avenida ', ' avenida$',
                '^avda\.? ', ' avda\.? ', ' avda\.?$',
                '^av\.? ', ' av\.? ', ' av\.?$',
                '^pasaje ', ' pasaje ', ' pasaje$',
                '^psje\.? ', ' psje\.? ', ' psje\.?$',
                '^pje\.? ', ' pje\.? ', ' pje\.?$',
            ]
            patron = '|'.join(patrones)
            return re.sub(patron, ' ', texto, flags=re.IGNORECASE)
        except:
            return texto

    def buscarCalle(self, inCalle, maxOptions):
        res = self.c.buscarCalle(inCalle, maxOptions)
        return res

    def normalizarCalleAltura(self, inCalle, inAltura, maxOptions=10):
        '''
        Normaliza una direccion de tipo Calle-altura
        @param inCalle: La calle a ser normalizada
        @type inCalle: String
        @param inAltura: La altura de la calle a ser normalizada
        @type inCalle: int
        @param maxOptions: Maximo numero de opciones a retornar.
        @type maxOptions: Integer
        @return: Las opciones halladas
        @rtype: Array de Direcciones
        '''
        opts = []
        calles = self.c.buscarCalle(inCalle)
        for calle in calles:
            if calle.alturaValida(inAltura):
                d = Direccion(calle, inAltura)
                opts.append(d)

        if(len(opts) == 0 and len(calles) > 0):
            raise ErrorCalleInexistenteAEsaAltura(inCalle, calles, inAltura)

        return opts

    def normalizarCalleYCalle(self, inCalle, inCruce, maxOptions=10):
        '''
        Normaliza una direccion de tipo calle-calle
        @param inCalle: Calle a ser normalizada
        @type inCalle: String
        @param inCruce: Cruce a ser normalizado
        @type inCruce: String
        @param maxOptions: Maximo numero de opciones a retornar. Por defecto es 10.
        @type maxOptions: Integer
        @return: Las opciones halladas que se corresponden con dir
        @rtype: Array de Direccion
        '''
        calles = self.c.buscarCalle(inCalle)

        opts = [[], [], [], [], []]
        for calle in calles:
            for idCruce in calle.cruces:
                cruces = self.c.buscarCodigo(idCruce)
                for cruce in cruces:
                    res = matcheaTexto(inCruce, cruce[2])
                    if res:
                        objCruce = Calle(cruce[0], cruce[1], [], cruce[4], calle.partido, cruce[5])
                        opts[res].append(Direccion(calle, 0, objCruce))
                        if(len(opts[MATCH_EXACTO]) >= maxOptions):
                            break
            if(len(opts[MATCH_EXACTO]) >= maxOptions):
                break

        opts = (opts[MATCH_EXACTO] + opts[MATCH_PERMUTADO] + opts[MATCH_INCLUIDO] + opts[MATCH])[:maxOptions]

        if(len(opts) == 0 and len(calles) > 0):
            raise ErrorCruceInexistente(inCalle, [], inCruce, [])
        return opts

    def _buscarIndicesDeCalleEnLista(self, palabras, sentido):
        # si sentido es -1 se desplaza a la izq, si es 1 se desplaza a la der
        retval = None
        cant_palabras = len(palabras)
        for i in range(cant_palabras):
            indice = (cant_palabras - 1 - i, cant_palabras) if sentido == -1 else (0, i + 1)
            calle = ' '.join(palabras[indice[0]:indice[1]])
            try:
                self.normalizar(calle)
                retval = indice
            except:
                break
        return retval

    def _buscarDireccionCalleAltura(self, token):
        retval = None
        palabras = re.split('\s', token.string[:token.start()])
        altura = token.groupdict()['dir_altura']
        indice = self._buscarIndicesDeCalleEnLista(palabras, -1)
        if indice:
            try:
                calle = ' '.join(palabras[indice[0]:indice[1]])
                direccion = u'{0} {1}'.format(calle, altura)
                res = [r for r in self.normalizar(direccion) if r.tipo == CALLE_ALTURA]
                if not res:
                    raise Exception()
                posicion = len(' '.join(palabras[:indice[0]]))
                posicion = posicion if indice[0] == 0 else posicion + 1  # Le sumo el espacio entre la direccion y lo que no es direccion
                texto = token.string[posicion:token.end()]
                retval = {'posicion': posicion, 'texto': texto, 'direcciones': res}
            except Exception:
                pass
        return retval

    def _buscarDireccionCalleCalle(self, token):
        retval = None
        palabras_izq = re.split('\s', token.string[:token.start()])
        palabras_der = re.split('\s', token.string[token.end():])
        indice_izq = self._buscarIndicesDeCalleEnLista(palabras_izq, -1)
        indice_der = self._buscarIndicesDeCalleEnLista(palabras_der, 1)
        if indice_izq and indice_der:
            try:
                calle_izq = ' '.join(palabras_izq[indice_izq[0]:indice_izq[1]])
                calle_der = ' '.join(palabras_der[indice_der[0]:indice_der[1]])
                direccion = u'{0}{1}{2}'.format(calle_izq, token.groupdict()['esq_conector'], calle_der)
                res = self.normalizar(direccion)
                res = [r for r in self.normalizar(direccion) if r.tipo == CALLE_Y_CALLE]
                if not res:
                    raise Exception()
                posicion = len(' '.join(palabras_izq[:indice_izq[0]]))
                posicion = posicion if indice_izq[0] == 0 else posicion + 1  # Le sumo el espacio entre la direccion y lo que no es direccion
                retval = {'posicion': posicion, 'texto': direccion, 'direcciones': res}
            except Exception:
                pass
        return retval

    def buscarDireccion(self, texto=''):
        texto = unicode(texto)
        ''' Patron: (dir_calle [al] dir_altura) | (esq_calle y|e esq_cruce) '''
        patron_calle_altura = '(?:(?P<dir_conector>(?:\s+al)?\s+)(?P<dir_altura>[0-9]+))'
        patron_calle_calle = '(?P<esq_conector>\s+(?:y|e)\s+)'
        patron = r'{0}|{1}'.format(patron_calle_altura, patron_calle_calle)
        tokens = re.finditer(patron, texto, re.I)
        retval = []

        for token in tokens:
            res = None
            if token.groupdict()['dir_altura']:
                res = self._buscarDireccionCalleAltura(token)
            elif token.groupdict()['esq_conector']:
                res = self._buscarDireccionCalleCalle(token)
            if res:
                retval.append(res)

        if not retval:
            raise ErrorTextoSinDireccion(texto)

        return retval
