# coding: UTF-8
from __future__ import absolute_import

default_settings = {
    'callejero_amba_server': 'http://servicios.usig.buenosaires.gob.ar/callejero-amba/',
    'callejero_caba_server': 'http://servicios.usig.buenosaires.gob.ar/callejero',
}

# Tipo de normalizacion
CALLE = 0
CALLE_ALTURA = 1
CALLE_Y_CALLE = 2
INVALIDO = -1

# Tipo de Match
NO_MATCH = 0
MATCH = 1
MATCH_INCLUIDO = 2
MATCH_PERMUTADO = 3
MATCH_EXACTO = 4
