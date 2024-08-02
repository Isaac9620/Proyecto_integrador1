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

def get_db_connection():
    conn_str = f"DRIVER={db_config['DRIVER']};SERVER={db_config['SERVER']};DATABASE={db_config['DATABASE']};Trusted_Connection={db_config['Trusted_Connection']}"
    return pyodbc.connect(conn_str)

@app.route('/test_connection')
def test_connection():
    try:
        print("Intentando conectar a la base de datos...")  # Mensaje de depuración
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("Conexión exitosa a la base de datos")  # Mensaje de depuración
        return "Conexión exitosa a la base de datos"
    except pyodbc.Error as e:
        print(f"Error en la conexión a la base de datos: {e}")  # Mensaje de depuración
        return f"Error en la conexión a la base de datos: {e}"
    finally:
        conn.close()
        print("Conexión cerrada")  # Mensaje de depuración

if __name__ == '__main__':
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("Conexión exitosa a la base de datos al iniciar")
        conn.close()
    except pyodbc.Error as e:
        print(f"Error en la conexión a la base de datos al iniciar: {e}")
    
    app.run(debug=True)
