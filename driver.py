"""
========================================================================
|| Seminario del Módulo de Métodos Estadísticos
|| "Factorización de enteros: algoritmos y aplicación en criptografía"
|| Autor:  Erik Alberto Ríos Mena
|| Asesor: Dr. Abel Palafox González
========================================================================
"""

import rsa
import factoring
import datetime
import timeit
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pgf as pgf
from matplotlib import cycler
from sympy import sieve, ntheory, li

if __name__ == '__main__':
    # Código general de las gráficas.
    plt.close("all")
    colors = cycler("color",["#187f69","#8fe51f","#bf304f",
                            "#f4bf2d","#1563a6","#17ecff",
                            "w","#2EA183","#36ACB2"])
    plt.rc("axes", facecolor='#999999', edgecolor="none",
            titlecolor="w", labelcolor="w", axisbelow=True,
            grid=True, prop_cycle=colors)
    plt.rc("figure", facecolor="#333333")
    plt.rc("figure.subplot", top=0.92, bottom=0.121,
            left=0.084, right=0.982, hspace=0.2, wspace=0.2)
    plt.rc("grid", color="#DDDDDD", linestyle="solid")
    plt.rc("xtick", direction="out", color="#DDDDDD", labelcolor="w")
    plt.rc("ytick", direction="out", color="#DDDDDD", labelcolor="w")
    plt.rc("legend", facecolor="#555555", labelcolor="w")
    plt.rc("lines", linewidth=1, markersize=0.5)
    plt.rc("pgf", rcfonts=False,
    preamble=r"""\usepackage{amsmath}
                \usepackage{fontspec}
                \usepackage{notomath}
                \setmainfont{Segoe UI}
                \setmonofont{Consolas}""")

    # t_1=[]
    # exp=330
    # n=2**2
    # while n<2**(exp+1):
    #     timer=timeit.Timer(f'rsa.generate_prime({int(math.log(n,2))},base=2)','import rsa')
    #     t=timer.repeat(20,20)
    #     t=[i/20 for i in t]
    #     t_1.append(min(t))
    #     n*=2
    # fig = plt.figure(0,figsize=(8,4.5))
    # plt.plot([i for i in range(2,exp+1)],t_1,'o-')
    # plt.show()
    # exit()

    # Verificación de primalidad (división tentativa y prueba de Miller-Rabin)
    x=np.linspace(1,128,10000)
    fig = plt.figure(0,figsize=(8,4.5))
    plt.loglog(x,10*(x**3),label=r'Operaciones por bit (pruebas aleatorias aplicadas 10 veces)',linestyle='--')
    plt.loglog(x,100*(x**3),label=r'Operaciones por bit (pruebas aleatorias aplicadas 100 veces)',linestyle='--')
    plt.loglog(x,1000*(x**3),label=r'Operaciones por bit (pruebas aleatorias aplicadas 1000 veces)',linestyle='--',color='#2df497')
    plt.loglog(x,2**x,label=r'Operaciones por bit (división por tentativa sin mejora)',linestyle=':',color='#1563a6')
    plt.loglog(x,2**(x/2),label=r'Operaciones por bit (división por tentativa con mejora)',linestyle=':',color='#17ecff')
    plt.loglog(x,x**6,label=r'Operaciones por bit (prueba AKS optimizada)',color='#ffee00')
    plt.xscale('log', base=2)
    plt.yscale('log', base=2)
    plt.title(r'Operaciones por bits de las pruebas de primalidad aleatorias contra la AKS.           ')
    plt.xlabel('Dígitos en el entero a verificar primalidad')
    plt.ylabel('Número de operaciones')
    plt.legend()
    pgf.FigureCanvasPgf(fig).print_pgf("o_pruebas_rand_aks.pgf")
    plt.close("all")

    t_1=[]
    t_2=[]
    exp=15
    worst=[i for i in sieve.primerange(2**exp)]
    for n in worst:
        x,o=factoring.prueba_tentativa(n)
        t_1.append(o)
        x,o=factoring.prueba_tentativa2(n)
        t_2.append(o)
    x=np.linspace(2.,2**exp,10000)
    fig = plt.figure(0,figsize=(8,4.5))
    plt.plot(worst,t_1,label=r'Operaciones por número (división por tentativa desde $2$ hasta $n$)')
    plt.plot(x,x,label=r'$n$')
    plt.title(r'Operaciones en el peor caso ($n$ primo) del algoritmo de división por tentativa básico.            ')
    plt.xlabel('Entero a verificar primalidad')
    plt.ylabel('Número de operaciones')
    plt.legend()
    # plt.show()
    pgf.FigureCanvasPgf(fig).print_pgf("o_prueba_tentativa.pgf")
    plt.close("all")

    t_1=[]
    t_2=[]
    t_3=[]
    exp=4
    worst=[i for i in sieve.primerange(2**exp)]
    for n in worst:
        x,o=factoring.prueba_tentativa(n)
        t_1.append(o)
        x,o=factoring.prueba_tentativa2(n)
        t_2.append(o)
    x=np.linspace(2.,2**exp,10000)
    fig = plt.figure(0,figsize=(8,4.5))
    plt.plot(worst,t_1,label=r'Operaciones por número (división por tentativa desde $2$ hasta $n$)')
    plt.plot(x,x,label=r'$n$')
    plt.plot(worst,t_2,label=r'Operaciones por número (división por tentativa desde $2$ hasta $\sqrt{n}$)')
    plt.plot(x,np.sqrt(x),label=r'$\sqrt{n}$')
    plt.title(r'Operaciones en el peor caso ($n$ primo) del algoritmo de división por tentativa con y sin mejora.        ')
    plt.xlabel('Entero a verificar primalidad')
    plt.ylabel('Número de operaciones')
    plt.legend()
    # plt.show()
    pgf.FigureCanvasPgf(fig).print_pgf("o_prueba_tentativa_mejorado.pgf")
    plt.close("all")

    #e=d=p=q=0
    #p,q,n,e,d=rsa.generate_keys(p=[522233,613337],e=73)
    #print(f"La clave pública es: ({n}, {e})\nLa clave privada es: {d}\nLos factores primos son ({p}, {q})")
    #message="Hola tú."
    #print(f"Para el mensaje ``{message}´´:\nEl valor decimal es: {int(format(message.encode('utf-8').hex()),16)}")
    #cyphertext=rsa.raw_encrypt(message,e,n)
    #print(f"Una vez cifrado, el valor de nuestro mensaje es: {cyphertext}")
    #print(f"Decriptando, nuestro texto cifrado es: {rsa.raw_decrypt(cyphertext,d,n)}")
    #while((e*d)%((p-1)*(q-1))!=1):
    #    p,q,n,e,d=rsa.generate_keys(digits=25)
    #    print(p,q,'\n')
    #    print(n,'\n')
    #    print(e,d,'\n')
    #    print((e*d)%((p-1)*(q-1)),'\n')
    #print(encrypted_message)
    #
    #print(message.hex())
    p=175
    print(f"es muy probable que {p} sea primo" if factoring.miller_rabin(p,10) else f"{p} no es primo")
    #print(rsa.generate_prime(10,3))
    #n=int(input("Inserte el entero a factorizar: "))

    # al chile esto me lo robé de timeit.py
    units={"nanosegundos":1e-9,"microsegundos":1e-6,"milisegundos":1e-3,"segundos":1.0,"minutos":60.0}
    precision=3
    number=1
    repeat=1
    def format_time(dt):
        scales = [(scale, unit) for unit, scale in units.items()]
        scales.sort(reverse=True)
        for scale, unit in scales:
            if dt >= scale:
                break
        return "%.*g %s" % (precision, dt / scale, unit)
    n=int(input("Inserte el entero a verificar: "))
    print(f"{n} {'sí' if factoring.prueba_tentativa2(n) else 'no'} es primo")
    timer=timeit.Timer(f'factoring.prueba_tentativa2({n})','import factoring')
    raw_timings=timer.repeat(repeat, number)
    timings = [dt / number for dt in raw_timings]
    print("Tras %d %s, el mejor de %d fue: %s por bucle" % (number, 'bucles' if number != 1 else 'bucle', repeat, format_time(min(timings))))

    t_1=[]
    t_2=[]
    t_3=[]
    exp=17
    worst=[i for i in sieve.primerange(2**exp)]
    for n in worst:
        x,o=factoring.division_tentativa2(n)
        t_1.append(o)
        x,o=factoring.division_tentativa3(n)
        t_2.append(o)
        x,o=factoring.division_tentativa_criba(n)
        t_3.append(o)
        #timer=timeit.Timer(f'factoring.division_tentativa2({n})','import factoring')
        #raw_timings=timer.repeat(repeat, number)
        #timings = [dt / number for dt in raw_timings]
        #t_1.append(min(timings))
        #timer=timeit.Timer(f'factoring.division_tentativa({n})','import factoring')
        #raw_timings=timer.repeat(repeat, number)
        #timings = [dt / number for dt in raw_timings]
        #t_2.append(min(timings))
    #t_1.sort()
    #t_2.sort()
    #plt.plot(ran,t_1,'o',ran,t_2,'o')
    x=np.linspace(2.,2**exp,10000)
    fig = plt.figure(0,figsize=(8,4.5))
    plt.plot(worst,t_1,label=r'Operaciones por número (división por tentativa desde $2$ hasta $\sqrt{n}$)')
    plt.plot(x,np.sqrt(x),label=r'$\sqrt{n}$')
    plt.plot(worst,t_2,label=r'Operaciones por número (división entre $2$ y por tentativa sobre impares hasta $\sqrt{n}$)')
    plt.plot(x,np.sqrt(x)/2,label=r'$\frac{\sqrt{n}}{2}$')
    plt.plot(worst,t_3,label=r'Operaciones por número (división por tentativa sobre los primos hasta $\sqrt{n}$)')
    #plt.plot(x,[ntheory.primepi(np.sqrt(i)) for i in x],label=r'$\pi(\sqrt{n})$')
    plt.plot(x,[li(np.sqrt(i)) for i in x],label=r'$\pi(\sqrt{n})\approx\operatorname{li}(\sqrt{n})$')
    plt.title(r'Operaciones en el peor caso ($n$ primo) de los algoritmos de división por tentativa mejorados.            ')
    plt.xlabel('Entero a factorizar')
    plt.ylabel('Número de operaciones')
    plt.legend()
    #plt.show()
    pgf.FigureCanvasPgf(fig).print_pgf("o_division_tentativa.pgf")
    plt.close("all")
#    plt.savefig("test.png")



    #print("Tras %d %s, el mejor de %d fue: %s por bucle" % (number, 'bucles' if number != 1 else 'bucle', repeat, format_time(min(timings))))
    #ini=datetime.datetime.today()
    #print(f"Los factores de 13492928519 son: {factoring.division_tentativa(13492928519)}")
    #print(datetime.datetime.today()-ini)