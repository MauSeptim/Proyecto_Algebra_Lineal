import hashlib
import re
import sqlite3 as sql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# Creación de la clase donde residirá el GUI (Graphic User Interface)
class Gui(QMainWindow):
    def __init__(self, parent=None, *args):
        super(Gui, self).__init__(parent=parent)

        # configuración de la ventana
        self.setMinimumSize(1300, 600)
        self.setMaximumSize(1600, 950)
        self.setWindowTitle("Proyecto inacabado")

        # Conectar nuestra base de datos en sqlite3 con nuestro archivo PyQt5
        self.con = sql.connect('Data.db')
        self.c = self.con.cursor()

        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        # Creación del QWidget()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Input del email
        self.input_email = QLineEdit(self.central_widget)
        self.input_email.setPlaceholderText("Ingresa tu email")
        self.input_email.setClearButtonEnabled(True)

        # Input de la contraseña
        self.password = QLineEdit(self.central_widget)
        self.password.setPlaceholderText("Contraseña")
        self.password.setClearButtonEnabled(True)
        self.password.setEchoMode(QLineEdit.Password)

        # Boton para desencadenar los eventos
        self.login = QPushButton("Login", self.central_widget)

        # Label que aparecerá para comunicar al usuario si su input fue válido o no
        self.notificacion = QLabel(self.central_widget)

        # Coordenadas
        self.notificacion.resize(self.frameGeometry().width(), self.notificacion.frameGeometry().height())
        self.input_email.move(0, 70)
        self.password.move(0, 130)
        self.login.move(0, 190)

        # Conectar Señales
        self.login.clicked.connect(self.signIn)

    def signIn(self):
        email = self.input_email.text()
        password = hashlib.sha512(self.password.text().encode())

        # Expresión regular para determinar si la contraseña es válida o no usando expresiones regulares
        if email != '' and re.match('[^@]+@[^@]+\.[^@]+', email) and password != '':
            # ¡Contraseña generada correctamente!
            self.notificacion.setText("Login exitoso")
            self.c.execute(
                'INSERT INTO USUARIOS (Email, Password) VALUES ("{}", "{}")'.format(email, password.hexdigest())
            )
            self.con.commit()
            self.notificacion.setStyleSheet('background: green; color: white')
        else:
            self.notificacion.setStyleSheet('background: tomato; color: white')
            self.notificacion.setText("Login denegado | Revise su contraseña o email")
            # Contraseña denegada
            pass


if __name__ == '__main__':
    app = QApplication([])
    window = Gui()
    window.show()
    app.exec_()
