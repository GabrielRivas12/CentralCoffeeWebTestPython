from flask import Flask, jsonify, render_template, request 

from controladores.ofertas_controlador import ofertas_bp

app = Flask(__name__, template_folder='vistas')

# ---------------- LOGIN / REGISTRO ----------------
@app.route('/')
def login():
    return render_template('pantallas/login/login.html', full_screen=True)
    
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('pantallas/login/registro.html', full_screen=True)

# ---------------------------------------------------



# ---------------- GEMINI AI ----------------

# 🔑 Clave de Gemini
API_KEY = "AIzaSyCJhLkIM4YqrI1tT9neYLSofwe9katbWWo"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# 📌 Ruta para mostrar el chatbox
@app.route('/chatbox')
def chatbox():
    return render_template('Pantallas/Chatbox/chatbox.html')

# 📌 Ruta para enviar mensajes a Gemini (proxy seguro)
@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    user_text = request.json.get("text", "")  # ✅ request está ahora importado
    if not user_text:
        return jsonify({"error": "Texto vacío"}), 400

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_text}
                ]
            }
        ]
    }

    try:
        # ✅ requests está ahora importado
        response = requests.post(API_URL, json=payload)
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error de API: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- GEMINI AI ----------------



# ---------------- Mapa ----------------

@app.route('/mapa')
def mapa():
    return render_template('pantallas/Mapa/mapa.html')



# ---------------- Mapa ----------------


@app.route('/rci')
def rci():
    return render_template('pantallas/RCI/rci.html')

# ---------------------------------------------------

# ---------------- BLUEPRINT OFERTAS ----------------

# Registrar Blueprint
app.register_blueprint(ofertas_bp)

# ---------------------------------------------------

if __name__ == '__main__':
    # Se ejecuta la app en modo debug en el puerto 8000
    app.run(debug=True, port=8000)