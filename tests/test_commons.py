# coding: UTF-8
from __future__ import absolute_import
import json

from usig_normalizador_amba.commons import normalizarTexto


def cargarCallejeroEstatico(c):
    filename = 'callejeros/{0}.callejero'.format(c.partido.codigo)
    with open(filename) as data_file:
        data = json.load(data_file)
    for d in data:
        d.append(set(normalizarTexto(d[1], separador=' ', lower=False).split(' ')))
    c.data = data
    c.data.sort()
    c.osm_ids = [k[0] for k in c.data]
