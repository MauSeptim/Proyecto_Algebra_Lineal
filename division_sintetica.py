def division_sintetica(lista: list):
    if len(lista) == 0:
        raise ValueError("el polinomio esta vacio")
    if all([isinstance(numeros, int) for numeros in lista]):
        raise ValueError("los elementos de la lista contienen valores no enteros")

    multiplicadores = []
    for i in [lista[-1], 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1 / 2, 3 / 2, 4 / 5, 3 / 5, 2 / 3, 1 / 4, 1 / 5]:
        if lista[-1] % i == 0:
            multiplicadores.append(i)
    multiplicadores.sort(reverse=True)
    valores_propios = []
    polinomio = lista.copy()
    polinomio_temporal = []
    stop = 0
    i = 0

    while len(polinomio) != 1:

        # si después de la última iteracion no se encontraron los valores propios se prueban los mismos
        # divisores, pero negativos y el contador en i se reinicia en 0
        if i == len(multiplicadores):
            if stop == 10:
                print("no se pudo sacar los valores")
                break
            i = 0
            multiplicadores = [divisores * -1 for divisores in multiplicadores]
            stop += 1

        # el divisor fijo es el factor por el que se multiplicaran a los valores del polinomio, y él
        divisor_fijo = multiplicadores[i]

        # al igual que en la division sintética, cuando se baja el primer número, se multiplica con el
        # divisor fijo y procede a sumar con el siguiente valor del polinomio, aquí automáticamente el
        # acomulador sintético hace la multiplicación para después hacer la suma en el for
        acomulador_sintetico = divisor_fijo * polinomio[0]

        # en la división sintética siempre se baja el primer número sin ningún cambio, entonces este
        # polinomio temporal lo hace de la misma manera guardando el primer número del polinomio
        polinomio_temporal.append(polinomio[0])

        # Aquí se hacen las sumas y multiplicaciones
        for j in range(1, len(polinomio)):

            # se hace la suma después de que el divisor fijo se multiplicara con el primer valor del polinomio
            acomulador_sintetico += polinomio[j]

            # después de que se baje el primer número del polinomio, todas las sumas se van almacenando en el nuevo
            # polinomio
            polinomio_temporal.append(acomulador_sintetico)

            # cuando estemos en la última iteracion si hubo residuo cero en la division sintética, se agrega la raiz,
            # osease, el valor de la división fija, y el polinomio original toma el valor de la temporal menos el último
            # valor, ya que el último valor es el residuo (0)
            if j == len(polinomio) - 1:
                if acomulador_sintetico == 0:
                    valores_propios.append(divisor_fijo)
                    polinomio = polinomio_temporal[:-1]

                break

            # mientras no sea la última iteracion, el acomulador sintético se multiplica con el divisor fijo para hacer
            # la suma del siguiente valor del polinomio en la siguiente iteración
            acomulador_sintetico *= divisor_fijo
        polinomio_temporal = []
        i += 1
    return valores_propios
