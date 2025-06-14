from flask import Flask, render_template, request, jsonify
from database import db, Categoria, Usuario, Ideia, Contatos # Importe os novos modelos
import os
from datetime import datetime
import urllib.parse

app = Flask(__name__)

SERVER = 'localhost'       # Geralmente 'localhost' para instância padrão local.
DATABASE = 'FlaskDB'       # Nome do seu banco de dados criado no SQL Server. Confirme que é 'FlaskDB'.
USERNAME = 'flask_user'    # Seu usuário SQL Server.
PASSWORD = 'SenhaSegura123!' # Sua senha.
DRIVER = 'ODBC Driver 17 for SQL Server'

encoded_password = urllib.parse.quote_plus(PASSWORD)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mssql+pyodbc://{USERNAME}:{encoded_password}@{SERVER}/{DATABASE}?'
    f'driver={DRIVER}'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def sobre():
    return render_template('sobre.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/contato.html')
def contato():
    return render_template('contato.html')

@app.route('/contatos', methods=['POST'])
def contatos():
        data = request.get_json()

        nome = data.get('nome') 
        email = data.get('email')
        assunto = data.get('assunto')
        mensagem = data.get('mensagem')

        if not all([nome, email, assunto, mensagem]):
            return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios!'}), 400
        
        novo_contato = Contatos(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )
        try:
            db.session.add(novo_contato)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Contato Cadastrado com Sucesso'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Erro ao cadastrar Contato: {str(e)}'}), 500

@app.route('/cadastrar_ideia', methods=['POST'])
def cadastrar_ideia():
        data = request.get_json()

        titulo = data.get('titulo') 
        descricao_problema = data.get('problemaResolvido')
        descricao_solucao = data.get('solucaoProposta')
        descricao_diferencial = data.get('diferencial')
        descricao_completa = f"Problema: {descricao_problema}\nSolução: {descricao_solucao}\nDiferencial: {descricao_diferencial}"

        nome_usuario = data.get('nomeAutor') 
        email_usuario = data.get('emailUsuario', f"{nome_usuario.replace(' ', '').lower()}@example.com") 
        categoria_nome = data.get('categoria') 

        if not all([titulo, descricao_problema, descricao_solucao, descricao_diferencial, nome_usuario, categoria_nome]):
            return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios!'}), 400

        categoria = Categoria.query.filter_by(nome=categoria_nome).first()
        if not categoria:
            categoria = Categoria(nome=categoria_nome, descricao=f"Categoria de {categoria_nome}")
            db.session.add(categoria)
            db.session.commit() 

        usuario = Usuario.query.filter_by(email=email_usuario).first()
        if not usuario:
            usuario = Usuario(nome=nome_usuario, email=email_usuario, senha="senha_temporaria_hash")
            db.session.add(usuario)
            db.session.commit() 

        nova_ideia = Ideia(
            titulo=titulo,
            descricao=descricao_completa,
            id_categoria=categoria.id_categoria,
            id_usuario=usuario.id_usuario,
            data_criacao=datetime.utcnow() 
        )
        try:
            db.session.add(nova_ideia)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Ideia (Startup) cadastrada com sucesso!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Erro ao cadastrar ideia: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
