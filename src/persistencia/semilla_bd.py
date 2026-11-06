from persistencia.crear_bd import abrir_conexion, obtener_motor
from dominio.usuario import Usuario
from servicios.autenticacion import crear_hash


def sembrar_datos():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    # 1. Verificar si la base de datos ya tiene datos
    cursor.execute("SELECT COUNT(*) FROM departamento;")
    if cursor.fetchone()[0] > 0:
        print("La base de datos ya contiene registros. Operación omitida.")
        conexion.close()
        return

    # Determinar el marcador de posición para consultas (%s o ?)
    motor = obtener_motor()
    ph = "?" if motor == "sqlite" else "%s"

    # 2. Insertar Departamentos
    departamentos = [
        ("Recursos Humanos", "Ana López"),
        ("Desarrollo de Software", "Carlos Pérez"),
        ("Marketing", "Laura Gómez"),
        ("Finanzas", "Javier Torres"),
        ("Operaciones", "Marta Sánchez")
    ]
    sql_dep = f"INSERT INTO departamento (nombre, gerente) VALUES ({ph}, {ph});"
    cursor.executemany(sql_dep, departamentos)

    # 3. Insertar Empleados
    empleados = [
        ("Juan Martínez", "juan.martinez@ecotech.com", "569-2221234", "2023-01-15", 500000, 1),
        ("María García", "maria.garcia@ecotech.com", "569-56786115", "2023-02-20", 550000, 2),
        ("Pedro Rodríguez", "pedro.rodriguez@ecotech.com", "569-9018842", "2023-03-10", 480000, 3),
        ("Ana López", "ana.lopez@ecotech.com", "569-3975456", "2023-04-05", 600000, 1),
        ("Carlos Pérez", "carlos.perez@ecotech.com", "569-7822690", "2023-05-12", 650000, 2),
        ("Laura Gómez", "laura.gomez@ecotech.com", "569-1111111", "2023-06-15", 580000, 3),
        ("Javier Torres", "javier.torres@ecotech.com", "569-2222222", "2023-07-20", 620000, 4),
        ("Marta Sánchez", "marta.sanchez@ecotech.com", "569-3333333", "2023-08-10", 520000, 5),
        ("Luis Fernández", "luis.fernandez@ecotech.com", "569-4444444", "2023-09-15", 540000, 1),
        ("Sofía Ramírez", "sofia.ramirez@ecotech.com", "569-5555555", "2023-10-20", 560000, 2),
        ("Diego Morales", "diego.morales@ecotech.com", "569-6666666", "2023-11-15", 590000, 3),
        ("Valentina Torres", "valentina.torres@ecotech.com", "569-7777777", "2023-12-01", 610000, 4),
        ("Andrés Castillo", "andres.castillo@ecotech.com", "569-8888888", "2023-12-15", 570000, 5),
        ("Camila Rojas", "camila.rojas@ecotech.com", "569-9999999", "2023-12-20", 530000, 1),
        ("Melissa Herrera", "melissa.herrera@ecotech.com", "569-0000000", "2023-12-25", 510000, 2),
        ("Fernando Vargas", "fernando.vargas@ecotech.com", "569-1111111", "2023-12-30", 550000, 3),
        ("Isabella Castro", "isabella.castro@ecotech.com", "569-2222222", "2023-12-31", 500000, 4),
        ("Sebastián Rojas", "sebastian.rojas@ecotech.com", "569-3333333", "2023-12-31", 520000, 5),
        ("Natalia Fuentes", "natalia.fuentes@ecotech.com", "569-4444444", "2023-12-31", 510000, 1),
        ("Matías Paredes", "matias.paredes@ecotech.com", "569-5555555", "2023-12-31", 500000, 2)
    ]
    sql_emp = f"INSERT INTO empleado (nombre, correo, telefono, fecha_inicio_contrato, salario, departamento_id) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph});"
    cursor.executemany(sql_emp, empleados)

    pass_hash = crear_hash("Admin123*")

    usuarios = [
        ("admin", pass_hash, 1, "admin"),
        ("mgarcia", pass_hash, 2, "admin"),
        ("prodriguez", pass_hash, 3, "empleado"),
        ("alopez", pass_hash, 4, "empleado"),
        ("cperez", pass_hash, 5, "empleado")
    ]
    sql_usr = f"INSERT INTO usuario (nombre_usuario, contrasena, empleado_id, rol) VALUES ({ph}, {ph}, {ph}, {ph});"
    cursor.executemany(sql_usr, usuarios)

    conexion.commit()
    conexion.close()
    print("Datos sembrados correctamente en la base de datos.")