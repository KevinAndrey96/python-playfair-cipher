# Cifrado Polialfabético de Playfair (Matriz 5x5) en Python

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Supported-013243.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Implementación interactiva en Python del **Cifrado de Playfair** para pares de letras (digramas) mediante matrices bidimensionales de $5 \times 5$ con **NumPy**. El proyecto contempla la construcción dinámica de la matriz clave a partir de palabras secretas, el formateo y relleno de digramas con caracteres de escape (`X`), y la aplicación de las tres reglas clásicas de sustitución geométrica.

---

## 🔐 Fundamento Histórico y Teórico

Inventado en 1854 por el científico británico **Charles Wheatstone** pero popularizado y adoptado por **Lord Playfair**, fue el primer sistema práctico de cifrado por sustitución digrámica (cifra pares de letras simultáneamente en lugar de letras individuales).

Al cifrar digramas, la distribución de frecuencias de los caracteres individuales queda fuertemente enmascarada (pasando de un espacio de 26 letras a uno de $25 \times 25 = 600$ posibles digramas), lo que dificulta significativamente el criptoanálisis de frecuencia monoalfabético.

### 1. Construcción de la Matriz de Clave ($5 \times 5$)

1. Se utiliza una matriz de $5 \times 5$ que aloja 25 letras.
2. Tradicionalmente, se combinan las letras **I** y **J** en una misma celda (o se omite la **J**, reemplazándola por **I**).
3. Se escribe la palabra clave eliminando letras duplicadas.
4. Las casillas vacías restantes se completan en orden alfabético con las letras restantes que no aparecieron en la clave.

```text
Ejemplo con la clave "MONARCHY":
M   O   N   A   R
C   H   Y   B   D
E   F   G   I/J K
L   P   Q   S   T
U   V   W   X   Z
```

### 2. Preparación del Texto Claro (Reglas de Digramas)

1. El texto se limpia de espacios y signos de puntuación y se convierte a mayúsculas.
2. Si un par contiene dos letras idénticas consecutivas (por ejemplo, `LL`), se inserta una letra de relleno (típicamente `X`: `LX L...`).
3. Si la longitud total del texto es impar, se añade una `X` final para completar el último digrama.

### 3. Reglas Geométricas de Cifrado

Para cada par de letras $(A, B)$ ubicadas en las posiciones $(r_1, c_1)$ y $(r_2, c_2)$:

| Caso Geométrico | Regla de Cifrado | Regla de Descifrado |
| :--- | :--- | :--- |
| **Misma Fila** ($r_1 = r_2$) | Se reemplaza cada letra por la que está inmediatamente a su **derecha** (con retorno circular al inicio: $(c+1) \pmod 5$). | Se desplaza una posición a la **izquierda** ($(c-1) \pmod 5$). |
| **Misma Columna** ($c_1 = c_2$) | Se reemplaza cada letra por la que está inmediatamente **debajo** (con retorno circular: $(r+1) \pmod 5$). | Se desplaza una posición hacia **arriba** ($(r-1) \pmod 5$). |
| **Rectángulo** ($r_1 \ne r_2, c_1 \ne c_2$) | Cada letra se reemplaza por la que está en su **misma fila**, pero en la **columna de la otra letra**: $(r_1, c_2)$ y $(r_2, c_1)$. | Idéntica regla geométrica sobre las columnas cruzadas. |

---

## 📂 Estructura del Repositorio

```text
playfair/
├── main.py          # Script interactivo de consola para cifrar y descifrar
└── Video URL.txt    # Enlace a demostracion multimedia en YouTube
```

---

## 🚀 Requisitos e Instalación

### Prerrequisitos

- **Python** (versión 3.8 o superior).
- Biblioteca **NumPy**.

### Instalación de Dependencias

```bash
pip install numpy
```

---

## 💻 Guía de Uso

Ejecuta el script desde tu terminal:

```bash
python main.py
```

### 1. Cifrado

1. Selecciona la opción `1`.
2. Introduce el texto a cifrar (las letras se convierten automáticamente a mayúsculas y las letras repetidas adyacentes se separan).
3. Introduce la palabra clave secreta.
4. El script generará la matriz $5 \times 5$, mostrará la separación en digramas y generará el texto cifrado final.

### 2. Descifrado

1. Selecciona la opción `2`.
2. Introduce el criptograma.
3. Introduce la misma clave.
4. El script revertirá las reglas geométricas y reconstruirá el mensaje original.

---

## 📹 Demostración en Video

Demostración práctica del funcionamiento paso a paso en YouTube:
[Demostración en YouTube](https://youtu.be/GqfD58_vW8A)

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.
