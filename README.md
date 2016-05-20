# Normalizador AMBA
'Normalizador AMBA' es una componente python para normalizar direcciones del AMBA (conurbano y CABA).

## Partidos disponibles:
Servicio de callejeros: http://servicios.usig.buenosaires.gov.ar/callejero-amba
* CABA
* Almirante Brown
* Avellaneda
* Berazategui
* Berisso
* Cañuelas
* Ensenada
* Escobar
* Esteban Echeverría
* Ezeiza
* Florencio Varela
* General Rodríguez
* General San Martín
* Hurlingham
* Ituzaingó
* José C. Paz
* La Matanza
* Lanús
* La Plata
* Lomas de Zamora
* Malvinas Argentinas
* Marcos Paz
* Merlo
* Moreno
* Morón
* Pilar
* Presidente Perón
* Quilmes
* San Fernando
* San Isidro
* San Miguel
* San Vicente
* Tigre
* Tres de Febrero
* Vicente López

## Instalación del proyecto
```sh
git clone http://git-asi.buenosaires.gob.ar/usig/normalizador-amba.git
```

## Generación de paquete de instalación
En el root del proyecto ejecutar:

```sh
make prepare-package
```


## Testing
En el root del proyecto ejecutar:

```sh
make run-test
```

## Instalación del paquete
En el directorio dist del proyecto se encuentra el paquete de instalación del Normalizador AMBA.

```sh
easy_install normalizador_direcciones_amba-1.0.0.tar.gz
```

## Ejemplos de uso
```python
from normalizador_direcciones_amba import NormalizadorAMBA

nd = NormalizadorAMBA()
res = nd.normalizar('callao y corrientes')
for r in res:
    print r
```

Para instanciar el normalizador para algún/os partido/s en particular:

```python
from normalizador_direcciones_amba import NormalizadorAMBA

nd = NormalizadorAMBA(include_list=['caba']) # lista de codigos de partido
res = nd.normalizar(u'San Martín 153')
for r in res:
    print r
```

Para excluir del normalizador algún partido en particular:

```python
from normalizador_direcciones_amba import NormalizadorAMBA

nd = NormalizadorAMBA(exclude_list=['caba']) # lista de codigos de partido
res = nd.normalizar(u'San Martín 153')
for r in res:
    print r
```
