from flask import Flask, request, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

BASE_DATOS = "usuarios.db"

USUARIOS_INICIALES = [
    ("cristobal", "Cristóbal Cornejo", "Cristobal123"),
    ("jesus", "Jesus Muñoz", "Jesus123"),
    ("sebastian", "Sebastian Muñoz", "Sebastian123")
]


def conectar_bd():
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_base_datos():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            nombre_completo TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    for usuario, nombre_completo, password in USUARIOS_INICIALES:
        password_hash = generate_password_hash(password)

        cursor.execute("""
            INSERT OR IGNORE INTO usuarios
            (usuario, nombre_completo, password_hash)
            VALUES (?, ?, ?)
        """, (usuario, nombre_completo, password_hash))

    conexion.commit()
    conexion.close()


PAGINA_LOGIN = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Inicio de sesión DRY7122</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #eeeeee;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .contenedor {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            width: 350px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        }

        h2 {
            text-align: center;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            box-sizing: border-box;
        }

        button {
            width: 100%;
            padding: 10px;
            background-color: #222222;
            color: white;
            border: none;
            cursor: pointer;
        }

        .mensaje {
            margin-top: 15px;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Acceso integrantes DRY7122</h2>

        <form method="POST">
            <label>Usuario:</label>
            <input type="text" name="usuario" required>

            <label>Contraseña:</label>
            <input type="password" name="password" required>

            <button type="submit">Iniciar sesión</button>
        </form>

        {% if mensaje %}
            <div class="mensaje">{{ mensaje }}</div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "POST":
        usuario_ingresado = request.form["usuario"]
        password_ingresada = request.form["password"]

        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario_ingresado,)
        )

        usuario = cursor.fetchone()
        conexion.close()

        if usuario and check_password_hash(
            usuario["password_hash"],
            password_ingresada
        ):
            mensaje = (
                f"Inicio de sesión correcto. "
                f"Bienvenido, {usuario['nombre_completo']}."
            )
        else:
            mensaje = "Usuario o contraseña incorrectos."

    return render_template_string(PAGINA_LOGIN, mensaje=mensaje)


if __name__ == "__main__":
    crear_base_datos()
    app.run(host="0.0.0.0", port=5800, debug=True)

