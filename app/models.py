# Importa o conector MySQL para fazer a conexão com o banco de dados
import mysql.connector
from flask import current_app

# Função para estabelecer a conexão com o banco de dados
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  # Endereço do servidor MySQL
        user='root',  # Usuário do MySQL
        password='mysql',  # Senha do MySQL
        database='diary'  # Nome do banco de dados
    )
    return conn
