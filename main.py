from analizador_sintactico.analizador import analizador as asa
import traceback
import readline

if __name__ == "__main__":
    # reglas = {
    #     'E': [['E', '+', 'E'], ['E', '*', 'E'], ['i'], ['(', 'E', ')']]
    # }

    # precedencias = {
    #     '<': [
    #         ('+', '*'),
    #         ('+', 'i'),
    #         ('+', '('),
    #         ('*', 'i'),
    #         ('*', '('),
    #         ('(', '+'),
    #         ('(', '*'),
    #         ('(', 'i'),
    #         ('(', '('),
    #         ('$', '+'),
    #         ('$', '*'),
    #         ('$', 'i'),
    #         ('$', '('),
    #     ],
    #     '>': [('i', '+'),
    #           ('i', '*'),
    #           ('i', '$'),
    #           ('i', ')'),
    #           ('+', '+'),
    #           ('+', ')'),
    #           ('+', '$'),
    #           ('*', '+'),
    #           ('*', '*'),
    #           ('*', ')'),
    #           ('*', '$'),
    #           (')', '+'),
    #           (')', '*'),
    #           (')', ')'),
    #           (')', '$'),
    #           ],
    #     '=': [('(', ')')]
    # }

    # simbolo_inicial = 'E'
    # simbolos_terminales = 'i+*$()'
    # simbolos_no_terminales = 'E'


    
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
    generador = asa(reglas, precedencias, simbolo_inicial,
                    simbolos_terminales, simbolos_no_terminales)

    print("Generador de analizadores sintacticos.\n Opciones:")
    print("\t* RULE <no-terminal> [<simbolo>]")
    print("\t* INIT <no-terminal>")
    print("\t* PREC <terminal> <op> <terminal>")
    print("\t* BUILD")
    print("\t* PARSE <string>")
    print("\t* EXIT")
    while True:
        try:

            entrada = input("#> ")

            entrada = entrada.strip()

            entrada_separada = entrada.split(' ')
            opcion = entrada_separada[0]

            if opcion == "RULE":
                generador.agregar_regla(
                    entrada_separada[1], entrada_separada[2:])
            elif opcion == "INIT":
                generador.set_inicial(entrada_separada[1])
            elif opcion == "PREC":
                generador.agregar_precedencia(*entrada_separada[1:4])
            elif opcion == "BUILD":
                generador.build()
            elif opcion == "PARSE":
                generador.parse(' '.join(entrada_separada[1:]))
            elif opcion == "STATS":
                generador.estadisticas()
            elif opcion == "EXIT":
                break
            else:
                raise Exception(f"Opción '{opcion}' no reconocida")

        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
