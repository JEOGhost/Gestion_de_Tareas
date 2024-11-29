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

@app.route('/', methods=['POST'])
def add_task():
    # Recoger datos
    title = request.form['title']
    start_date = request.form['start_date']
    status = 'Pendiente'  # Estado inicial por default

    # Insertar nueva tarea
    conn = get_connection()
    conn.execute('INSERT INTO tareas (title, start_date, status) VALUES (?, ?, ?)',
                 (title, start_date, status))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = get_connection()

    if request.method == 'POST':
        # POST: actualiza los datos
        title = request.form['title']
        start_date = request.form['start_date']
        status = request.form['status']
        conn.execute('UPDATE tareas SET title = ?, start_date = ?, status = ? WHERE id = ?',
                     (title, start_date, status, task_id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        # GET: obtiene los datos para mostrar
        task = conn.execute('SELECT * FROM tareas WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return render_template('editar.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # Eliminar tarea de la base de datos
    conn = get_connection()
    conn.execute('DELETE FROM tareas WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
