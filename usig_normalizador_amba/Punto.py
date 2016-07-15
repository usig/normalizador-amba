# coding: UTF-8
'''
Created on Apr 16, 2014

@author: hernan
'''
from __future__ import absolute_import


class Punto:
    '''
    @ivar x: Coordenada X del punto
    @type x: Float
    @ivar y: Coordenada Y del punto
    @type y: Float
    @ivar srid: Sistema de coordenadas
    @type srid: Int
    '''
    x = 0
    y = 0
    srid = -1

    def __init__(self, x, y, srid=0):
        '''
        @param x: Coordenada X del punto
        @type x: Float
        @param y: Coordenada Y del punto
        @type y: Float
        @ivar srid: Sistema de coordenadas
        @type srid: Int
        '''
        try:
            self.x = float(x)
            self.y = float(y)
            self.srid = int(srid)
        except Exception, e:
            raise e

    def __str__(self):
        '''
        Devuelve una representacion del punto como cadena en el formato '(x,y)'
        @return: Representacion del punto como cadena con la forma '(x,y)'
        @rtype: String
        '''
        return u'({0},{1})'.format(self.x, self.y)

    def __unicode__(self):
        return unicode(self.__str__())

    def toJson(self):
        '''
        Devuelve una representacion del punto en formato JSON
        @return: Representacion del punto como cadena JSON con la forma '{'x':XXXXX,'y':YYYYY,'srid':ZZZZ}'
        @rtype: String
        '''
        return u'{{"x":{0},"y":{1},"srid":{2}}}'.format(self.x, self.y, self.srid)

    def toDict(self):
        '''
        Devuelve una representacion del punto en un Dict de Python
        @return: Representacion del punto como Dict de Python
        @rtype: Dict
        '''
        return {'x': self.x,
                'y': self.y,
                'srid': self.srid}

    def toGeoJson(self):
        '''
        Devuelve una representacion del punto en formato GeoJSON
        @return: Representacion del punto como cadena GeoJSON
        @rtype: String
        '''
        return u'{"type": "Feature", "geometry": {"type": "Point", "coordinates": [{0}, {1}]}}'.format(self.x, self.y)

    def toWKT(self):
        '''
        Devuelve una representacion del punto en formato WKT
        @return: Representacion del punto como cadena WKT
        @rtype: String
        '''
        return u'POINT ({0},{1})'.format(self.x, self.y)
