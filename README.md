# Normalizador de Direcciones AMBA
El procedimiento de normalización de direcciones tiene por objetivo unificar la escritura de direcciones con respecto a un callejero de referencia.

'Normalizador de Direcciones AMBA' es una componente python para normalizar direcciones del AMBA (conurbano y CABA).

## Partidos disponibles:
Servicio de callejeros: http://servicios.usig.buenosaires.gov.ar/callejero-amba

| Partidos                |                         |                         |
|-------------------------|-------------------------|-------------------------|
| * CABA                  | * General San Martín    | * Morón                 |
| * Almirante Brown       | * Hurlingham            | * Pilar                 |
| * Avellaneda            | * Ituzaingó             | * Presidente Perón      |
| * Berazategui           | * José C. Paz           | * Quilmes               |
| * Berisso               | * La Matanza            | * San Fernando          |
| * Cañuelas              | * Lanús                 | * San Isidro            |
| * Ensenada              | * La Plata              | * San Miguel            |
| * Escobar               | * Lomas de Zamora       | * San Vicente           |
| * Esteban Echeverría    | * Malvinas Argentinas   | * Tigre                 |
| * Ezeiza                | * Marcos Paz            | * Tres de Febrero       |
| * Florencio Varela      | * Merlo                 | * Vicente López         |
| * General Rodríguez     | * Moreno                |                         |

## Instalación

### PyPi
```sh
$ pip install usig-normalizador-amba
```
### Git
```sh
$ git clone https://github.com/usig/normalizador-amba.git
$ cd normalizador-amba
$ python setup.py install
```
### Easy Install
```sh
$ git clone https://github.com/usig/normalizador-amba.git
$ cd normalizador-amba
$ make prepare-package
$ easy_install dist/usig-normalizador-amba-x.x.x.tar.gz
```
## Generación del paquete de instalación
```sh
$ make prepare-package
```
## Testing
En el root del proyecto ejecutar:

```sh
$ make run-test
```

## Ejemplos
```python
from usig_normalizador_amba import NormalizadorAMBA

nd = NormalizadorAMBA()
res = nd.normalizar('callao y corrientes')
for r in res:
    print r
```

Para instanciar el normalizador para algún/os partido/s en particular:

```python
from usig_normalizador_amba import NormalizadorAMBA

nd = NormalizadorAMBA(include_list=['caba']) # lista de codigos de partido
res = nd.normalizar(u'San Martín 153')
for r in res:
    print r
```

Para excluir del normalizador algún partido en particular:

```python
from usig_normalizador_amba import NormalizadorAMBA

nd = NormalizadorAMBA(exclude_list=['caba']) # lista de codigos de partido
res = nd.normalizar(u'San Martín 153')
for r in res:
    print r
```

Para buscar una dirección en un texto:

```python
from usig_normalizador_amba import NormalizadorAMBA

nd = NormalizadorAMBA() # lista de codigos de partido
res = nd.buscarDireccion(u'Ubicado en Monseñor Alejandro Schell 166, a metros de la estación de Lomas de Zamora.')
print res[0][0]['direcciones'][0]        
```
