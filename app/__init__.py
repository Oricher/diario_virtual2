# Importa o Flask para criar uma aplicação web
from flask import Flask

# Inicializa o app Flask
app = Flask(__name__)

# Importa as rotas (funções que controlam o comportamento das páginas)
from app import routes
