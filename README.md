# Password Manager

Este proyecto es una herramienta para la encriptación y desencriptación de contraseñas usando Flex, Bison y OpenSSL. También incluye una interfaz gráfica hecha con PyQt5 para la gestión de contraseñas.

## Estructura del Proyecto

```bash
password_manager/
├── encryptor/
│   ├── lexer.l
│   ├── parser.y
│   └── encryption.c
├── decryptor/
│   ├── lexer.l
│   ├── parser.y
│   └── decryption.c
├── gui/
│   ├── login.py
│   ├── view_password.py
│   └── wing.png
└── passwords.txt
```

## Requisitos

- Flex
- Bison
- OpenSSL
- Python 3
- PyQt5

### Instalación de Flex y Bison

```bash
sudo apt install flex bison
```
### Instalación de Pyhton 3 en Ubuntu

1. **Actualizar el índice de paquetes:**
```bash
sudo apt update
```

2. **Instalación de Python 3:**
En Ubuntu, Python 3 generalmente ya está instalado. Sin embargo, para asegurarte de tener la última versión y configurarlo como `python3` de manera explícita, puedes ejecutar:
```bash
sudo apt install python3
```

3. **Verificar la instalación:**
Puedes verificar que Python 3 está correctamente instalado ejecutando:
```bash
python3 --version
```

### Instalación de PyQt5 en Ubuntu

1. **Instalación de pip3 (si no está instalado):**
`pip3` es el gestor de paquetes de Python 3. Asegúrate de tenerlo instalado con el siguiente comando:
```bash
sudo apt install python3-pip
```

2. **Instalación de PyQt5:**
Una vez que `pip3` está instalado, puedes instalar PyQt5 ejecutando:
```bash
sudo apt install python3-pyqt5
```
Este comando instalará tanto PyQt5 como sus dependencias necesarias.

3. **Verificar la instalación de PyQt5:**
Puedes verificar que PyQt5 se ha instalado correctamente ejecutando un pequeño script que importe PyQt5:
```bash
python3 -c "import PyQt5.QtCore; print('PyQt5 installed successfully')"
```

```bash
sudo apt install flex bison
```

### Verificación de la Instalación

```bash
flex --version
bison --version
```

## Compilación del Encriptador

```bash
cd ~/Escritorio/password_manager_v2/encryptor
flex lexer.l
bison -d parser.y
gcc -o encryptor lex.yy.c parser.tab.c encryption.c -lssl -lcrypto
```

## Compilación del Desencriptador

```bash
cd ~/Escritorio/password_manager_v2/decryptor
flex lexer.l
bison -d parser.y
gcc -o decryptor lex.yy.c parser.tab.c decryption.c -lssl -lcrypto
```

## Ejecutar las Interfaces Gráficas

```bash
python3 gui/login.py
python3 gui/view_password.py
```

## Pasos para Correr en WSL (Windows Subsystem for Linux)

### Instalación de Ubuntu

1. Dirigirse a la Microsoft Store.
2. Buscar "Ubuntu".
3. Seleccionar el botón de descargar y esperar la descarga.

### Permisos y Activación

Abrir una terminal de PowerShell e introducir los siguientes comandos:

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### Ejecutar la Aplicación

1. Ejecutar la aplicación de Ubuntu.
2. Crear un usuario y una contraseña.

### Configuración de la Ventana Virtual

1. Buscar en el navegador [VcXsrv](https:/*sourceforge.net/projects/vcxsrv/).
2. Descargar e instalar la aplicación.
3. Ejecutar el Launcher de VcXsrv.
4. Seleccionar "Multiple windows" y darle a siguiente.
5. Seleccionar "Start no client" y darle a siguiente.
6. Seleccionar todos los checkboxes, incluyendo "Disable access control" y darle a siguiente.
7. Finalmente, darle al botón "Finish".

### Dar Permisos a Encryptor y Decryptor

En la raíz de cada uno:

```bash
chmod +x decryptor
chmod +x encryptor
```

### Funcionalidad de la Ventana Virtual con localhost

```bash
export DISPLAY=localhost:0
```

## Descripción del Proyecto

Este proyecto consiste en un sistema de gestión de contraseñas que permite a los usuarios almacenar y recuperar contraseñas de manera segura. Utiliza Flex y Bison para la creación de analizadores léxicos y sintácticos, y OpenSSL para la encriptación y desencriptación de las contraseñas. La interfaz gráfica está desarrollada con PyQt5.

### login.py

Implementa una ventana de login con PyQt5. Permite al usuario ingresar un email y una contraseña para registrarse o iniciar sesión. La contraseña se valida para cumplir con ciertos criterios y se encripta antes de guardarse. Durante el login, la contraseña ingresada se compara con la desencriptada almacenada.

### view_password.py

Implementa una ventana para ver contraseñas con PyQt5. Permite al usuario ingresar un email y muestra la contraseña desencriptada correspondiente. La contraseña se desencripta utilizando un ejecutable externo.

### encryption.c y decryption.c

Estos archivos contienen la lógica de encriptación y desencriptación utilizando OpenSSL. La encriptación y desencriptación se realizan con el algoritmo AES-256-CBC, que es un estándar seguro y ampliamente utilizado.

#### encryption.c

- Crea un contexto de cifrado usando OpenSSL.
- Inicializa el contexto con el algoritmo AES-256-CBC.
- Realiza el cifrado de los datos de entrada.
- Finaliza el cifrado y libera el contexto.

#### decryption.c

- Crea un contexto de descifrado usando OpenSSL.
- Inicializa el contexto con el algoritmo AES-256-CBC.
- Realiza el descifrado de los datos de entrada.
- Finaliza el descifrado y libera el contexto.

### lexer.l y parser.y

Estos archivos definen los analizadores léxicos y sintácticos para el proceso de encriptación y desencriptación. Flex se utiliza para el análisis léxico y Bison para el análisis sintáctico. Estos analizadores toman el texto de entrada, lo tokenizan y lo procesan según las reglas definidas para encriptar o desencriptar contraseñas.

## Contribución

Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.