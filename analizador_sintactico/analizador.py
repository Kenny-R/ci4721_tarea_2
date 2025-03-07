import re
import traceback
from termcolor import colored


class analizador:

    def __init__(self, reglas=None, precedencias=None, simbolo_inicial=None, simbolos_terminales=None, simbolos_no_terminales=None):
        self.simbolo_inicial = ''
        self.simbolos_no_terminales = ''
        self.simbolos_terminales = ''

        self._regex_simbolos_no_terminales = r'[A-Z]'
        self._regex_simbolos_terminales = r'[^A-Z\s$<>=]'
        self.se_puende_calcular_f_g = True

        self.reglas = {}
        self.precedencias = {}

        self.f_n_adyacencia = {}
        self.g_n_adyacencia = {}
        self.f_n_camino_mas_largo = {}
        self.g_n_camino_mas_largo = {}

        self.construido = False

        if reglas is not None:
            self.reglas = reglas
        if precedencias is not None:
            self.precedencias = precedencias
        if simbolo_inicial is not None:
            self.simbolo_inicial = simbolo_inicial
        if simbolos_terminales is not None:
            self.simbolos_terminales = simbolos_terminales
        if simbolos_no_terminales is not None:
            self.simbolos_no_terminales = simbolos_no_terminales

    def _agregar_simbolo(self, simbolo: str):

        if simbolo in self.simbolos_terminales:
            return

        if simbolo in self.simbolos_no_terminales:
            return

        if re.match(self._regex_simbolos_no_terminales, simbolo) != None:
            self.simbolos_no_terminales += simbolo
            return

        if re.match(self._regex_simbolos_terminales, simbolo) != None:
            self.simbolos_terminales += simbolo
            return

        raise Exception(f'El simbolo "{simbolo}" no es valido')

    def _verificar_si_es_gramatica_de_operadores(self, no_terminal, regla: list[str]):
        ultimo_simbolo = ''
        for simbolo in regla:

            if (re.match(self._regex_simbolos_no_terminales, simbolo) != None
                    and len(simbolo) != 1):
                raise Exception(
                    f'La gramática no es de operadores. El simbolo no terminal {simbolo} tiene tamaño {len(simbolo)} != 1.')

            if ultimo_simbolo == '':
                ultimo_simbolo = simbolo
                continue

            if (re.match(self._regex_simbolos_no_terminales, ultimo_simbolo) != None
                    and re.match(self._regex_simbolos_no_terminales, simbolo) != None):
                raise Exception(
                    f'La regla "{no_terminal} -> {''.join(regla)}" no corresponde a una gramática de operadores')

            self._agregar_simbolo(simbolo)

            ultimo_simbolo = simbolo

    def _crear_clases_de_equivalencia(self):
        clases_equivalencia = {}
        if self.precedencias.get('=') != None:
            for equivalencia in self.precedencias['=']:
                # llamaremos a la clase de equivalencia como el primer elemento de la tupla
                clases_equivalencia[equivalencia[1]] = equivalencia[0]

        return clases_equivalencia

    def _crear_grafo(self):

        clases_equivalencia = self._crear_clases_de_equivalencia()

        # creamos las funciones para las precedencias >
        for precedencia in self.precedencias['>']:
            a = precedencia[0]
            b = precedencia[1]

            # Verificamos si realmente a o b pertenecen a una clase de equivalencia
            if clases_equivalencia.get(a) != None:
                a = clases_equivalencia[a]

            if clases_equivalencia.get(b) != None:
                b = clases_equivalencia[b]

            if self.f_n_adyacencia.get(a) == None:
                self.f_n_adyacencia[a] = []

            if b in self.f_n_adyacencia[a]:
                continue

            self.f_n_adyacencia[a].append(b)

        # creamos las funciones para las precedencias <
        for precedencia in self.precedencias['<']:
            a = precedencia[0]
            b = precedencia[1]

            # Verificamos si realmente a o b pertenecen a una clase de equivalencia
            if clases_equivalencia.get(a) != None:
                a = clases_equivalencia[a]
            if clases_equivalencia.get(b) != None:
                b = clases_equivalencia[b]

            if self.g_n_adyacencia.get(b) == None:
                self.g_n_adyacencia[b] = []

            if a in self.g_n_adyacencia[b]:
                continue

            self.g_n_adyacencia[b].append(a)

    def _calcular_camino_mas_largo(self, funcion: str, simbolo):
        cola = [(funcion, simbolo, [f'{funcion}("{simbolo}")'])]
        camino_mas_largo = 0

        while len(cola) > 0:
            actual = cola.pop(0)

            if actual[0] == 'f':
                siguiente_funcion = 'g'
                adyacentes = self.f_n_adyacencia.get(actual[1])
            elif actual[0] == 'g':
                siguiente_funcion = 'f'
                adyacentes = self.g_n_adyacencia.get(actual[1])
            else:
                raise Exception('La función no es válida')

            largo_camino = len(actual[2]) - 1

            if adyacentes == None:
                camino_mas_largo = max(camino_mas_largo, largo_camino)
            else:
                for adyacente in adyacentes:

                    if f'{siguiente_funcion}("{adyacente}")' in actual[2]:
                        resultado = "Hay un ciclo en el grafo."
                        # resultado = f'Hay un ciclo en el grafo, siguiendo este camino\n{"->".join(actual[2])} \nvecinos de {actual[0]}("{actual[1]}"):\n'

                        # for valor in adyacentes:
                        #     resultado += f'{siguiente_funcion}("{valor}")\n'
                        raise Exception(resultado)

                    cola.append((siguiente_funcion, adyacente,
                                actual[2] + [f'{siguiente_funcion}("{adyacente}")']))

        return camino_mas_largo

    def _imprimir_tabla_precedencias(self):
        filas = []
        clases_equivalencia = self._crear_clases_de_equivalencia()

        # creamos la cabecera de la tabla
        fila_actual = ['|   |']
        for simbolo in self.simbolos_terminales:
            fila_actual.append(f' {simbolo} |')
        filas.append(fila_actual)

        # creamos la fila de f
        fila_actual = ['| f |']
        for simbolo in self.simbolos_terminales:
            if clases_equivalencia.get(simbolo) is not None:
                simbolo = clases_equivalencia[simbolo]
            fila_actual.append(f' {self.f_n_camino_mas_largo[simbolo]} |')
        filas.append(fila_actual)

        # creamos la fila de g
        fila_actual = ['| g |']
        for simbolo in self.simbolos_terminales:
            if clases_equivalencia.get(simbolo) is not None:
                simbolo = clases_equivalencia[simbolo]
            fila_actual.append(f' {self.g_n_camino_mas_largo[simbolo]} |')
        filas.append(fila_actual)

        # Determinar la longitud máxima de cada columna
        max_lens = [max(len(str(item)) for item in col) for col in zip(*filas)]

        # Ajustar las celdas para que todas tengan la misma longitud
        for fila in filas:
            for i, item in enumerate(fila):
                fila[i] = str(item).ljust(max_lens[i])

        # Imprimir la tabla
        print("Analizador sint ́actico construido.")
        print("Tabla con los valores de las funciones f y g: ")
        fila_mas_larga = max(len(fila) for fila in filas)
        print('|---' * fila_mas_larga + '|')
        for fila in filas:
            print(''.join(fila))
            print('|---' * fila_mas_larga + '|')

    def _preparar_entrada(self, entrada: str) -> str:
        entrada = '$' + entrada + '$'

        precedencias_inversas = {}

        for op, relaciones in self.precedencias.items():
            for (a, b) in relaciones:
                precedencias_inversas[(a, b)] = op

        nueva_entrada = ''

        for i in range(len(entrada)-1):
            a = entrada[i]
            b = entrada[i+1]
            if precedencias_inversas.get((a, b)) == None:
                raise Exception(
                    f'Lo simbolos "{a}" y "{b}" no son comparables')

            nueva_entrada += a + precedencias_inversas[(a, b)]

        nueva_entrada += entrada[-1]
        return nueva_entrada

    def _imprimir_salida_parse(self, salida: list[list[str]]):
        # Determinar la longitud máxima de cada columna
        max_lens = [max(len(str(item)) for item in col)
                    for col in zip(*salida)]

        # Ajustar las celdas para que todas tengan la misma longitud
        for i, row in enumerate(salida):
            for j, item in enumerate(row):
                if ((i == 0 or i == len(salida)-1) and j == 1):
                    row[j] = str(item).ljust(max_lens[j] - 21)
                else:
                    row[j] = str(item).ljust(max_lens[j])

        # Imprimir la tabla
        for row in salida:
            print(" | ".join(row))

    def _verificar_entrada(self, entrada: str):
        simbolos_no_conocidos = []
        simbolos_no_terminales_encontrados = []
        for simbolo in entrada:
            if re.match(self._regex_simbolos_no_terminales, simbolo) != None:
                simbolos_no_terminales_encontrados.append(simbolo)

            if (simbolo not in self.simbolos_no_terminales and
                    simbolo not in self.simbolos_terminales):
                simbolos_no_conocidos.append(simbolo)

        resultado = ''
        if len(simbolos_no_conocidos) > 0:
            resultado += 'Los siguientes simbolos no pertenecen a la gramatica: ' + \
                ', '.join(simbolos_no_conocidos) + '\n'

        if len(simbolos_no_terminales_encontrados) > 0:
            resultado += 'Una expresión no puede tener simbolos no-terminales, se encontro los siguientes simbolos no-terminales en la entrada: ' + \
                ', '.join(simbolos_no_terminales_encontrados) + '\n'

        if len(resultado) > 0:
            raise Exception('\n' + resultado)

    def _resaltar_texto(self, texto, inicio=0, fin=-1):
        return texto[:inicio] + colored(texto[inicio:fin+1], "green", attrs=["bold", "underline", "dark"]) + texto[fin+1:]

    def set_inicial(self, simbolo_inicial: str):
        if re.match(self._regex_simbolos_no_terminales, simbolo_inicial) == None:
            raise Exception(
                f'El simbolo {simbolo_inicial} no es un símbolo no-terminal')

        self.simbolo_inicial = simbolo_inicial
        print(f'"{simbolo_inicial}" es ahora el símbolo inicial de la gramática')

    def agregar_regla(self, no_terminal: str, simbolos: list[str]):
        if re.match(self._regex_simbolos_no_terminales, no_terminal) == None:
            raise Exception(
                f'El simbolo {no_terminal} no es un símbolo no-terminal')
            
        if len(no_terminal) != 1:
            raise Exception('El no terminal debe ser un solo caracter')

        self._verificar_si_es_gramatica_de_operadores(no_terminal, simbolos)

        for simbolo in simbolos:
            if (re.match(self._regex_simbolos_no_terminales, simbolo) != None
                    and simbolo not in self.simbolos_no_terminales):
                self.simbolos_no_terminales += simbolo

            if (re.match(self._regex_simbolos_terminales, simbolo) != None
                    and simbolo not in self.simbolos_terminales):
                self.simbolos_terminales += simbolo

        if self.reglas.get(no_terminal) == None:
            self.reglas[no_terminal] = []

        self._agregar_simbolo(no_terminal)
        self.reglas[no_terminal].append(simbolos)

        print(
            f'Regla "{no_terminal}->{''.join(simbolos)}" agregada a la gramatica')

    def agregar_precedencia(self, terminal1: str, op: str, terminal2: str):

        if op not in ['>', '<', '=']:
            raise Exception(
                f'El operador "{op}" no es un operacdor de precedencia no es válido')

        if re.match(self._regex_simbolos_terminales, terminal1) == None and terminal1 != '$':
            raise Exception(f'El terminal "{terminal1}" no es válido')

        if re.match(self._regex_simbolos_terminales, terminal2) == None and terminal2 != '$':
            raise Exception(f'El terminal "{terminal2}" no es válido')

        if self.precedencias.get(op) == None:
            self.precedencias[op] = []

        self.precedencias[op].append((terminal1, terminal2))

        resultado = f'{terminal1} tiene'

        if op == '>':
            resultado += ' mayor '
        elif op == '=':
            resultado += ' igual '
        elif op == '<':
            resultado += ' menor '

        print(resultado + terminal2)

    def build(self):
        self._crear_grafo()
        clases_equivalencia = self._crear_clases_de_equivalencia()

        try:
            for simbolo in self.simbolos_terminales:
                if clases_equivalencia.get(simbolo) != None:
                    simbolo = clases_equivalencia[simbolo]

                self.f_n_camino_mas_largo[simbolo] = self._calcular_camino_mas_largo(
                    'f', simbolo)
                self.g_n_camino_mas_largo[simbolo] = self._calcular_camino_mas_largo(
                    'g', simbolo)

            try:
                self._imprimir_tabla_precedencias()
            except Exception as e:
                print(
                    f"No se pueden imprimir las tablas de precedencias. Razón: {e}")
                # traceback.print_exc()
        except Exception as e:
            print(f"No se pueden calcular las funciones f y g. Razón: {e}")
            # traceback.print_exc()

        self.construido = True

    def estadisticas(self):
        self._crear_grafo()
        print("Símbolo inicial:", self.simbolo_inicial)
        print(f"Símbolos terminales: {self.simbolos_terminales}")
        print("Símbolos no terminales:", self.simbolos_no_terminales)
        print("\nReglas:")
        for no_terminal, reglas in self.reglas.items():
            for regla in reglas:
                print(f"  {no_terminal} -> {' '.join(regla)}")
        print("\nPrecedencias:")
        for op, precedencias in self.precedencias.items():
            for precedencia in precedencias:
                print(f"  {precedencia[0]} {op} {precedencia[1]}")
        print("\nAdyacentes de f_n:")
        for simbolo, adyacentes in self.f_n_adyacencia.items():
            print(f"  {simbolo} -> {', '.join(adyacentes)}")
        print("\nAdyacentes de g_n:")
        for simbolo, adyacentes in self.g_n_adyacencia.items():
            print(f"  {simbolo} -> {', '.join(adyacentes)}")
            
        print(self.f_n_adyacencia)
        print(self.g_n_adyacencia)

    def parse(self, entrada):

        if not self.construido:
            raise Exception('Aún no se ha consruido el analizador sintáctico')

        entrada = entrada.replace(' ', '')
        entrada = entrada.strip()

        self._verificar_entrada(entrada)
        nueva_entrada = self._preparar_entrada(entrada)

        reglas_inversas = {}
        precedencias_inversas = {}
        pila = []
        posicion = 0

        salida = [["Pila", "Entrada", "Acción"]]

        for op, relaciones in self.precedencias.items():
            for (a, b) in relaciones:
                precedencias_inversas[(a, b)] = op

        for no_terminal, reglas in self.reglas.items():
            for regla in reglas:
                clave = ''.join(regla)
                reglas_inversas[clave] = no_terminal

        if nueva_entrada[posicion] == '$':
            posicion += 1
        else:
            raise Exception(f'La frase {nueva_entrada} es mal formada')

        while nueva_entrada != '$$':

            salida.append([])
            salida[-1].append(str(pila))
            salida[-1].append(self._resaltar_texto(str(nueva_entrada), 1, posicion))

            simbolo = nueva_entrada[posicion]

            if simbolo == '>':
                contenido = ''
                posicion -= 1
                while nueva_entrada[posicion] != '<':

                    if nueva_entrada[posicion] == '$':
                        raise Exception('Falta un <')

                    contenido = nueva_entrada[posicion] + contenido

                    posicion -= 1

                produccion = ''
                while len(pila) != 0:
                    produccion = pila.pop() + produccion

                    if reglas_inversas.get(produccion) != None:
                        break

                if reglas_inversas.get(produccion) == None:
                    raise Exception(
                        f'No existe una regla que produzca {produccion}')

                pila.append(reglas_inversas[produccion])

                a = nueva_entrada[posicion - 1]
                b = nueva_entrada[posicion + len(contenido) + 2]

                if a == '$' and b == '$':
                    salida[-1].append(
                        f'reducir {reglas_inversas[produccion]} -> {produccion}')

                    salida.append([])
                    salida[-1].append(pila)
                    salida[-1].append(nueva_entrada[:posicion] +
                                      nueva_entrada[posicion + len(contenido) + 2:])

                    if len(pila) != 1 or pila[0] != self.simbolo_inicial:
                        salida[-1].append('Error')
                        self._imprimir_salida_parse(salida)
                        raise Exception(
                            'Ocurrio un problema al parsear, se redujo toda la expresión pero el simbolo final en la pila no es el simbolo inicial.')

                    salida[-1].append('aceptar')
                    self._imprimir_salida_parse(salida)
                    break

                salida[-1].append(
                    f'reducir {reglas_inversas[produccion]} -> {produccion}')

                if precedencias_inversas.get((a, b)) == None:
                    raise Exception(
                        f'Los simbolos "{a}" y {b} son incomparables')

                nueva_entrada = nueva_entrada[:posicion] + precedencias_inversas[(
                    a, b)] + nueva_entrada[posicion + len(contenido) + 2:]

            else:
                if re.match(self._regex_simbolos_terminales, simbolo) != None:
                    pila.append(simbolo)
                    posicion += 1
                    salida[-1].append(f'leer {simbolo}')
                    continue

                if simbolo in "<>=":
                    posicion += 1
                    salida[-1].append(f'leer {simbolo}')
                    continue

                if re.match(self._regex_simbolos_no_terminales, simbolo) != None:
                    raise Exception(
                        f'El simbolo "{simbolo}" es un no terminal. No pueden haber no terminales en las cadenas a parsear')

                if nueva_entrada[posicion] == '$':
                    raise Exception('Falta un >')

                raise Exception(f'Simbolo "{simbolo}" invalido')
