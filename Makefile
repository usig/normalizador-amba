# Normalizador de Direcciones AMBA Python
VERSION = $(shell python -c 'import usig_normalizador_amba; print usig_normalizador_amba.__version__')
TITLE = $(shell python -c 'import usig_normalizador_amba; print usig_normalizador_amba.__title__')

run-test:
	@cd tests && python test.py

prepare-package:
	find dist/ -type f -name "$(TITLE)-*$(VERSION)*" -exec rm -if {} \;
	python setup.py sdist

install:
	python setup.py install

