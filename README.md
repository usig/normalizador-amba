# Normalizador de Direcciones AMBA
El procedimiento de normalización de direcciones tiene por objetivo unificar la escritura de direcciones con respecto a un callejero de referencia.
A su vez ofrece herramientas para consultar de manera transparente la existencia de cruces de calle, calles pertenecientes a
partidos, calle con altura con y sin partido determinado. 'Normalizador de Direcciones AMBA' es una componente python para normalizar direcciones del AMBA (conurbano y CABA).


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
str = 'callao y corrientes'
print('A normalizar cruce: ', str)
try:
    res = nd.normalizar(str)
    for r in res:
        print('Nombre calle : ', r.calle.nombre)
        print('Cruce calle: ', r.cruce.nombre)
        print('Altura del cruce: ', r.altura)
        print('Coordenadas: ', r.coordenadas)
        print('Localidad del cruce: ', r.localidad)
        print('Partido del cruce', r.partido.nombre)
        print('___________________')
except Exception as e:
    print('error')
    print('___________________')
```

Para instanciar el normalizador para algún/os partido/s en particular:

```python
from usig_normalizador_amba import NormalizadorAMBA
nd = NormalizadorAMBA(include_list=['caba']) # lista de codigos de partido
str = u'San Martín 153'
cont=0
print('A normalizar en un partido (caba): ',str)
try:
    res = nd.normalizar(str)
    for r in res:
        print('Partido: ', res[cont].partido.nombre)
        print('Localidad: ', res[cont].localidad)
        print('Nombre de la calle: ', res[cont].calle.nombre)
        print('Altura: ', res[cont].altura)
        print('___________________')
        cont += 1
except Exception as e:
    print('error')
    print('___________________')
```

Para excluir del normalizador algún partido en particular:

```python
from usig_normalizador_amba import NormalizadorAMBA

nd = NormalizadorAMBA(exclude_list=['caba'])  # lista de codigos de partido
str = u'San Martín 153'
cont = 0
print('A normalizar excluyendo un partido (caba): ',str)
try:
    res = nd.normalizar(str)
    for r in res:
        print('Partido: ', res[cont].partido.nombre)
        print('Localidad: ', res[cont].localidad)
        print('Nombre de la calle: ', res[cont].calle.nombre)
        print('Altura: ', res[cont].altura)
        print('___________________')
        cont += 1
except Exception as e:
    print('error')
    print('___________________')
```

Para buscar una dirección en un texto:

```python
from usig_normalizador_amba import NormalizadorAMBA

def parseText(str):
    nd = NormalizadorAMBA()  # lista de codigos de partido
    res = nd.buscarDireccion(str)
    print('Texto filtrado:',res[0][0]['texto'])
    print('Partido: ',res[0][0]['direcciones'][0].partido.nombre)
    print('Localidad: ', res[0][0]['direcciones'][0].localidad)
    print('Calle: ', res[0][0]['direcciones'][0].calle.nombre)
    print('Altura ', res[0][0]['direcciones'][0].altura)
    print('___________________')

direcciones = [u'Ubicado en Monseñor Alejandro Schell 166, a metros de la estación de Lomas de Zamora.',
               u'ministro brin al 600',
               '9 de julio al 1963',
               'nueve de julio al 700',
               '9 de julio al setecientos',
               '9 de jul 800',
               'calle inventada 1500',
               u'calle ministro brin al 600',
               u'ninguna calle y otra calle']

for direccion in direcciones:
    try:
        parseText(direccion)
    except Exception as e:
        print(e)
        print('___________________')    
```
