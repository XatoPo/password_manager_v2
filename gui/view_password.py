# view_password.py: Este archivo contiene la implementación de una ventana para ver contraseñas usando PyQt5

import sys  # Importa el módulo sys para manejar argumentos y salida del sistema
import subprocess  # Importa el módulo subprocess para ejecutar comandos del sistema
from PyQt5.QtGui import QIcon  # Importa QIcon para manejar íconos
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox  # Importa los widgets de PyQt5

class ViewPasswordWindow(QWidget):  # Clase que define la ventana para ver contraseñas
    def __init__(self):
        super().__init__()  # Llama al constructor de la clase base QWidget
        self.init_ui()  # Inicializa la interfaz de usuario
    
    def init_ui(self):
        self.setWindowTitle('View Password')  # Establece el título de la ventana
        layout = QVBoxLayout()  # Crea un layout vertical para organizar los widgets

        self.setWindowIcon(QIcon('../password_manager_v2/gui/Chimbo.png'))  # Establece el ícono de la ventana

        self.email_input = QLineEdit(self)  # Crea un QLineEdit para ingresar el email
        self.email_input.setPlaceholderText('Email')  # Establece un texto de marcador de posición
        layout.addWidget(self.email_input)

        self.view_button = QPushButton('View Password', self)  # Crea un botón para ver la contraseña
        self.view_button.clicked.connect(self.view_password)  # Conecta el clic del botón a la función view_password
        layout.addWidget(self.view_button)

        self.password_display = QLabel('Password:', self)  # Crea un QLabel para mostrar la contraseña
        layout.addWidget(self.password_display)

        self.setLayout(layout)  # Establece el layout para la ventana
    
    def view_password(self):
        # Función para ver la contraseña
        email = self.email_input.text()  # Obtiene el texto ingresado en el campo de email

        if not email:
            QMessageBox.warning(self, 'Input Error', 'Please enter an email.')  # Muestra una advertencia si el campo de email está vacío
            return

        try:
            with open('passwords.txt', 'r') as f:
                lines = f.readlines()  # Lee las credenciales guardadas
                for line in lines:
                    parts = line.strip().split(':', 1)  # Divide la línea en email y contraseña encriptada
                    if len(parts) == 2:
                        stored_email, encrypted_password = parts
                        if stored_email == email:
                            process = subprocess.Popen(['../password_manager_v2/decryptor/decryptor'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            stdout, stderr = process.communicate(input=encrypted_password.encode())  # Desencripta la contraseña guardada
                            decrypted_password = stdout.decode(errors='ignore').strip()
                            if not decrypted_password:
                                QMessageBox.warning(self, 'Decryption Error', 'Failed to decrypt the password.')  # Muestra un mensaje de error si la desencriptación falla
                            else:
                                self.password_display.setText(f'Password: {decrypted_password}')  # Muestra la contraseña desencriptada
                            return
                QMessageBox.warning(self, 'Not Found', 'No password found for this email.')  # Muestra un mensaje de advertencia si no se encuentra la contraseña
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Decryptor executable not found.')  # Muestra un mensaje de error si no se encuentra el desencriptador

app = QApplication(sys.argv)  # Crea la aplicación PyQt
window = ViewPasswordWindow()  # Crea una instancia de la ventana para ver contraseñas
window.show()  # Muestra la ventana
sys.exit(app.exec_())  # Ejecuta la aplicación