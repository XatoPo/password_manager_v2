# login.py: Este archivo contiene la implementación de una ventana de login usando PyQt5

import sys  # Importa el módulo sys para manejar argumentos y salida del sistema
import subprocess  # Importa el módulo subprocess para ejecutar comandos del sistema
import re  # Importa el módulo re para manejar expresiones regulares
from PyQt5.QtCore import Qt  # Importa Qt para manejar configuraciones de la ventana
from PyQt5.QtGui import QPixmap, QIcon  # Importa QPixmap y QIcon para manejar imágenes y íconos
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QMainWindow  # Importa los widgets de PyQt5

class LoginWindow(QWidget):  # Clase que define la ventana de login
    def __init__(self):
        super().__init__()  # Llama al constructor de la clase base QWidget
        self.init_ui()  # Inicializa la interfaz de usuario
    
    def init_ui(self):
        self.setWindowTitle('Login')  # Establece el título de la ventana
        self.setGeometry(100, 100, 200, 200)  # Configura el tamaño y posición de la ventana

        self.setWindowIcon(QIcon('../password_manager_v2/gui/Chimbo.png'))  # Establece el ícono de la ventana

        self.setStyleSheet("background-color: lightblue;")  # Establece el estilo CSS para la ventana

        layout = QVBoxLayout()  # Crea un layout vertical para organizar los widgets

        # Cargar la imagen desde un archivo
        pixmap = QPixmap('../password_manager_v2/gui/wing.png')
        if pixmap.isNull():
            print("Error al cargar la imagen")
        self.logo_label = QLabel(self)  # Crea un QLabel para mostrar la imagen
        self.logo_label.setPixmap(pixmap)
        layout.addWidget(self.logo_label)

        self.email_input = QLineEdit(self)  # Crea un QLineEdit para ingresar el email
        self.email_input.setPlaceholderText('Email')  # Establece un texto de marcador de posición
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)  # Crea un QLineEdit para ingresar la contraseña
        self.password_input.setPlaceholderText('Password')  # Establece un texto de marcador de posición
        self.password_input.setEchoMode(QLineEdit.Password)  # Configura el modo de eco para ocultar la contraseña
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)  # Crea un botón de login
        self.login_button.setStyleSheet("background-color: white; color: black;")  # Establece el estilo CSS del botón
        self.login_button.clicked.connect(self.login)  # Conecta el clic del botón a la función login
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register', self)  # Crea un botón de registro
        self.register_button.setStyleSheet("background-color: white; color: black;")  # Establece el estilo CSS del botón
        self.register_button.clicked.connect(self.register)  # Conecta el clic del botón a la función register
        layout.addWidget(self.register_button)

        self.setLayout(layout)  # Establece el layout para la ventana
    
    def validate_password(self, password):
        # Función para validar la contraseña
        if len(password) < 8:
            return False, 'La contraseña debe tener al menos 8 caracteres.'
        if not re.search(r'\d', password):
            return False, 'La contraseña debe tener al menos un número.'
        if not re.search(r'[A-Z]', password):
            return False, 'La contraseña debe tener al menos una letra mayúscula.'
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, 'La contraseña debe tener al menos un carácter especial.'
        return True, ''
    
    def register(self):
        # Función para manejar el registro
        email = self.email_input.text()  # Obtiene el texto ingresado en el campo de email
        password = self.password_input.text()  # Obtiene el texto ingresado en el campo de contraseña

        if not email or not password:
            QMessageBox.warning(self, 'Input Error', 'Please enter both email and password.')  # Muestra una advertencia si los campos están vacíos
            return
        
        is_valid, message = self.validate_password(password)  # Valida la contraseña
        if not is_valid:
            QMessageBox.warning(self, 'Password Error', message)  # Muestra un mensaje de error si la contraseña no es válida
            return

        try:
            process = subprocess.Popen(['../password_manager_v2/encryptor/encryptor'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(input=password.encode())  # Ejecuta el encriptador y obtiene el resultado
            encrypted_password = stdout.decode().strip()
            
            with open('passwords.txt', 'a') as f:
                f.write(f'{email}:{encrypted_password}\n')  # Guarda el email y la contraseña encriptada en un archivo

            QMessageBox.information(self, 'Success', 'Password has been encrypted and saved.')  # Muestra un mensaje de éxito
            
            self.email_input.clear()  # Limpia los campos de entrada
            self.password_input.clear()
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Encryption executable not found.')  # Muestra un mensaje de error si no se encuentra el encriptador

    def login(self):
        # Función para manejar el login
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, 'Input Error', 'Please enter both email and password.')  # Muestra una advertencia si los campos están vacíos
            return

        try:
            with open('passwords.txt', 'r') as f:
                credentials = f.readlines()  # Lee las credenciales guardadas
            
            for credential in credentials:
                saved_email, encrypted_password = credential.strip().split(':')  # Divide la línea en email y contraseña encriptada
                if email == saved_email:
                    process = subprocess.Popen(['../password_manager_v2/decryptor/decryptor'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate(input=encrypted_password.encode())  # Desencripta la contraseña guardada
                    decrypted_password = stdout.decode().strip()

                    # Añadir depuración para verificar las contraseñas
                    print(f"Decrypted password: {decrypted_password}")
                    print(f"Entered password: {password}")

                    if password == decrypted_password:
                        self.open_logged_in_window(email, decrypted_password)  # Abre la ventana de sesión iniciada si la contraseña coincide
                        return
            
            QMessageBox.warning(self, 'Login Error', 'Invalid email or password.')  # Muestra un mensaje de error si el email o la contraseña no coinciden
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'File not found.')  # Muestra un mensaje de error si no se encuentra el archivo de contraseñas
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))  # Muestra cualquier otro error que ocurra
            
    def open_logged_in_window(self, email, decrypted_password):
        # Función para abrir la ventana de sesión iniciada
        self.logged_in_window = QMainWindow()
        self.logged_in_window.setWindowTitle('Sesión Iniciada')
        self.logged_in_window.setGeometry(300, 300, 250, 150)

        self.logged_in_window.setStyleSheet("background-color: lightblue;")  # Aplica el mismo estilo CSS

        central_widget = QWidget()
        self.logged_in_window.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        label = QLabel(f'¡Sesión iniciada para {email}!')
        layout.addWidget(label)

        self.button_show_passwords = QPushButton('Mostrar Contraseña')
        self.button_show_passwords.setStyleSheet("background-color: white; color: black;")
        self.button_show_passwords.clicked.connect(lambda: self.show_password(email, decrypted_password))
        layout.addWidget(self.button_show_passwords)

        central_widget.setLayout(layout)

        self.logged_in_window.show()
        self.close()  # Cierra la ventana de login después de iniciar sesión

    def show_password(self, email, decrypted_password):
        # Función para mostrar la contraseña
        msg_box = QMessageBox(self.logged_in_window)
        msg_box.setStyleSheet("background-color: lightblue;")
        msg_box.setWindowTitle('Password')
        msg_box.setText(f'La contraseña para {email} es: {decrypted_password}')
        msg_box.exec_()

app = QApplication(sys.argv)  # Crea la aplicación PyQt
window = LoginWindow()  # Crea una instancia de la ventana de login
window.show()  # Muestra la ventana
sys.exit(app.exec_())  # Ejecuta la aplicación