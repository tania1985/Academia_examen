from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, template_folder='templates')  # Asegúrate de que Flask busque en la carpeta 'templates'
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Configuración de la base de datos MySQL
db_config = {
    'host': 'localhost',  # Cambia esto si tu servidor MySQL está en otro host
    'user': 'root',       # Tu usuario MySQL
    'password': '',       # Tu contraseña MySQL
    'database': 'academia'
}

# Función para obtener la conexión a la base de datos
def obtener_conexion():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

@app.route('/')
def index():
    print("Ruta / accedida")
    return render_template('index.html')

@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
    print("Ruta /alumnos accedida")
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = int(request.form['edad'])
        print(f"Datos recibidos: nombre={nombre}, edad={edad}")  # Línea de depuración
        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO alumnos (nombre, edad)
                    VALUES (%s, %s)
                ''', (nombre, edad))
                conn.commit()
                flash('Alumno registrado exitosamente', 'success')
            except Error as e:
                print(f"Error al insertar alumno: {e}")
                flash('Error al registrar alumno', 'danger')
            finally:
                conn.close()
        return redirect(url_for('alumnos'))

    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM alumnos')
            alumnos = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener alumnos: {e}")
            alumnos = []
        finally:
            conn.close()
    else:
        alumnos = []
    return render_template('alumnos.html', alumnos=alumnos)

@app.route('/asignaturas', methods=['GET', 'POST'])
def asignaturas():
    print("Ruta /asignaturas accedida")
    if request.method == 'POST':
        nombre = request.form['nombre']
        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO asignaturas (nombre)
                    VALUES (%s)
                ''', (nombre,))
                conn.commit()
                flash('Asignatura registrada exitosamente', 'success')
            except Error as e:
                print(f"Error al insertar asignatura: {e}")
                flash('Error al registrar asignatura', 'danger')
            finally:
                conn.close()
        return redirect(url_for('asignaturas'))

    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM asignaturas')
            asignaturas = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener asignaturas: {e}")
            asignaturas = []
        finally:
            conn.close()
    else:
        asignaturas = []
    return render_template('asignaturas.html', asignaturas=asignaturas)

@app.route('/calificaciones', methods=['GET', 'POST'])
def calificaciones():
    print("Ruta /calificaciones accedida")
    if request.method == 'POST':
        alumno_id = int(request.form['alumno_id'])
        asignatura_id = int(request.form['asignatura_id'])
        calificacion = float(request.form['calificacion'])
        conn = obtener_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO calificaciones (alumno_id, asignatura_id, calificacion)
                    VALUES (%s, %s, %s)
                ''', (alumno_id, asignatura_id, calificacion))
                conn.commit()
                flash('Calificación registrada exitosamente', 'success')
            except Error as e:
                print(f"Error al insertar calificación: {e}")
                flash('Error al registrar calificación', 'danger')
            finally:
                conn.close()
        return redirect(url_for('calificaciones'))

    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM calificaciones')
            calificaciones = cursor.fetchall()
            cursor.execute('SELECT * FROM alumnos')
            alumnos = cursor.fetchall()
            cursor.execute('SELECT * FROM asignaturas')
            asignaturas = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener datos: {e}")
            calificaciones = []
            alumnos = []
            asignaturas = []
        finally:
            conn.close()
    else:
        calificaciones = []
        alumnos = []
        asignaturas = []
    return render_template('calificaciones.html', calificaciones=calificaciones, alumnos=alumnos, asignaturas=asignaturas)

if __name__ == '__main__':
    print("Iniciando la aplicación Flask")
    app.run(debug=True)
