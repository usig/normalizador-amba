# coding: UTF-8
import sys, os
import json

sys.path.append(os.path.join('..','normalizador_direcciones_amba'))

from commons import normalizarTexto

def cargarCallejeroEstatico(c):
    filename = 'callejeros/{0}.callejero'.format(c.partido.codigo)
    with open(filename) as data_file:
        data = json.load(data_file)
    for d in data:
        d.append(set(normalizarTexto(d[1], separador=' ', lower=False).split(' ')))
    c.data = data
    c.data.sort()
    c.osm_ids = [k[0] for k in c.data]
