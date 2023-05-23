import numbers
from sympy import Matrix, init_printing, symbols, expand, linsolve
from division_sintetica import division_sintetica

init_printing()


class ExcepcionMatrizNoEsCuadrada(Exception):
    pass


class ExcepcionMatrizNoNumerica(Exception):
    pass


class MatrizCuadrada(Matrix):
    # Método constructor de mi clase MatrizCuadrada
    def __new__(cls, *args, **kwargs):

        # si la matriz tiene contenido se verifica que sea cuadrada, de lo contrario se valida dado a
        # que una matriz con 0 filas y 0 columnas, se sigue considerando cuadrada.
        if args:
            # verifica si todos los elementos de la matriz son números y no letras u otras cosas.
            for columnas_de_la_fila in args[0]:
                if not all([isinstance(valores, numbers.Number) for valores in columnas_de_la_fila]):
                    raise ExcepcionMatrizNoNumerica("")

            """matriz = Matrix(args[0])
            if not matriz.is_square:
                raise ExcepcionMatrizNoEsCuadrada("")"""

        return super().__new__(cls, *args, **kwargs)

    def metodo_estrella(self):
        primera_mitad = (self[0] * self[4] * self[-1]) + (self[-2] * self[3] * self[2]) + (self[1] * self[5] * self[-3])
        segunda_mitad = - (self[2] * self[4] * self[-3]) - (self[3] * self[1] * self[-1]) - (
                self[-2] * self[-4] * self[0])
        return primera_mitad + segunda_mitad
        pass

    def determinante_de_2x2(self):
        return (self[0] * self[-1]) - (self[1] * self[-2])

    def identidad(self):
        matriz_identidad = self.copy()
        poner_unos = True
        i_mas_nxn = 0

        for i in range(len(matriz_identidad)):

            if poner_unos:
                matriz_identidad[i] = 1
                i_mas_nxn = i + matriz_identidad.rows
                poner_unos = False
            else:
                matriz_identidad[i] = 0
                if i == i_mas_nxn:
                    poner_unos = True

        return matriz_identidad

    def determinante(self):

        match self.rows:
            case 1:
                return self
            case 2:
                return self.determinante_de_2x2()
            case 3:
                return self.metodo_estrella()
            case _:
                return self.det()

    def polinomio_caracteristico(self):
        lamda = symbols("lamda")
        lambda_por_identidad = lamda * self.identidad()
        polinomio_caracteristico = MatrizCuadrada.determinante(self - lambda_por_identidad)

        polinomio_caracteristico = expand(polinomio_caracteristico).as_poly(lamda)
        return polinomio_caracteristico

    def valores_propios(self):
        coeficientes = self.polinomio_caracteristico().coeffs()

        if coeficientes[0] < 0:
            coeficientes = [numeros * -1 for numeros in coeficientes]

        return division_sintetica(coeficientes)

    def vectores_propios(self):
        valores_y_vectores_propios = {}

        variables_fijas = symbols('x y z w u v j')

        incognitas_del_sistema = [variables_fijas[i] for i in range(self.rows)]

        valores_propios = (valores for valores in self.valores_propios())

        igualado_a_ceros = Matrix([0 for i in range(self.rows)])

        for valor_propio in valores_propios:
            sistema = self - (self.identidad() * valor_propio)
            solucion_del_sistema = linsolve((sistema, igualado_a_ceros), incognitas_del_sistema)

            for i in range(len(incognitas_del_sistema)):
                soluciones = list(solucion_del_sistema)
                valores_y_vectores_propios.setdefault(valor_propio, soluciones[0])

        return valores_y_vectores_propios
