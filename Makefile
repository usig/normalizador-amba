# Normalizador de Direcciones AMBA Python
VERSION = $(shell python normalizador_direcciones_amba/__init__.py)

prepare:
	find dist/ -type f -name "normalizador_direcciones-*$(VERSION)*" -exec rm -if {} \;
	find . -type f -name "MANIFEST" -exec rm -if {} \;
	python setup.py sdist


