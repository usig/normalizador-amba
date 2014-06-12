# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
'''

class Partido:
    '''
    @ivar codigo: Codigo de partido (nombre normalizado)
    @type codigo: String
    @ivar nombre: Nombre del partido
    @type nombre: Unicode
    @ivar nombre_largo: Nombre completo del partido 
    @type nombre: Unicode
    @ivar codigo_osm: Codigo de partido (OSM)
    @type codigo_osm: Integer
    '''
    codigo = ''
    nombre = ''
    nombre_largo = ''
    codigo_osm = 0

    def __init__(self, codigo, nombre, nombre_largo = '', codigo_osm = 0):
        '''
        @ivar codigo: Codigo de partido (nombre normalizado)
        @type codigo: String
        @ivar nombre: Nombre del partido
        @type nombre: Unicode
        @ivar nombre_largo: Nombre completo del partido 
        @type nombre: Unicode
        @ivar codigo_osm: Codigo de partido (OSM)
        @type codigo_osm: Integer
        '''
        try:
            self.codigo = str(codigo)
            self.nombre = unicode(nombre)
            self.nombre_largo = unicode(nombre_largo) if nombre_largo != '' else self.nombre
            self.codigo_osm = int(codigo_osm)
        except Exception, e:
            raise e

    def __str__(self):
        return self.__unicode__().encode('utf8','ignore')

    def __unicode__(self):
        retval = u'''-- Partido
    codigo = {0}
    nombre = {1}
    nombre largo = {2}
    codigo OSM = {3}'''
        return retval.format(self.codigo,
                         self.nombre,
                         self.nombre_largo,
                         self.codigo_osm)

    def toString(self):
        '''
        Devuelve un string con el partido escrito correctamente para mostrar
        @return: Partido como texto
        @rtype: String
        '''
        return self.nombre