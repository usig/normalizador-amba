# coding: UTF-8
"""
Normalizador de Direcciones AMBA

El procedimiento de normalización de direcciones tiene por objetivo unificar la escritura de direcciones con respecto a un callejero de referencia.
El normalizador de Direcciones AMBA toma como referencia los callejeros del Área Metropolitana de Buenos Aires.
"""

from __future__ import absolute_import

from usig_normalizador_amba.NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA as ND
NormalizadorAMBA = ND

__title__ = 'usig-normalizador-amba'
__description__ = 'Normalizador de Direcciones AMBA'
__author__ = 'USIG - GCBA'
__author_email__ = 'Hernán Ogasawara <hogasawara@buenosaires.gob.ar>'
__version__ = '1.2.4'
__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2016 USIG - GCBA'
