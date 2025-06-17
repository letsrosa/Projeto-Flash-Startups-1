from flask import Flask, render_template, request, jsonify, url_for
from database import db, Categoria, Usuario, Ideia, Contatos # Importe os novos modelos
import os
from datetime import datetime
import urllib.parse
import uuid
from werkzeug.utils import secure_filename

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


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')  # index.html deve conter seu HTML acima

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

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
    titulo = request.form.get('titulo')
    problema = request.form.get('problemaResolvido')
    solucao = request.form.get('solucaoProposta')
    diferencial = request.form.get('diferencial')
    nome_usuario = request.form.get('nomeAutor')
    email_usuario = request.form.get('emailUsuario')
    categoria_nome = request.form.get('categoria')
    logo = request.files.get('logo')

    if not all([titulo, problema, solucao, diferencial, nome_usuario, categoria_nome, logo]):
        return jsonify({'success': False, 'message': 'Todos os campos são obrigatórios!'}), 400

    if not allowed_file(logo.filename):
        return jsonify({'success': False, 'message': 'Tipo de arquivo não permitido!'}), 400

    filename = secure_filename(f"{uuid.uuid4().hex}_{logo.filename}")
    caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    logo.save(caminho)

    categoria = Categoria.query.filter_by(nome=categoria_nome).first()
    if not categoria:
        categoria = Categoria(nome=categoria_nome, descricao=f"Categoria de {categoria_nome}")
        db.session.add(categoria)
        db.session.commit()

    usuario = Usuario.query.filter_by(email=email_usuario).first()
    if not usuario:
        usuario = Usuario(nome=nome_usuario, email=email_usuario, senha="senha_temporaria")
        db.session.add(usuario)
        db.session.commit()

    nova_ideia = Ideia(
        titulo=titulo,
        descricao=f"Problema: {problema}\nSolução: {solucao}\nDiferencial: {diferencial}",
        id_categoria=categoria.id_categoria,
        id_usuario=usuario.id_usuario,
        data_criacao=datetime.utcnow(),
    )

    # 🚨 Adiciona o campo logo_url:
    nova_ideia.logo = f"/static/uploads/{filename}"

    try:
        db.session.add(nova_ideia)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Startup cadastrada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/listar_ideias', methods=['GET'])
def listar_ideias():
    ideias = Ideia.query.all()
    resultado = []
    for ideia in ideias:
        resultado.append({
            'titulo': ideia.titulo,
            'descricao': ideia.descricao,
            'data_criacao': ideia.data_criacao.strftime('%Y-%m-%d'),
            'categoria': ideia.categoria.nome,
            'autor': ideia.usuario.nome
        })
    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(debug=True)
