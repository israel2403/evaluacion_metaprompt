# Conversación ficticia — un solo chat

## I01 · Alumno
Escribe en Python 3 una función contar(a, objetivo) que cuente pares de índices i < j cuya suma sea objetivo. Recibe una lista de enteros y un entero y devuelve un entero. n <= 200000; necesitamos O(n) esperado, memoria O(n). Comprueba [1, 1, 1], objetivo 2: debe devolver 3.

## I01 · IA
Usa un diccionario de frecuencias para contar valores anteriores.
```python
def contar(a, objetivo):
    frecuencias = {}
    total = 0
    for x in a:
        total += frecuencias.get(objetivo - x, 0)
        frecuencias[x] = frecuencias.get(x, 0) + 1
    return total
```

## I02 · Alumno
Para la misma función, justifica por qué contar solo valores anteriores evita duplicar pares; verifica también la lista vacía, cuya salida esperada es 0. No generes código nuevo.

## I02 · IA
Cada par se cuenta al visitar su segundo índice. Para una lista vacía no se entra al ciclo y se devuelve 0. Con diccionarios, el tiempo esperado es O(n) y el espacio O(n).
