from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')  # Ruta principal
def login():
    return render_template('Ofertas/Ofertas.html')  # <- solo la subcarpeta

@app.route('/ofertas')  
def ofertas():
    return render_template('Ofertas/Ofertas.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
