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

## Instalacion del proyecto
```sh
git clone http://git-asi.buenosaires.gob.ar/usig/normalizador-amba.git
```

## Testing
```sh
make run-test
```

## Instalación del paquete
```sh
easy_install normalizador_direcciones_amba-1.0.0.tar.gz
```

## Ejemplo de uso
```python
from NormalizadorDireccionesAMBA import NormalizadorDireccionesAMBA

nd = NormalizadorDireccionesAMBA()
res = nd.normalizar('callao y corrientes')
for r in res:
    print r
```
