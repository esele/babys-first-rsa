"""
rsa.py - Implementación sencilla del sistema criptográfico RSA
---
Autor: Erik Alberto Ríos Mena

Incluye una implementación del cifrado de un mensaje w arbitrario
(UTF-8 o cualquier otro), métodos para generación de primos y pruebas
de primalidad probabilísticas (Miller-Rabin) en tiempo polinómico
"""

import random
import factoring
import numpy as np

def generate_prime(digits,n=1,base=10,trials=10):
    """
    generate_prime(digits,n=1,base=10,trials=10): Generación de números primos
    ---
    Entrada: digits es la cantidad de dígitos en los números a generar
             n es la cantidad de primos a generar (default:1)
             base es la representación posicional del número (default: decimal)
             trials es la cantidad de pruebas Miller-Rabin (default: 10)
    
    Salida:  un int (n=1) o array con los primos generados
    """

    p=[]
    for _ in range(n):
        while(True):
            # Generar un entero y probarlo con Miller-Rabin
            random.seed()
            cand=random.randrange(base**(digits-1)+1,base**digits,2)
            if factoring.miller_rabin(cand,trials)==True:
                # Es primo, guardarlo
                p.append(cand)
                break
    return cand if n==1 else p

def extended_euclidean_algorithm(a,b):
    """
    extended_euclidean_algorithm(a,b): Algoritmo de Euclides extendido para inverso modular
    ---
    Entrada: a y b son enteros coprimos, i.e. gcd(a,b)=1, para los cuales se van a
             calcular los coeficientes de Bézout
    
    Salida:  el coeficiente de Bézout t, positivo, que cumple a*t=1 mod b
    """

    r,r_prime=b,a
    t,t_prime=0,1
    # Este es el procedimiento de la división con residuo
    while(r_prime!=0):
        q=int(np.fix(r/r_prime))
        r,r_prime=r_prime,r-q*r_prime
        t,t_prime=t_prime,t-q*t_prime
    return t+b if t<0 else t

def generate_keys(p=[None,None],bits=512,base=2,e=None,e_bits=5,e_base=2,trials=10):
    """
    generate_keys(p=[None,None],bits=512,base=2,e=None,e_bits=7,e_base=2,trials=10): Generación de clave pública y privada RSA
    ---
    Entrada: p es un array de dos números primos (default: [None, None], i.e. generar ambos primos)
             bits es la cantidad de bits o dígitos en cada p (default: 512 bits)
             base es la representación posicional de cada p (default: 2, i.e. binaria)
             e es el exponente de encriptación (default: None, i.e. generarlo)
             e_bits es la cantidad de bits o dígitos en e (default: 7 bits)
             e_base es la representación posicional de e (default: 2, i.e. binaria)
             trials es la cantidad de pruebas Miller-Rabin (default: 10)

    Salida:  p[0] y p[1] son los factores del módulo RSA
             n:=p[0]*p[1] es el módulo RSA
             e es el exponente de encriptación
             d es el exponente de decriptación
    """

    # Generar a p de ser necesario
    random.seed()
    if p[0] is None or p[1] is None:
        p=generate_prime(bits,n=2,base=base,trials=trials)
    # Calcular la phi de Euler de p y q
    phi=(p[0]-1)*(p[1]-1)
    # Generar al exponente de encriptación de ser necesario
    if e is None:
        e=phi
        # Hay que cuidar que phi no divida a e
        while(phi%e==0):
            e=generate_prime(e_bits,base=e_base,trials=trials)
    # Calcular el exponente de decriptación
    d=extended_euclidean_algorithm(e,phi)
    return p[0],p[1],p[0]*p[1],e,d

def raw_encrypt(plaintext,e,n,encoding="utf8"):
    """
    raw_encrypt(plaintext,e,n,encoding="utf8"): Encriptación RSA básica
    ---
    Entrada: plaintext es una cadena de caracteres
             e es el exponente de encriptación
             n es el módulo RSA
             encoding es la codificiación de la cadena (default: UTF-8)
    
    Salida:  la representación decimal del mensaje encriptado.
    """
    # Convierte el texto plano a una cadena hexadecimal
    plaintext=plaintext.encode(encoding).hex()
    # - Convierte la representación hexadecimal a un entero decimal
    # - Calcula c=w^e mod n
    return pow(int(plaintext,16),e,n)

def raw_decrypt(cypher,d,n,encoding="utf8"):
    """
    raw_decrypt(plaintext,e,d,encoding="utf8"): Decriptación RSA básica
    ---
    Entrada: plaintext es una cadena de caracteres
             d es el exponente de decriptación
             n es el módulo RSA
             encoding es la codificiación de la cadena (default: UTF-8)
    
    Salida:  una cadena con el mensaje decriptado.
    """
    # - Convierte el texto cifrado en decimal a una representación hexadecimal
    # - Calcula w=c^d mod n
    # - Convierte de vuelta a una cadena
    return bytes.fromhex(format(pow(cypher,d,n),'x')).decode(encoding)

def try_decrypt(cypher,e,n,encoding="utf-8"):
    """
    try_decrypt(cypher,e,n,encoding="utf-8"): Intentar romper un módulo RSA
    ---
    Entrada: cypher es el texto cifrado
             e es el exponente de encriptación
             n es el módulo RSA

    Salida:  una cadena con el mensaje decriptado.
    """
    p,q=factoring.division_tentativa_sp(n)
    phi=(p-1)*(q-1)
    d=extended_euclidean_algorithm(e,phi)
    return raw_decrypt(cypher,d,n,encoding=encoding)
