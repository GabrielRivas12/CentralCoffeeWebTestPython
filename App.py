from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')  # Ruta principal
def login():
    return render_template('Pantallas/Ofertas.html')  # <- solo la subcarpeta

@app.route('/chatbox')  
def chatbox():
    return render_template('Pantallas/Chatbox.html')

@app.route('/mapa')
def mapa():
    return render_template('Pantallas/Mapa.html')

@app.route('/ofertas')  
def ofertas():
    return render_template('Pantallas/Ofertas.html')

@app.route('/rci')
def rci():
    return render_template('Pantallas/RCI.html')



if __name__ == '__main__':
    app.run(debug=True, port=8000)
