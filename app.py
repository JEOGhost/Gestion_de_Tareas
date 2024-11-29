from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Inicializador de la base de datos
@app.route('/initdb')
def init_db():
    try:
        connection = sqlite3.connect('tareas.db')  # Conecta a la base de datos
        cursor = connection.cursor()

        # Se crea la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start_date TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
        return "Base de datos inicializada."
    except Exception as e:
        return f"Error al inicializar: {e}"

@app.route('/')
def index():
    return "Tenemos base de datos."

if __name__ == '__main__':
    app.run(debug=True)
