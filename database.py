from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'Categoria' 
    id_categoria = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    ideias = db.relationship('Ideia', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Contatos(db.Model):
    __tablename__='Contatos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    assunto = db.Column(db.String(150), unique=True, nullable=False)
    mensagem = db.Column(db.String(150), unique=True, nullable=False)


    
    def __repr__(self):
        return f'<Contatos {self.email}>'

class Usuario(db.Model):
    __tablename__ = 'Usuario' 
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    data_registro = db.Column(db.DateTime, default=datetime.utcnow) 

    ideias = db.relationship('Ideia', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Ideia(db.Model):
    __tablename__ = 'ideia'
    id_ideia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow) 

    id_categoria = db.Column(db.Integer, db.ForeignKey('Categoria.id_categoria'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'), nullable=False)

    def __repr__(self):
        return f'<Ideia {self.titulo}>'