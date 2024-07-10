from flask import flash, session
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash,  check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'GomitaRoja'

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'D57422910Ei.',
    'database': 'proyecto_integrador'
}

def registro(username, email, password):
    cuenta = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    datos= (username, email, password)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(cuenta, datos)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Por favor, introduce ambos el correo electrónico y la contraseña')
            return redirect(url_for('login'))

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Inicio de sesión exitoso')
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template ('InicioSesion.html')
    
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
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            sql_registro = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql_registro, (username, email, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
        
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            flash('Error en el registro. Inténtalo de nuevo.')
            return redirect(url_for('registro_view'))
    
    return render_template('Registro.html')


@app.route('/signup')
def signup():
    return render_template('Registro.html')

@app.route('/sectorambiental')
def SectorA():
    return render_template('SectorAmbientalIndex.html')

@app.route('/sectorsalud')
def SectorS():
    return render_template('SectorSaludIndex.html')


if __name__ == '__main__':
    app.run(debug=True)
