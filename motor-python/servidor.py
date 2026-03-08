import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import wmi
import pythoncom # Necesario para usar WMI dentro del servidor web

app = Flask(__name__)
# Habilitamos CORS para que React (puerto 3000) pueda hablar con Python (puerto 8080)
CORS(app)

DB_PATH = "tienda_retrogeek.db"

def obtener_conexion():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

# --- 1. CATÁLOGO DE TIENDA ---
@app.route('/api/juegos', methods=['GET'])
def get_juegos_tienda():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM juegos")
        juegos = cursor.fetchall()
        
        cursor.execute("SELECT juego_id FROM biblioteca")
        owned_ids = [row['juego_id'] for row in cursor.fetchall()]
        
        conn.close()

        lista_final = []
        for j in juegos:
            juego_dict = dict(j)
            juego_dict['comprado'] = juego_dict['id'] in owned_ids
            lista_final.append(juego_dict)

        return jsonify(lista_final)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. OBTENER SOLO LA BIBLIOTECA DEL USUARIO ---
@app.route('/api/biblioteca', methods=['GET'])
def get_biblioteca():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        query = """
            SELECT juegos.*, biblioteca.fecha_adquisicion 
            FROM juegos 
            JOIN biblioteca ON juegos.id = biblioteca.juego_id
            ORDER BY biblioteca.fecha_adquisicion DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(row) for row in rows])
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. SIMULAR COMPRA / ADQUISICIÓN DE JUEGO ---
@app.route('/api/adquirir', methods=['POST'])
def adquirir_juego():
    data = request.json
    juego_id = data.get('juego_id')
    
    if not juego_id:
        return jsonify({"error": "No se proporcionó juego_id"}), 400

    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM juegos WHERE id = ?", (juego_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "Juego no encontrado en catálogo"}), 404
            
        cursor.execute("SELECT id FROM biblioteca WHERE juego_id = ?", (juego_id,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "El juego ya está en biblioteca"}), 400
            
        cursor.execute("INSERT INTO biblioteca (juego_id) VALUES (?)", (juego_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"mensaje": "Juego añadido a biblioteca con éxito", "juego_id": juego_id}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 4. DETALLE DE UN JUEGO (RESTAURADO AL 100%) ---
@app.route('/api/juegos/<int:juego_id>', methods=['GET'])
def get_detalle_juego(juego_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM juegos WHERE id = ?", (juego_id,))
    juego_row = cursor.fetchone()
    
    if juego_row is None:
        conn.close()
        return jsonify({"error": "Juego no encontrado"}), 404
        
    juego_data = dict(juego_row)
    
    # ESTAS SON LAS LÍNEAS QUE HABÍA RECORTADO (Requisitos y Reseñas)
    cursor.execute("SELECT * FROM requisitos WHERE juego_id = ?", (juego_id,))
    requisitos = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT * FROM resenas WHERE juego_id = ?", (juego_id,))
    resenas = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM biblioteca WHERE juego_id = ?", (juego_id,))
    juego_data['comprado'] = cursor.fetchone() is not None
    
    conn.close()
    
    estructura_completa = {
        **juego_data,
        "requisitos": requisitos,
        "resenas": resenas
    }
    
    return jsonify(estructura_completa)

# =====================================================================
# --- 5. NUEVO: MÓDULO DE TELEMETRÍA (WMI) ---
# =====================================================================
@app.route('/api/telemetria', methods=['GET'])
def escanear_hardware():
    print("Iniciando escaneo de hardware...")
    try:
        # Inicializar los permisos de Windows para el hilo actual
        pythoncom.CoInitialize()
        c = wmi.WMI()

        # 1. Leer Procesador (CPU)
        cpu_nombre = c.Win32_Processor()[0].Name.strip()

        # 2. Leer Tarjeta Gráfica (GPU)
        gpu_nombre = c.Win32_VideoController()[0].Name.strip()

        # 3. Leer Memoria RAM
        ram_bytes = psutil.virtual_memory().total
        ram_gb = round(ram_bytes / (1024**3))

        print(f"Detectado exitosamente: {cpu_nombre} | {gpu_nombre} | {ram_gb}GB")
        
        return jsonify({
            "cpu": cpu_nombre,
            "gpu": gpu_nombre,
            "ram": f"{ram_gb} GB",
            "os": "Windows",
            "status": "success"
        })
    except Exception as e:
        print(f"Error leyendo hardware: {e}")
        return jsonify({
            "cpu": "No se pudo leer CPU",
            "gpu": "No se pudo leer GPU",
            "ram": "--",
            "os": "Desconocido",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)