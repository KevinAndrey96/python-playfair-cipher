# Cifrado Playfair en Python

[![CI](https://github.com/KevinAndrey96/python-playfair-cipher/actions/workflows/ci.yml/badge.svg)](https://github.com/KevinAndrey96/python-playfair-cipher/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-3776AB)
![Cobertura](https://img.shields.io/badge/cobertura-100%25-brightgreen)
![mypy](https://img.shields.io/badge/mypy-strict-2A6DB2)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-yellow.svg)](LICENSE)

Implementación tipada y probada del **cifrado Playfair**, la sustitución por dígrafos que Charles Wheatstone inventó en 1854 y que el ejército británico usó hasta la Primera Guerra Mundial. Construye el cuadrado de 5 x 5 a partir de una clave, cifra y descifra por pares de letras, valida que un criptograma sea posible y ofrece una interfaz de línea de comandos.

## Contenido

- [Cómo funciona](#cómo-funciona)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Historia del proyecto](#historia-del-proyecto)

## Cómo funciona

**El cuadrado.** Se escriben las letras de la clave sin repetir y luego el resto del alfabeto; la I y la J comparten casilla. Con la clave `Yoan Pinzon`, la del ejemplo original de 2020:

```text
Y O A N P
I Z B C D
E F G H K
L M Q R S
T U V W X
```

**Los dígrafos.** El texto se normaliza (mayúsculas, sin tildes, J como I) y se divide en pares. Un par nunca repite letra: entre letras dobles se inserta una X (una Q si la letra doble es X), y una letra final suelta se completa igual. `THIS SECRET MESSAGE IS ENCRYPTED` queda como

```text
TH IS SE CR ET ME SX SA GE IS EN CR YP TE DX
```

**La sustitución.** Para cada par:

| Posición de las dos letras | Al cifrar | Al descifrar |
| :--- | :--- | :--- |
| Misma fila | la letra de la derecha de cada una | la de la izquierda |
| Misma columna | la letra de abajo de cada una | la de arriba |
| Rectángulo | la esquina en su propia fila | igual, es su propia inversa |

Los bordes son circulares. El ejemplo anterior produce `WE DL LK HW LY LF XP QP HF DL HY HW OY YL KP`, el mismo resultado que documentaba el trabajo original, y el ejemplo de Wikipedia (`hide the gold in the tree stump` con la clave `playfair example`) produce `BMODZBXDNABEKUDMUIXMMOUVIF`.

Descifrar devuelve los dígrafos con sus rellenos. `remove_fillers` quita las X entre letras iguales y la final, pero no puede distinguir un relleno de una X auténtica en esas posiciones, así que su resultado es una sugerencia y no una inversa exacta.

## Uso

Requiere Python 3.12 o superior y [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run playfair square "Yoan Pinzon"
uv run playfair encrypt -k "Yoan Pinzon" --pairs "This secret message is encrypted"
# WE DL LK HW LY LF XP QP HF DL HY HW OY YL KP
uv run playfair decrypt -k "Yoan Pinzon" --strip-fillers "WE DL LK HW LY LF XP QP HF DL HY HW OY YL KP"
# THISSECRETMESSAGEISENCRYPTED
```

Si se omite el texto, se lee de la entrada estándar. Un criptograma con longitud impar, con J, con símbolos o con un par de letras iguales no puede venir de Playfair: el comando lo rechaza con código 2 y un mensaje en la salida de error.

Como librería:

```python
from playfair import KeySquare, decrypt, digraphs, encrypt, remove_fillers

KeySquare.from_key("Yoan Pinzon").rows()   # ['YOANP', 'IZBCD', 'EFGHK', 'LMQRS', 'TUVWX']
digraphs("balloon")                        # ['BA', 'LX', 'LO', 'ON']
cifrado = encrypt("instruments", "MONARCHY")
remove_fillers(decrypt(cifrado, "MONARCHY"))  # 'INSTRUMENTS'
```

## Arquitectura

```text
src/playfair/
  square.py   normalización y KeySquare inmutable con posiciones precalculadas
  cipher.py   dígrafos, sustitución, validación de criptogramas y rellenos
  cli.py      comandos encrypt, decrypt y square
```

El cuadrado indexa la posición de cada letra al construirse, así que cifrar es lineal en la longitud del texto. Sin dependencias externas; los criptogramas imposibles se reportan con `CiphertextError`, subclase de `ValueError`.

## Pruebas y calidad

```bash
uv run pytest --cov
uv run ruff check src tests && uv run ruff format --check src tests
uv run mypy
```

27 pruebas con cobertura del 100 % de líneas y ramas. Además de los vectores del trabajo original y de Wikipedia, las pruebas basadas en propiedades con Hypothesis verifican que cualquier clave produce una permutación de las 25 letras, que todo criptograma generado es válido y descifra a sus dígrafos, y que quitar los rellenos recupera exactamente cualquier texto sin X ni Q. El pipeline de GitHub Actions ejecuta Ruff y mypy en modo estricto, las pruebas en Python 3.12, 3.13 y 3.14, una prueba de humo del comando instalado y la construcción del paquete con `twine check`.

## Historia del proyecto

El proyecto nació en marzo de 2020 como un script interactivo para la clase de criptografía, con matrices de caracteres de NumPy y un [video explicativo](https://www.youtube.com/watch?v=MPUKMzf_PX4). Aquel script agregaba siempre un par `XX` al final, que viola la regla de no repetir letra en un dígrafo, y solo funcionaba por consola. En 2026 se reescribió como un paquete tipado sin dependencias, con la regla de rellenos corregida, validación de criptogramas, una interfaz de línea de comandos y pruebas automatizadas; además se eliminaron del historial el entorno virtual y los archivos del IDE que se habían versionado. El código original se conserva en el tag [`v0.1-python-coursework-2020`](https://github.com/KevinAndrey96/python-playfair-cipher/tree/v0.1-python-coursework-2020).

## Autor

**Kevin Andrey Herrera Silva** · [GitHub](https://github.com/KevinAndrey96)

## Licencia

Distribuido bajo la [licencia MIT](LICENSE).
