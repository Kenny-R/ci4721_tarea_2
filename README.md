# Analizador Sintáctico

Este proyecto implementa un analizador sintáctico en Python.

## Instalación de dependencias

Para instalar las dependencias necesarias, asegúrate de tener `pip` instalado y ejecuta el siguiente comando:

```sh
pip install -r requirements.txt
```
## Ejecución del programa

Para ejecutar el programa principal, utiliza el siguiente comando:

```sh
python main.py
```

## Uso del programa
El programa principal ofrece varias opciones interactivas:

`RULE <no-terminal> [<simbolo>]`: Agrega una regla a la gramática.

`INIT <no-terminal>`: Establece el símbolo inicial de la gramática.

`PREC <terminal> <op> <terminal>`: Agrega una precedencia entre terminales.

`BUILD`: Construye el analizador sintáctico.

`PARSE <string>`: Parsea una cadena de entrada.

`EXIT`: Sale del programa.

## Ejecución de pruebas

Para ejecutar las pruebas unitarias, utiliza el siguiente comando:

```sh
pytest
```

## Revisión de cobertura

Para revisar la cobertura de las pruebas, utiliza el siguiente comando:

```sh
pytest --cov=analizador_sintactico --cov-report=html
```

El reporte HTML se generará en el directorio htmlcov. Puedes abrir el archivo htmlcov/index.html en tu navegador para ver el reporte de cobertura.

# Estructura del proyecto

```
analizador_sintactico/
    __init__.py
    analizador.py
    tests/
        __init__.py
        test_analizador.py
main.py
README.md
requirements.txt
```