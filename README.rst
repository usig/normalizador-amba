Normalizador de Direcciones AMBA
================================
El procedimiento de normalización de direcciones tiene por objetivo unificar la escritura de direcciones con respecto a un callejero de referencia.
A su vez ofrece herramientas para consultar de manera transparente la existencia de cruces de calle, calles pertenecientes a
partidos, calle con altura con y sin partido determinado. 'Normalizador de Direcciones AMBA' es una componente python para normalizar direcciones del AMBA (conurbano y CABA).

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

Para instanciar el normalizador para algún/os partido/s en particular:

.. code:: python
    
    from usig_normalizador_amba import NormalizadorAMBA

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


Para excluir del normalizador algún partido en particular:

.. code:: python
    
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


Para buscar una dirección en un texto:

.. code:: python
    
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
    