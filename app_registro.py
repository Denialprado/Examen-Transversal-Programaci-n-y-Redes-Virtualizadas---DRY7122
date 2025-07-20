import sqlite3
import hashlib
from flask import Flask, request

app = Flask(__name__)
db_name = 'database.db' 

@app.route('/')
def index():
    return 'Bienvenido al servidor de registro manual.'

@app.route('/signup/v2', methods=['POST'])
def signup_v2():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS USER_HASH (
            USERNAME TEXT PRIMARY KEY NOT NULL, 
            HASH TEXT NOT NULL
        );
    ''')
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        # Se usan '?' para prevenir inyección SQL
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) VALUES (?, ?)", 
                  (request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ya ha sido registrado."
    finally:
        conn.close()
    return "Registro exitoso."

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Se usan '?' para prevenir inyección SQL
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = ?"
    c.execute(query, (username,))
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login/v2', methods=['POST'])
def login_v2():
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            return 'Inicio de sesión exitoso'
        else:
            return 'Usuario/contraseña inválidos'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, ssl_context='adhoc')