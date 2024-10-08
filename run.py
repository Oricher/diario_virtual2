# Importa o app Flask
from app import app

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)


