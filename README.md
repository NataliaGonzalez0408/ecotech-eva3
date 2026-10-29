# ecotech-eva3

coTech Solutions

Descripción del proyecto

EcoTech Solutions es un proyecto desarrollado en Python para gestionar información de empleados, departamentos, proyectos y registros de tiempo. Su objetivo es organizar la información y facilitar las operaciones mediante el uso de clases, DAO y una conexión a una base de datos.

Tecnologías utilizadas

Python SQLite MySQL Git y GitHub

Requisitos

Antes de ejecutar el proyecto, se necesita tener instalado:

Python Git Las dependencias indicadas en requirements.txt

Instalación y ejecución

Pasos para lograr instalar este repositorio (En Git Bach):

1.- Clonar el repositorio desde Git Bash:

git clone URL_DEL_REPOSITORIO

2.- Ingresar a la carpeta del proyecto:

cd Ecotech_grupal

3.- Crear el entorno virtual de Python:

python -m venv .venv

4.- Activar el entorno virtual:

source .venv/Scripts/activate

5.- Instalar las dependencias necesarias:

pip install -r requirements.txt

Configurar la base de datos
El proyecto permite utilizar SQLite o MySQL mediante el archivo de conexión. Se deben configurar las variables de entorno necesarias según el motor seleccionado, utilizando los datos correspondientes al entorno de ejecución.

Ejecutar el programa
Una vez configuradas las dependencias y la base de datos, ejecutar el archivo principal del proyecto desde la terminal.

El comando exacto debe ajustarse al nombre y la ubicación reales de dicho archivo.

Estructura general

src/dominio/: contiene las clases principales del sistema.

src/persistencia/: contiene los archivos de conexión y acceso a datos (DAO).

requirements.txt: contiene las dependencias de Python.

README.md: contiene la información y las instrucciones del proyecto.

Autores

Proyecto desarrollado en equipo para EcoTech Solutions.s