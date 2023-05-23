import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from valores_y_vectores_propios import *
from diseño_proyectoQTDesigner import *
import gc
import matplotlib.pyplot as plt
import sys

init_printing()


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        self.ui.superior.mouseMoveEvent = self.mover_ventana

        self.ui.btn_inicio.clicked.connect(lambda: self.ui.cambiarPagina.setCurrentWidget(self.ui.page))
        self.ui.btn_calculadora.clicked.connect(lambda: self.ui.cambiarPagina.setCurrentWidget(self.ui.page_2))
        self.ui.btn_sistema_dinamico.clicked.connect(lambda: self.ui.cambiarPagina.setCurrentWidget(self.ui.page_4))

        self.ui.btn_minimizar.clicked.connect(self.minimizar_ventana)
        self.ui.btn_maximizar.clicked.connect(self.maximizar_ventana)
        self.ui.btn_salir.clicked.connect(lambda: self.close())
        self.ui.btn_restaurar.clicked.connect(self.restaurar_ventana)

        self.ui.btn_restaurar.hide()

        self.ui.btn_menu.clicked.connect(self.mover_menu)

        self.ui.input_nxn_matriz.currentIndexChanged.connect(self.manejarBox)
        self.ui.calcular_vectores_propios.setVisible(False)
        self.ui.calcular_vectores_propios.clicked.connect(self.output_vectores_propios)
        self.ui.limpiarTabla.clicked.connect(self.limpiarTablaYresultados)

        self.lineEditValido = False
        self.poblacionBuhosValido = False

        self.ui.btn_mostrarGrafica.clicked.connect(self.mostrarGrafica)
        self.ui.lineEdit_ingresarAnios.textChanged.connect(self.LineEditEsValido)
        self.ui.tabla_poblacion_buhos.cellChanged.connect(self.TablaPoblacionEsValido)
        self.ui.btn_mostrarGrafica.hide()
        self.ui.btn_vaciarTablaBuhosProbablidades.clicked.connect(self.vaciarTabla)
        self.ui.btn_probabilidadesRandom.clicked.connect(self.generarConcentracionesAleatorias)

        self.ui.tabla_probabilidades_buhos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabla_probabilidades_buhos.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def TablaPoblacionEsValido(self):
        self.poblacionBuhosValido = True
        for i in range(self.ui.tabla_poblacion_buhos.columnCount()):
            if not self.ui.tabla_poblacion_buhos.item(0, i).text().isdigit() or int(
                    self.ui.tabla_poblacion_buhos.item(0, i).text()) == 0:
                self.poblacionBuhosValido = False
                break
        self.aparecerBoton()

    def LineEditEsValido(self):
        self.lineEditValido = self.ui.lineEdit_ingresarAnios.text().isdigit() and int(
            self.ui.lineEdit_ingresarAnios.text()) != 0
        self.aparecerBoton()

    def aparecerBoton(self):
        if self.lineEditValido and self.poblacionBuhosValido:
            self.ui.btn_mostrarGrafica.show()
        else:
            self.ui.btn_mostrarGrafica.hide()

    def generarConcentracionesAleatorias(self):
        import random
        for fila in range(3):
            for columna in range(3):
                probablidad = QTableWidgetItem(str(random.uniform(0, 1.01)))
                probablidad.setTextAlignment(Qt.AlignCenter)
                self.ui.tabla_probabilidades_buhos.setItem(fila, columna, probablidad)

    def vaciarTabla(self):

        for fila in range(3):
            for columna in range(3):
                cero = QTableWidgetItem('0')
                cero.setTextAlignment(Qt.AlignCenter)
                self.ui.tabla_probabilidades_buhos.setItem(fila, columna, cero)

    def mostrarGrafica(self):
        sistema_dinamico = np.zeros((3, 3))
        input_error = False

        for fila in range(3):
            if input_error:
                break
            for columna in range(3):
                if self.ui.tabla_probabilidades_buhos.item(fila, columna).text().isdigit():
                    if int(self.ui.tabla_probabilidades_buhos.item(fila, columna).text()) == 0:
                        sistema_dinamico[fila][columna] = int(
                            self.ui.tabla_probabilidades_buhos.item(fila, columna).text())
                        continue
                    else:
                        input_error = True
                        break
                else:
                    try:
                        celda = float(self.ui.tabla_probabilidades_buhos.item(fila, columna).text())
                    except ValueError:
                        input_error = True
                        break

                sistema_dinamico[fila][columna] = celda

        if input_error:
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText("Agrega solo numeros con punto decimal, representan los porcentajes")
            mensaje.addButton(QMessageBox.Ok)
            respuesta = mensaje.exec_()
        else:
            poblacion = np.zeros((1, 3))
            for i in range(self.ui.tabla_poblacion_buhos.rowCount()):
                poblacion[0][i] = int(self.ui.tabla_poblacion_buhos.item(0, i).text())

            n = int(self.ui.lineEdit_ingresarAnios.text())
            x = np.zeros((n + 1, 3))
            x[0, :] = poblacion

            for i in range(n):
                x[i + 1, :] = np.dot(sistema_dinamico, x[i, :])
                gc.collect()

            plt.rcParams.update({'font.size': 20})
            plt.figure(figsize=(30, 30))
            plt.plot(range(n + 1), x[:, 0], label='Juvenil')
            plt.plot(range(n + 1), x[:, 1], label='Subadulto')
            plt.plot(range(n + 1), x[:, 2], label='Adulto')
            plt.legend()
            plt.xlabel('Años')
            plt.ylabel('Número de hembras')
            plt.title('Sistema dinamico de poblacion')
            plt.get_current_fig_manager()
            plt.show()

    def limpiarTablaYresultados(self):
        nxn = self.ui.matriz_input.rowCount()
        for fila in range(nxn):
            for columna in range(nxn):
                item = QTableWidgetItem('0')
                self.ui.matriz_input.setItem(fila, columna, item)

        self.ui.lista_resultados.clear()

    def output_vectores_propios(self):
        self.ui.lista_resultados.clear()
        lista_cuadrada = []
        nxn = int(self.ui.input_nxn_matriz.currentText()[0])

        for fila in range(nxn):
            lista_cuadrada += [[]]
            for columna in range(nxn):
                celda = int(self.ui.matriz_input.item(fila, columna).text())
                lista_cuadrada[fila] += [celda]

        matriz = MatrizCuadrada(lista_cuadrada)
        vectores_propios_de_la_matriz = matriz.vectores_propios()
        lamda = "λ"
        indices = ["₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]

        if vectores_propios_de_la_matriz != {}:
            i = 0
            lamdas = []

            for valores_propios in vectores_propios_de_la_matriz.keys():
                valor_propio_en_lista = lamda + indices[i]
                lamdas.append(valor_propio_en_lista)
                self.ui.lista_resultados.addItems([valor_propio_en_lista + " = " + str(valores_propios)])
                i += 1

            for i, vectores_propios in enumerate(vectores_propios_de_la_matriz.values()):
                expresion = "V" + lamdas[i] + " = " + str(vectores_propios)
                self.ui.lista_resultados.addItems([expresion])
        else:
            self.ui.lista_resultados.addItems(["No se pudieron sacar sus valores propios"])

    def manejarBox(self):
        if not self.ui.calcular_vectores_propios.isVisible():
            self.ui.calcular_vectores_propios.setVisible(True)

        nxn = int(self.ui.input_nxn_matriz.currentText()[0])
        self.ui.matriz_input.setRowCount(nxn)
        self.ui.matriz_input.setColumnCount(nxn)
        if nxn == 1:
            self.ui.matriz_input.setItem(0, 0, QTableWidgetItem('0'))
        else:
            for filas in range(nxn):
                for columnas in range(nxn):
                    self.ui.matriz_input.setItem(filas, columnas, QTableWidgetItem('0'))

    def minimizar_ventana(self):
        self.showMinimized()

    def restaurar_ventana(self):
        self.showNormal()
        self.ui.btn_restaurar.hide()
        self.ui.btn_maximizar.show()

    def maximizar_ventana(self):
        self.showMaximized()
        self.ui.btn_maximizar.hide()
        self.ui.btn_restaurar.show()

    def mover_menu(self):
        width = self.ui.menu.width()
        normal = 0
        largo = self.frameGeometry().width()
        extender = largo / 3 if width == 0 else normal

        self.animacion = QPropertyAnimation(self.ui.menu, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animacion.start()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if not self.isMaximized():
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
