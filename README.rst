Normalizador de Direcciones AMBA
================================
El procedimiento de normalización de direcciones tiene por objetivo unificar la escritura de direcciones con respecto a un callejero de referencia.
'Normalizador de Direcciones AMBA' es una componente python para normalizar direcciones del AMBA (conurbano y CABA).

Partidos disponibles
~~~~~~~~~~~~~~~~~~~~
Servicio de callejeros: http://servicios.usig.buenosaires.gov.ar/callejero-amba

+-------------------------+-------------------------+
| * CABA                  | * La Plata              |
| * Almirante Brown       | * Lomas de Zamora       |
| * Avellaneda            | * Malvinas Argentinas   |
| * Berazategui           | * Marcos Paz            |
| * Berisso               | * Merlo                 |
| * Cañuelas              | * Moreno                |
| * Ensenada              | * Morón                 |
| * Escobar               | * Pilar                 |
| * Esteban Echeverría    | * Presidente Perón      |
| * Ezeiza                | * Quilmes               |
| * Florencio Varela      | * San Fernando          |
| * General Rodríguez     | * San Isidro            |
| * General San Martín    | * San Miguel            |
| * Hurlingham            | * San Vicente           |
| * Ituzaingó             | * Tigre                 |
| * José C. Paz           | * Tres de Febrero       |
| * La Matanza            | * Vicente López         |
| * Lanús                 |                         |
+-------------------------+-------------------------+


Instalación
-----------

PyPi
~~~~
.. code:: bash

    $ pip install usig-normalizador-amba

Git
~~~
.. code:: bash

    $ git clone https://github.com/usig/normalizador-amba.git
    $ cd normalizador-amba
    $ python setup.py install

Easy Install
~~~~~~~~~~~~
.. code:: bash

    $ git clone https://github.com/usig/normalizador-amba.git
    $ cd normalizador-amba
    $ make prepare-package
    $ easy_install dist/usig-normalizador-amba-x.x.x.tar.gz


Generación del paquete de instalación
-------------------------------------
.. code:: bash

    $ make prepare-package


Testing
-------
En el root del proyecto ejecutar:

.. code:: bash

    $ make run-test



Ejemplos
--------

.. code:: python
    
    from usig_normalizador_amba import NormalizadorAMBA

    nd = NormalizadorAMBA()
    res = nd.normalizar('callao y corrientes')
    for r in res:
        print r

Para instanciar el normalizador para algún/os partido/s en particular:

.. code:: python
    
    from usig_normalizador_amba import NormalizadorAMBA

    nd = NormalizadorAMBA(include_list=['caba']) # lista de codigos de partido
    res = nd.normalizar(u'San Martín 153')
    for r in res:
        print r


Para excluir del normalizador algún partido en particular:

.. code:: python
    
    from usig_normalizador_amba import NormalizadorAMBA

    nd = NormalizadorAMBA(exclude_list=['caba']) # lista de codigos de partido
    res = nd.normalizar(u'San Martín 153')
    for r in res:
        print r


Para buscar una dirección en un texto:

.. code:: python
    
    from usig_normalizador_amba import NormalizadorAMBA

    nd = NormalizadorAMBA() # lista de codigos de partido
    res = nd.buscarDireccion(u'Ubicado en Monseñor Alejandro Schell 166, a metros de la estación de Lomas de Zamora.')
    print res[0][0]['direcciones'][0]        
    