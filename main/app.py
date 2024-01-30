from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

class GenealogiaDB:
    def __init__(self, db_path="genealogia.db"):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS individuos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            madre_id INTEGER,
            padre_id INTEGER,
            FOREIGN KEY (madre_id) REFERENCES individuos (id),
            FOREIGN KEY (padre_id) REFERENCES individuos (id)
        );
        """
        with self.connection:
            self.connection.execute(query)

    def agregar_individuo(self, nombre, madre_id=None, padre_id=None):
        query = "INSERT INTO individuos (nombre, madre_id, padre_id) VALUES (?, ?, ?);"
        with self.connection:
            self.connection.execute(query, (nombre, madre_id, padre_id))
            self.connection.commit()

    def obtener_ancestros(self, individuo_id):
        query = """
        WITH RECURSIVE ancestros AS (
            SELECT id, nombre, madre_id, padre_id FROM individuos WHERE id = ?
            UNION
            SELECT i.id, i.nombre, i.madre_id, i.padre_id FROM individuos i
            JOIN ancestros a ON i.id = a.madre_id OR i.id = a.padre_id
        )
        SELECT * FROM ancestros;
        """
        with self.connection:
            result = self.connection.execute(query, (individuo_id,))
            return result.fetchall()

genealogia_db = GenealogiaDB()

@app.route('/agregar_individuo', methods=['GET', 'POST'])
def agregar_individuo():
    if request.method == 'POST':
        data = request.form
        nombre = data.get('nombre')
        madre_id = data.get('madre_id') or None
        padre_id = data.get('padre_id') or None
        
        genealogia_db.agregar_individuo(nombre, madre_id, padre_id)
        return jsonify({"mensaje": "Individuo agregado correctamente"}), 201
    return render_template('agregar_individuo.html')

@app.route('/calcular_probabilidad', methods=['GET', 'POST'])
def calcular_probabilidad_pariente():
    if request.method == 'POST':
        individuo1_id = request.form.get('individuo1_id', type=int)
        individuo2_id = request.form.get('individuo2_id', type=int)
        
        # Aquí iría la lógica para calcular la probabilidad...
        # Y luego rediriges o muestras el resultado como prefieras

    return render_template('calcular_probabilidad.html')

if __name__ == "__main__":
    app.run(debug=True)
