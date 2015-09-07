# coding: UTF-8
import sys, os, time, datetime
sys.path.append(os.path.join('..','normalizador_direcciones_amba'))
    
from NormalizadorDireccionesAMBA import *

nd = NormalizadorDireccionesAMBA()
filename = 'estaciones_de_servicio.txt'
data = []
count_match = 0

with open(filename, 'r') as f:
    for line in f:
        data.append(line.strip().decode('utf8','ignore'))
f.closed

ts_start = time.time()
for idx, d in enumerate(data, start=1):
    try:
        res = nd.normalizar(d)
        if res:
            count_match += 1
        print u'{0} - {1} ----> {2}'.format(str(idx).rjust(4, ' '), d, res[0].toString())
    except:
        pass
ts_end = time.time()

ts_delta = ts_end - ts_start

print '---------------------------------------------'
print '- Fecha: {0}'.format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
print '- Archivo: {0}'.format(filename)
print '- Direcciones: {0}'.format(len(data))
print '- Matchings: {0}'.format(count_match)
print '- Tiempo total: {0}'.format(str(datetime.timedelta(seconds=(ts_delta))))
print '- Tiempo promedio: {0}'.format((ts_delta) / len(data)) 
print '---------------------------------------------'