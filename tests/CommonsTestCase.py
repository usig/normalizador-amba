# coding: UTF-8
from __future__ import absolute_import
import unittest

from usig_normalizador_amba.commons import normalizarTexto, matcheaTexto
from usig_normalizador_amba.commons import MATCH_EXACTO, MATCH_PERMUTADO, MATCH_INCLUIDO, MATCH, NO_MATCH


class CommonsTestCase(unittest.TestCase):

    def test_normalizarTexto_acentos(self):
        res = normalizarTexto(u'ábçdéfǵhíjḱĺḿńñóṕqŕśtúvẃxýźÁBÇDÉFǴHÍJḰĹḾŃÑÓṔQŔŚTÚVẂXÝŹäëïöüÄËÏÖÜ')
        self.assertEqual(res, u'abcdefghijklmnnopqrstuvwxyzabcdefghijklmnnopqrstuvwxyzaeiouaeiou')

    def test_normalizarTexto_espacios(self):
        res = normalizarTexto(u'   hola    chau         ')
        self.assertEqual(res, u'hola chau')

    def test_normalizarTexto_lower(self):
        res = normalizarTexto(u'   hola  á   chau         ', lower=False)
        self.assertEqual(res, u'HOLA A CHAU')

    def test_normalizarTexto_separador(self):
        res = normalizarTexto(u'   hola  á   chau         ', separador='_')
        self.assertEqual(res, u'hola_a_chau')

    def test_normalizarTexto_simbolos(self):
        res = normalizarTexto(u'hola !#$%&/()=?¡@"\\\' chau')
        self.assertEqual(res, u'hola chau')

    def test_matcheaTexto_no_match(self):
        res = matcheaTexto('partido de Lomas de Zamora', 'Lomas de Zamora')
        self.assertEqual(res, NO_MATCH)
        res = matcheaTexto(u'Lanús', 'Lomas de Zamora')
        self.assertEqual(res, NO_MATCH)

    def test_matcheaTexto_exacto(self):
        res = matcheaTexto('Lomas de Zamora', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_EXACTO)
        res = matcheaTexto('Lanus', u'Lanús')
        self.assertEqual(res, MATCH_EXACTO)

    def test_matcheaTexto_permutado(self):
        res = matcheaTexto('de lomas zamora', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_PERMUTADO)
        res = matcheaTexto('lomas zamora de', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_PERMUTADO)
        res = matcheaTexto('zamora lomas de', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_PERMUTADO)
        res = matcheaTexto('zamora de lomas', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_PERMUTADO)

    def test_matcheaTexto_incluido(self):
        res = matcheaTexto('Lomas', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_INCLUIDO)
        res = matcheaTexto('Lomas de', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_INCLUIDO)
        res = matcheaTexto('Lomas ZAMORA', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_INCLUIDO)
        res = matcheaTexto('ZAMORA Lomas', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_INCLUIDO)

    def test_matcheaTexto_match(self):
        res = matcheaTexto('', 'Lomas de Zamora')
        self.assertEqual(res, MATCH)
        res = matcheaTexto('Lom ZAM', 'Lomas de Zamora')
        self.assertEqual(res, MATCH)

    def test_matcheaTexto_normalizacion(self):
        res = matcheaTexto(u'-  (lomas, dé,  zámórá)-', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_EXACTO)

    def test_matcheaTexto_case(self):
        res = matcheaTexto('lOMAS DE zAMORA', 'Lomas de Zamora')
        self.assertEqual(res, MATCH_EXACTO)

    def test_matcheaTexto_no_normalizar_no_match(self):
        res = matcheaTexto('Lanus', u'Lanús', normalizar=False)
        self.assertEqual(res, NO_MATCH)
        res = matcheaTexto(u'-  (lomas, dé,  zámórá)-', 'Lomas de Zamora', normalizar=False)
        self.assertEqual(res, NO_MATCH)
        res = matcheaTexto('de lomas zamora', 'Lomas de Zamora', normalizar=False)
        self.assertEqual(res, NO_MATCH)
        res = matcheaTexto('lOMAS DE zAMORA', 'Lomas de Zamora', normalizar=False)
        self.assertEqual(res, NO_MATCH)
