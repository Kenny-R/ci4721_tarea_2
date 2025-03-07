import pytest
from ..analizador import analizador


class TestAnalizadorSintactico:
    def test_init(self):
        a = analizador()
        assert a.simbolos_terminales == ''
        assert a.simbolos_no_terminales == ''
        assert a.reglas == {}
        assert a.precedencias == {}
        assert a.simbolo_inicial == ''
        assert a.construido == False

    def test_agrear_simbolo_terminal_simbolo_correcto(self):
        a = analizador()
        a._agregar_simbolo('a')
        assert a.simbolos_terminales == 'a'

        a._agregar_simbolo('a')
        assert a.simbolos_terminales == 'a'

    def test_agrear_simbolo_terminal_simbolo_incorrecto(self):
        a = analizador()
        with pytest.raises(Exception):
            a._agregar_simbolo('<')

    def test_verificar_si_es_gramatica_de_operadores_no_es(self):
        a = analizador()
        a._agregar_simbolo('a')
        a._agregar_simbolo('B')
        with pytest.raises(Exception):
            a._verificar_si_es_gramatica_de_operadores('B', ['B', 'B'])

    def test_verificar_si_es_gramatica_de_operadores_si_es(self):
        a = analizador()
        a._agregar_simbolo('a')
        a._agregar_simbolo('B')
        a._verificar_si_es_gramatica_de_operadores('B', ['a', 'B'])

    def test_crear_clases_de_equivalencia(self):
        simbolos_terminales = 'ab()'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['(', 'A', ')']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '=': [('(', ')'), ('a', 'b')],
        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)
        resulado = a._crear_clases_de_equivalencia()
        assert resulado == {
            'b': 'a',
            ')': '('
        }

    def test_crear_grafo(self):
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        a._crear_grafo()

        assert a.f_n_adyacencia == {
            'a': ['+', '*', '$'], '+': ['+', '$'], '*': ['*', '$']}
        assert a.g_n_adyacencia == {
            '*': ['+', '$'], 'a': ['+', '*', '$'], '+': ['$']}

    def test_calcular_camino_mas_largo(self):
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        a._crear_grafo()

        resultado = a._calcular_camino_mas_largo("f", "a")
        assert resultado == 4

    def test_preparar_entrada_bien(self):
        entrada_sin_tratar = "a+a+b+a"
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('+', 'b'),
                ('*', 'b'),
                ('$', 'b'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('b', '+'),
                  ('b', '*'),
                  ('b', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        assert a._preparar_entrada(entrada_sin_tratar) == '$<a>+<a>+<b>+<a>$'

    def test_preparar_entrada_mal(self):
        entrada_sin_tratar = "a+a+b+a"
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        with pytest.raises(Exception):
            a._preparar_entrada(entrada_sin_tratar)

    def test_verificar_entrada_bien(self):
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        a._verificar_entrada("a+a+b+a")

    def test_verificar_entrada_mal(self):
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        with pytest.raises(Exception):
            a._verificar_entrada("a+a+i+a")

    def test_set_inicial_bien(self):
        simbolo_inicial = 'A'

        a = analizador()
        a.set_inicial(simbolo_inicial)
        assert a.simbolo_inicial == 'A'

    def test_set_inicial_mal(self):
        simbolo_inicial = 'a'

        a = analizador()
        with pytest.raises(Exception):
            a.set_inicial(simbolo_inicial)

    def test_agregar_regla_bien(self):
        regla = ['a', '+', 'A']

        a = analizador()
        a.agregar_regla('A', regla)
        assert a.reglas == {'A': [['a', '+', 'A']]}
        assert a.simbolos_no_terminales == 'A'
        assert a.simbolos_terminales == '+a'

    def test_agregar_regla_mal_1(self):
        regla = ['a', '+', 'A']

        a = analizador()
        with pytest.raises(Exception):
            a.agregar_regla('a', regla)

    def test_agregar_regla_mal_2(self):
        regla = ['A', '+', 'A']

        a = analizador()
        with pytest.raises(Exception):
            a.agregar_regla('AA', regla)

    def test_agregar_precedencia_bien(self):
        precedencia = ('a', 'b')

        a = analizador()
        a.agregar_precedencia('a', '=', 'b')
        a.agregar_precedencia('a', '<', 'b')
        a.agregar_precedencia('a', '>', 'b')
        assert a.precedencias['='] == [('a', 'b')]
        assert a.precedencias['<'] == [('a', 'b')]
        assert a.precedencias['>'] == [('a', 'b')]

    def test_build(self):
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)
        a.build()
        assert a.construido == True
        assert a.simbolos_terminales == 'ab+*'
        assert a.simbolos_no_terminales == 'A'
        assert a.reglas == {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        assert a.simbolo_inicial == 'A'
        assert a.precedencias == {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]
        }
        assert a.f_n_adyacencia == {
            'a': ['+', '*', '$'], '+': ['+', '$'], '*': ['*', '$']}
        assert a.g_n_adyacencia == {
            '*': ['+', '$'], 'a': ['+', '*', '$'], '+': ['$']}

    def test_parse_bien(self):
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('+', 'b'),
                ('*', 'b'),
                ('$', 'b'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('b', '+'),
                  ('b', '*'),
                  ('b', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        a.build()
        a.parse("a+a+b")

    def test_parse_mal(self):
        simbolos_terminales = 'ab+*'
        simbolos_no_terminales = 'A'
        reglas = {
            'A': [['a'], ['b'], ['A', '+', 'A']]
        }
        simbolo_inicial = 'A'
        precedencias = {
            '<': [
                ('+', '*'),
                ('+', 'a'),
                ('*', 'a'),
                ('$', 'a'),
                ('+', 'b'),
                ('*', 'b'),
                ('$', 'b'),
                ('$', '+'),
                ('$', '*'),
            ],
            '>': [('a', '+'),
                  ('a', '*'),
                  ('a', '$'),
                  ('b', '+'),
                  ('b', '*'),
                  ('b', '$'),
                  ('+', '+'),
                  ('+', '$'),
                  ('*', '*'),
                  ('*', '$'),
                  ],
            '=': [('a', 'b')]

        }
        a = analizador(reglas, precedencias, simbolo_inicial,
                       simbolos_terminales, simbolos_no_terminales)

        a.build()
        with pytest.raises(Exception):
            a.parse("a+a+*b")
