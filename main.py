from flask import flash, session, Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc

app = Flask(__name__)
app.secret_key = 'GomitaRoja'

# Configuración de la conexión a la base de datos SQL Server
db_config = {
'DRIVER': '{ODBC Driver 17 for SQL Server}',
    'SERVER': 'LAPTOPIR',
    'DATABASE': 'BetterAlliance_PI',
    'Trusted_Connection': 'yes'    
}

def registro(username, email, password, nombre, Ap, Am, edad, genero, fecha_nac):
    cuenta = "INSERT INTO Usuarios (Nombre_usuario, Correo, Contrasena) VALUES (?, ?, ?)"
    hashed_password = generate_password_hash(password)  # Hashear la contraseña
    datos = (username, email, hashed_password)
    cuenta2 = "INSERT INTO Personas (Nombre, Apellido_p, Apellido_m, Edad, genero_id, Fecha_nac) VALUES (?, ?, ?, ?, ?, ?)"
    datos2 = (nombre, Ap, Am, edad, genero, fecha_nac)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(cuenta, datos)
        cursor.execute(cuenta2, datos2)
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_generos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, Nombre FROM generos")
        generos = cursor.fetchall()
    except pyodbc.Error as e:
        print(f"Error al obtener los géneros: {e}")
        generos = []
    finally:
        cursor.close()
        conn.close()
    return generos

def get_db_connection():
    conn_str = f"DRIVER={db_config['DRIVER']};SERVER={db_config['SERVER']};DATABASE={db_config['DATABASE']};Trusted_Connection={db_config['Trusted_Connection']}"
    return pyodbc.connect(conn_str)

def actualizar_password(email, hashed_password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Usuarios SET Contrasena = ? WHERE Correo = ?", (hashed_password, email))
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error actualizando la contraseña: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print(f"Email ingresado: {email}, Password ingresado: {password}")  # Imprimir para depuración
        
        if not email or not password:
            flash('Por favor, introduce ambos el correo electrónico y la contraseña')
            return redirect(url_for('login'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE Correo = ?", (email,))
            user = cursor.fetchone()
            print(f"Usuario recuperado: {user}")  # Imprimir datos del usuario para depuración
        except pyodbc.Error as e:
            print(f"Error en la consulta SQL: {e}")
            user = None
        finally:
            cursor.close()
            conn.close()
        
        if user:
            username, stored_password = user  # Desempaquetar correctamente
            print(f"Contraseña almacenada: {stored_password}")  # Imprimir la contraseña almacenada
            
            # Verificar si la contraseña almacenada está hasheada
            if check_password_hash(stored_password, password):
                session['username'] = username  # Asegúrate de que el nombre de usuario está en la columna correcta
                password = check_password_hash(password)
                flash('Inicio de sesión exitoso')
                return redirect(url_for('dashboard'))
            else:
                flash('Contraseña incorrecta')
                print("Contraseña incorrecta")  # Depuración de contraseña incorrecta
        else:
            flash('Correo electrónico no encontrado')
            print("Correo electrónico no encontrado")  # Depuración de correo no encontrado
    
    return render_template('InicioSesion.html')

@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html')  # Renderiza la página de ajustes de DB si el usuario ha iniciado sesión
    else:
        return render_template('Home.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirigir a la página de inicio de sesión
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Elimina 'username' de la sesión
    flash('Has cerrado sesión con éxito.')
    return redirect(url_for('home'))

@app.route('/registro', methods=['GET', 'POST'])
def registro_view():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        Ap = request.form['Apellido_p']
        Am = request.form['Apellido_m']
        edad = request.form['Edad']
        genero = request.form['Genero']
        fecha_nac = request.form['Fecha_nac']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            registro(username, email, password, nombre, Ap, Am, edad, genero, fecha_nac)
            flash('Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
        
        except Exception as e:
            print(f"Error: {e}")
            flash('Error en el registro. Inténtalo de nuevo.')
            return redirect(url_for('registro_view'))
    generos = get_generos()
    return render_template('Registro.html', generos=generos)

@app.route('/signup')
def signup():
    return render_template('Registro.html')

@app.route('/sectorambiental')
def SectorA():
    return render_template('SectorAmbientalIndex.html')

@app.route('/sectorsalud')
def SectorS():
    return render_template('SectorSaludIndex.html')

@app.route('/tablas')
def tablas():
    if 'username' not in session:
        flash('Debe iniciar sesión primero')
        return redirect(url_for('login'))
    tablas = obtener_users()
    return render_template('Tablas.html', tablas=tablas)

if __name__ == '__main__':
    app.run(debug=True)
