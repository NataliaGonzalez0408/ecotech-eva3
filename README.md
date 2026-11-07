# EcoTech Solutions — Sistema de Gestión Interna

## Descripción del Proyecto

**EcoTech Solutions** es una aplicación desarrollada en Python para la gestión integral de personal, departamentos, proyectos y registros de tiempo de trabajo. El sistema implementa una arquitectura por capas basada en patrones **DAO (Data Access Object)**, servicios de negocio, validaciones y sanitización estricta de datos. Cuenta con una autenticación segura de usuarios (`bcrypt`) y un soporte de persistencia tanto para **SQLite** como para **MySQL/MariaDB**.

Antes de poder ejecutar la aplicación, hay que asegurarse de contar con:

1. Python 3.10 o superior instalado.
2. Git instalado en el sistema.
3. Entorno virtual activo y dependencias instaladas.

## Instalación y Configuración

Hay que seguir estos pasos desde la terminal que tengas, ya sea el Git Bash o la Consola de tu dispositivo:

### 1. Clonar el repositorio 

- git clone (https://github.com/NataliaGonzalez0408/ecotech-eva3.git)
- cd ecotech-eva3

### 2. Creamos el entorno virtual, y luego se activa.

- python -m venv venv
- source venv/Scripts/activate 

### 3. Instalar dependencias del proyecto
- pip install --upgrade pip
- pip install -r requirements.txt

Luego, para abrir el codigo, se deberia de colocar:

- code .

### Ejecucion del Sistema

Ya realizado la clonación del repositorio, la creacion y activacion del entorno virtual y las dependencias instaladas, se deberia de iniciar la aplicacion:

- python main.py

La población de datos gracias a la semilla se hara automaticamente iniciada la aplicacion, y para poder probar el repositorio, debes de iniciar sesion.

### Datos Sesión

Para probarlo como admin, se deberá de iniciar de la siguiente manera:

- Usuario: jmartinez
- Contraseña: Admin123*

Y con eso, tendrás libertad para revisar el proyecto con el mayor rol posible.
