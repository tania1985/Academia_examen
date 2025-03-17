import mysql.connector

def conectar_db():
    return mysql.connector.connect(
        host="localhost",   # Cambia si tu servidor no es local
        user="root",        # Usuario de MySQL
        password="",        # Contraseña de MySQL (déjala vacía si no tiene)
        database="academia" # Base de datos en phpMyAdmin
    )
