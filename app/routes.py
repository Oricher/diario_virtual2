from app import app
from flask import request, jsonify, render_template, request
from .models import get_db_connection
from math import ceil

# Rota principal para exibir a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota para adicionar uma nova entrada ao diário (via POST)
@app.route('/add_entry', methods=['POST'])
def add_entry():
    # Obtém dados do formulário
    title = request.form['title']
    content = request.form['content']
    
    # Conecta ao banco de dados e insere a nova entrada
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (title, content, created_at) VALUES (%s, %s, NOW())', (title, content))
    conn.commit()
    cursor.close()
    conn.close()
    
    # Retorna uma resposta em formato JSON
    return jsonify({'status': 'success', 'message': 'Entry added successfully!'})

# Rota para listar todas as entradas do diário (via GET e renderizar o HTML)
@app.route('/entries')
def list_entries():
    # Conecta ao banco de dados e busca as entradas
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Usa 'dictionary=True' para retornar colunas com nome
    cursor.execute("SELECT * FROM entries ORDER BY created_at DESC")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    per_page = 6
    page = request.args.get('page', 1, type=int)
    total_entries = len(entries)  # Assumindo que 'entries' é a lista com todas as entradas
    total_pages = ceil(total_entries / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    entries_to_show = entries[start:end]

    return render_template('list_entries.html', entries=entries_to_show, page=page, total_pages=total_pages)

# Rota para editar uma entrada existente (via POST)
@app.route('/edit_entry/<int:entry_id>', methods=['POST'])
def edit_entry(entry_id):
    # Obtém os dados do formulário
    title = request.form['title'] 
    content = request.form['content']
    
    # Conecta ao banco de dados e atualiza a entrada com o ID fornecido
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE entries SET title = %s, content = %s WHERE id = %s', (title, content, entry_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    # Retorna uma resposta em formato JSON
    return jsonify({'status': 'success', 'message': 'Entry updated successfully!'})

# Rota para excluir uma entrada existente (via DELETE)
@app.route('/delete_entry/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    # Conecta ao banco de dados e exclui a entrada com o ID fornecido
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE id = %s', (entry_id,))
    conn.commit()
    cursor.close()
    conn.close()

    # Retorna uma resposta em formato JSON
    return jsonify({'status': 'success', 'message': 'Entry deleted successfully!'})

# Rota para visualizar uma entrada específica (via GET)
@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    # Conecta ao banco de dados e busca a entrada com o ID fornecido
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Usa 'dictionary=True' para retornar colunas com nome
    cursor.execute('SELECT * FROM entries WHERE id = %s', (entry_id,))
    entry = cursor.fetchone()
    cursor.close()
    conn.close()

    # Se não encontrar a entrada, retorna um erro 404
    if entry is None:
        return jsonify({'status': 'error', 'message': 'Entry not found!'}), 404

    # Renderiza a página de visualização da entrada
    return render_template('view_entry.html', entry=entry)
