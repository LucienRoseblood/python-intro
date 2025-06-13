import random
import math


lista_a = []
for x in range(8):
    # do listy lista_a jest dodany element o pseudolosowej wartości float między 2 a 10
    # https://docs.python.org/3/library/random.html
    lista_a.append(random.randrange(2, 10))
print("lista_a: " + str(lista_a))

lista_b = []
for x in range(7):
    try:
        # do listy lista_a jest dodany element o pseudolosowej wartości int włącznie między -2 a 2
        # https://docs.python.org/3/library/random.html
        lista_b.append(10/random.randint(-2, 2))
    # w przypadku w linii 16 wystąpi ZeroDivisionError, do listy_b zostanie zamiast tego dodane 30.
    except ZeroDivisionError:
        lista_b.append(30)
print("lista_b: " + str(lista_b))

# połączenie elementów z lista_a i lista_b w tuple. Zip zwraca iterator, więc w celu użycia go wielokrotnie jest on zamieniany w listę.
# https://docs.python.org/3.3/library/functions.html#zip
lista_c = list(zip(lista_a, lista_b))
print("zip(lista_a, lista_b): " + str(lista_c))

# posortowanie elementów z lista_c
# https://docs.python.org/3.3/library/functions.html#sorted
lista_d = sorted(lista_c)
print("sorted zip(lista_a, lista_b): " + str(lista_d))

lista_e = []
for x in lista_d:
    # podniesienie pierwszego elementu każdej tupli w lista_e z użyciem math.sqrt(x) do 3 potęgi
    # https://docs.python.org/3/library/math.html#math.pow
    lista_e.append(math.pow(x[0], 3))
print("lista_e: " + str(lista_e))