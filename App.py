from src.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    # Se ejecuta la app en modo debug en el puerto 8000
    app.run(debug=True, port=8000)