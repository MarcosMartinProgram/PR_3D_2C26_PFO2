import os
import sqlite3
from flask import Flask, request, jsonify, render_template_string, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_por_defecto_desarrollo")

# Configurar CORS permitiendo credenciales (cookies de sesión)
CORS(app, supports_credentials=True, origins=["*"])

DB_NAME = os.getenv("DB_NAME", "gestion_tareas.db")

# --- Configuración y migración de base de datos ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- Endpoints ---

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Formato JSON inválido o body vacío"}), 400

    usuario = data.get("usuario")
    contrasena = data.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Debe enviar 'usuario' y 'contraseña'"}), 400

    # Hasheo seguro usando werkzeug (genera hash aleatorio con salt)
    hash_clave = generate_password_hash(contrasena)

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
            (usuario.strip(), hash_clave)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado con éxito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Formato JSON inválido o body vacío"}), 400

    usuario = data.get("usuario")
    contrasena = data.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"error": "Debe enviar 'usuario' y 'contraseña'"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario.strip(),))
    user = cursor.fetchone()
    conn.close()

    # Verificación del hash con la contraseña ingresada
    if user and check_password_hash(user["contrasena_hash"], contrasena):
        session["usuario"] = user["usuario"]
        return jsonify({
            "mensaje": f"Bienvenido/a {user['usuario']}. Inicio de sesión exitoso.",
            "usuario": user["usuario"]
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


@app.route('/tareas', methods=['GET'])
def tareas():
    if "usuario" not in session:
        return jsonify({"error": "Acceso denegado. Debe iniciar sesión primero."}), 401

    html_bienvenida = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Panel de Tareas</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; margin: 0; padding: 2rem; display: flex; justify-content: center; align-items: center; min-height: 100vh; box-sizing: border-box; }
            .card { background: #ffffff; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); padding: 2.5rem; text-align: center; max-width: 480px; width: 100%; }
            h1 { color: #0f172a; margin-top: 0; font-size: 1.5rem; }
            p { color: #64748b; line-height: 1.5; }
            .badge { display: inline-block; padding: 0.35rem 0.75rem; border-radius: 9999px; background: #dcfce7; color: #15803d; font-weight: 600; font-size: 0.85rem; margin-top: 1rem; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Bienvenido/a al Sistema de Tareas!</h1>
            <p>Sesión activa para el usuario: <strong>{{ usuario }}</strong></p>
            <div class="badge">Autenticación Verificada en SQLite</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_bienvenida, usuario=session["usuario"]), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.pop("usuario", None)
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200


if __name__ == '__main__':
    puerto = int(os.getenv("FLASK_PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=puerto, debug=debug_mode)