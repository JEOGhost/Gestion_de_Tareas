from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Inicializador de la base de datos
def get_connection():
    conn = sqlite3.connect('tareas.db')
    conn.row_factory = sqlite3.Row  # Habilitar acceso por nombres de columnas
    return conn

# Crear la tabla de tareas si no existe
with get_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')

@app.route('/')
def index():
    # Conectar y obtener todas las tareas de la base de datos
    conn = get_connection()
    tasks = conn.execute('SELECT * FROM tareas').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
