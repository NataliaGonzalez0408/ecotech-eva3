from persistencia.conexion import abrir_conexion, obtener_motor

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    # Tabla departamento (Se eliminó la coma sobrante)
    if obtener_motor() == "sqlite":
        sql = '''
        CREATE TABLE IF NOT EXISTS departamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            gerente TEXT
        );
        '''
    else:
        sql = '''
        CREATE TABLE IF NOT EXISTS departamento (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            gerente VARCHAR(100)
        );
        '''
    cursor.execute(sql)

    # Tabla empleado
    if obtener_motor() == "sqlite":
        sql = '''
        CREATE TABLE IF NOT EXISTS empleado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            telefono TEXT,
            fecha_inicio_contrato TEXT,
            salario INTEGER,
            departamento_id INTEGER,
            FOREIGN KEY (departamento_id) REFERENCES departamento(id)
        );
        '''
    else:
        sql = '''
        CREATE TABLE IF NOT EXISTS empleado (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(150) NOT NULL UNIQUE,
            telefono VARCHAR(20),
            fecha_inicio_contrato DATE,
            salario DECIMAL(10, 2),
            departamento_id INT,
            FOREIGN KEY (departamento_id) REFERENCES departamento(id)
        );
        '''
    cursor.execute(sql)

    # Tabla proyecto (Se eliminó fecha_inicio duplicada)
    if obtener_motor() == "sqlite":
        sql = '''
        CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT
        );
        '''
    else:
        sql = '''
        CREATE TABLE IF NOT EXISTS proyecto (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            descripcion VARCHAR(160),
            fecha_inicio DATE
        );
        '''
    cursor.execute(sql)

    # Tabla registro_tiempo (Se corrigió sintaxis anidada y atributos según dominio)
    if obtener_motor() == "sqlite":
        sql = '''
        CREATE TABLE IF NOT EXISTS registro_tiempo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            cantidad_horas REAL,
            tareas_realizadas TEXT,
            descripcion TEXT,
            empleado_id INTEGER,
            proyecto_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        );
        '''
    else:
        sql = '''
        CREATE TABLE IF NOT EXISTS registro_tiempo (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fecha DATE,
            cantidad_horas DECIMAL(4, 2),
            tareas_realizadas VARCHAR(255),
            descripcion TEXT,
            empleado_id INT,
            proyecto_id INT,
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        );
        '''

        # tabla usuario
    if obtener_motor() == "sqlite":
        sql = '''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            empleado_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        );
        '''


    cursor.execute(sql)

    conexion.commit()
    conexion.close()