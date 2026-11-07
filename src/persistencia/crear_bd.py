from persistencia.conexion import abrir_conexion, obtener_motor


def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    # 1. Tabla departamento
    if obtener_motor() == "sqlite":
        sql = """
        CREATE TABLE IF NOT EXISTS departamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            gerente TEXT
        );
        """
    else:
        sql = """
        CREATE TABLE IF NOT EXISTS departamento (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            gerente VARCHAR(100)
        );
        """
    cursor.execute(sql)

    # 2. Tabla empleado (Se corrigió AUTO_INCREMENT)
    if obtener_motor() == "sqlite":
        sql = """
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
        """
    else:
        sql = """
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
        """
    cursor.execute(sql)

    # 3. Tabla proyecto
    if obtener_motor() == "sqlite":
        sql = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT
        );
        """
    else:
        sql = """
        CREATE TABLE IF NOT EXISTS proyecto (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            descripcion VARCHAR(160),
            fecha_inicio DATE
        );
        """
    cursor.execute(sql)

    # 4. Tabla registro_tiempo
    if obtener_motor() == "sqlite":
        sql = """
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
        """
    else:
        sql = """
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
        """
    cursor.execute(sql)

    # 5. Tabla usuario
    if obtener_motor() == "sqlite":
        sql = """
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            empleado_id INTEGER NOT NULL UNIQUE,
            rol TEXT NOT NULL DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado')),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        );
        """
    else:
        sql = """
        CREATE TABLE IF NOT EXISTS usuario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
            contrasena VARCHAR(255) NOT NULL,
            empleado_id INT NOT NULL UNIQUE,
            rol ENUM('admin', 'empleado') NOT NULL DEFAULT 'empleado',
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        );
        """
    cursor.execute(sql)

    # 6. Tabla indicador_api
    if obtener_motor() == "sqlite":
        sql = """
        CREATE TABLE IF NOT EXISTS indicador_api (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuente TEXT NOT NULL,
            codigo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            valor REAL NOT NULL,
            unidad TEXT NOT NULL,
            verificado_en TEXT,
            UNIQUE (fuente, codigo, fecha)
        );
        """
    else:
        sql = """
        CREATE TABLE IF NOT EXISTS indicador_api (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fuente VARCHAR(50) NOT NULL,
            codigo VARCHAR(50) NOT NULL,
            fecha VARCHAR(50) NOT NULL,
            valor DECIMAL(10, 4) NOT NULL,
            unidad VARCHAR(20) NOT NULL,
            verificado_en VARCHAR(50),
            UNIQUE (fuente, codigo, fecha)
        );
        """
    cursor.execute(sql)

    # 7. Tabla de rompimiento: empleado_proyecto (Relación N:M)
    if obtener_motor() == "sqlite":
        sql = """
        CREATE TABLE IF NOT EXISTS empleado_proyecto (
            empleado_id INTEGER NOT NULL,
            proyecto_id INTEGER NOT NULL,
            fecha_asignacion TEXT DEFAULT CURRENT_TIMESTAMP,
            rol_en_proyecto TEXT,
            PRIMARY KEY (empleado_id, proyecto_id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
        );
        """
    else:
        sql = """
        CREATE TABLE IF NOT EXISTS empleado_proyecto (
            empleado_id INT NOT NULL,
            proyecto_id INT NOT NULL,
            fecha_asignacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            rol_en_proyecto VARCHAR(100),
            PRIMARY KEY (empleado_id, proyecto_id),
            FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id) ON DELETE CASCADE
        );
        """
    cursor.execute(sql)

    conexion.commit()
    conexion.close()