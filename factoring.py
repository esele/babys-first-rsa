import math
import random
from sympy import sieve

#=======================================
# Algoritmos para prueba de primalidad
#=======================================

def prueba_tentativa(n):
    """
    prueba_tentativa(n): Algoritmo de división por tentativa
    Entrada: un entero n
    Salida:  booleana (True si n es primo, False si es compuesto)
    """
    # Repetir hasta que i sea igual a n
    o=0
    for i in range(2,n):
        # Dividir n entre i, si no hay residuo regresar que es compuesto, de otro modo incrementar i
        if(n%i==0):
            return False,o
        o+=1
    return True,o

def prueba_tentativa2(n):
    """
    prueba_tentativa2(n): Algoritmo de división por tentativa mejorado
    Entrada: un entero n
    Salida:  booleana (True si n es primo, False si es compuesto)
    """
    # Repetir hasta que i sea igual a n
    o=0
    for i in range(2,round(math.sqrt(n))):
        # Dividir n entre i, si no hay residuo regresar que es compuesto, de otro modo incrementar i
        if(n%i==0):
            return False,o
        o+=1
    return True,o

def fermat_witness(n,witness):
    """
    fermat_witness(n,witness): Prueba de primalidad de Fermat con posible testigo
    Entrada: n es un entero que queremos verificar es primo
             witness es el testigo, i.e. un a tal que calculamos a^{n-1} mod n
    Salida:  booleana (True si n es pseudo-primo de Fermat base a, False si es compuesto)
    """
    return True if pow(witness,n-1,n)==1 else False

def fermat(n,trials):
    """
    fermat(n,trials): Prueba de primalidad de Fermat
    Entrada: n es un entero que queremos verificar es primo
             trials es la cantidad de veces que correr la prueba
    Salida:  booleana (True si n es, posiblemente, un número primo, False si es compuesto;
             la prueba siempre devuelve True si n es primo, aunque algunos compuestos
             también lo hacen).
    """
    if(n==2 or n==3):
        return True
    if(n%2==0):
        return False
    for _ in range(trials):
        random.seed()
        a=random.randint(2,n-2)
        if not fermat_witness(n,a):
            return False
    return True

def miller_rabin_witness(n,witness):
    """
    miller_rabin_witness(n,witness): Prueba de primalidad de Miller-Rabin con posible testigo
    Entrada: n es un entero que queremos verificar es primo
             witness es el testigo, i.e. un a al que se calculan las congruencias
             n=2^sd+1 ---> a^d mod n y a^{2^id} mod n, 0<=i<=s-1
    Salida:  booleana (True si n es pseudo-primo fuerte base a, False si es compuesto)
    """

    # Expresar a n=2^sd+1
    s=0
    d=n-1
    while(d%2==0):
        s+=1
        d//=2
    # Verificar las congruencias sin potencia de 2
    x=pow(witness,d,n)
    if(x!=1 and x!=n-1):
        for _ in range(s-1):
            # Verificar las congruencias con potencia de 2
            x=pow(x,2,n)
            if(x==n-1):
                break
        else:
            # Ninguna congruencia se cumple, regresar False
            return False
    # Alguna congruencia se cumple, n es pseudo-primo fuerte
    return True

def miller_rabin(n,trials):
    """
    miller_rabin(n,trials): Prueba de primalidad de Miller-Rabin
    Entrada: n es un entero que queremos verificar es primo
             trials es la cantidad de veces que correr la prueba
    Salida:  booleana (True si n es, posiblemente, un número primo, False si es compuesto;
             la prueba siempre devuelve True si n es primo, aunque algunos compuestos
             también lo hacen).
    """

    # Casos triviales
    if n==2 or n==3:
        return True
    if n%2==0:
        return False

    for _ in range(trials):
        # Genera un testigo a y corre la prueba para este
        random.seed()
        a=random.randint(2,n-2)
        # Finalizar con False si algún testigo fracasa
        if not miller_rabin_witness(n,a):
            return False
    # Todos los a probados son testigos
    return True

#==============================
# Algoritmos de factorización
#==============================

def division_tentativa(n):
    """
    division_tentativa(n): Algoritmo de división por tentativa
    Entrada: un entero n
    Salida:  un array con los factores de n
    """

    # Forma el array e inicia desde el número primo 2
    factores=[]
    i=2
    # Repetir hasta que n no sea unidad
    o=0
    while(n!=1):
        # Dividir n entre i si no hay residuo, de otro modo incrementar i
        if(n%i==0):
            n//=i
            factores.append(i)
        else:
            i+=1
        o+=1
    return factores,o

def division_tentativa2(n):
    """
    division_tentativa2(n): Algoritmo de división por tentativa mejorado
    Entrada: un entero n
    Salida:  un array con los factores de n
    """

    # Forma el array e inicia desde el número primo 2
    factores=[]
    i=2
    # Repetir hasta que n<=i^2:
    o=0
    while(n>i**2):
        # Dividir n entre i si no hay residuo, de otro modo incrementar i
        if(n%i==0):
            n//=i
            factores.append(i)
        else:
            i+=1
        o+=1
    # Añadir n a la lista si ni es unidad
    if n!=1:
        factores.append(n)
    return factores,o

def division_tentativa3(n):
    """
    division_tentativa3(n): Algoritmo de división por tentativa mejorado más
    Entrada: un entero n
    Salida:  un array con los factores de n
    """

    # Forma el array e inicia desde el número primo 2
    factores=[]
    # Repetir hasta que n<=i^2:
    o=0
    while(n%2==0):
        n//=2
        factores.append(2)
        o+=1
    i=3
    while(n>i**2):
        # Dividir n entre i si no hay residuo, de otro modo incrementar i
        if(n%i==0):
            n//=i
            factores.append(i)
        else:
            i+=2
        o+=1
    # Añadir n a la lista si ni es unidad
    if n!=1:
        factores.append(n) 
    return factores,o

def division_tentativa_criba(n):
    """
    division_tentativa_criba(n): Algoritmo de división por tentativa con criba de primos
    Entrada: un entero n
    Salida:  un array con los factores de n
    """

    factores=[]
	# Crea la criba de primos
    s=[i for i in sieve.primerange(math.sqrt(n))]
    o=0
	# Verifica para cada primo en la criba si éste es factor
    for i in s:
        while(n%i==0):
            n//=i
            factores.append(i)
            o+=1
    if n!=1:
        factores.append(n)
    return factores,o

def division_tentativa_sp(n):
    """
    division_tentativa_sp(n): Algoritmo de división por tentativa para semiprimos
    Entrada: un entero n
    Salida:  los factores de n
    """

    # Repetir hasta que n<=i^2:
    if(n%2==0):
        return 2,n//2
    i=3
    while(n>i**2):
        # Dividir n entre i si no hay residuo y terminar
        if(n%i==0):
            return i,n//i
        i+=1
    # n fue primo, después de todo
    return 1,n
