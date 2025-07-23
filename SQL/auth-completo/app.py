from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import flash

from flask_login import LoginManager, UserMixin, logout_user
from flask_login import login_required, login_user

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


import sqlite3

login_manager = LoginManager()
app = Flask(__name__)

login_manager.__init__(app)

app.secret_key = 'chave_secreta'


def obter_conexao():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    def __init__(self, nome, senha) -> None:
        self.nome = nome
        self.senha = senha

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM users WHERE nome = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        conexao.close()

        if resultado is None:
            return None

        user = User(nome=resultado['nome'], senha=resultado['senha'])
        user.id = resultado['nome']
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['name']
        senha = request.form['password']

        conexao = obter_conexao()
        sql = "SELECT * FROM users WHERE nome = ?"
        resultado = conexao.execute(sql, (nome,)).fetchone()

        if resultado:
            hash = resultado['senha']
            if check_password_hash(hash, senha):
                user = User(nome=resultado['nome'], senha=hash)
                user.id = resultado['nome']
                login_user(user)
                return redirect(url_for('dash'))

        flash('Dados incorretos', category='error') 
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nome = request.form['name']
        senha= request.form['password']
    
        conexao = obter_conexao()        
        sql = "select * from users where nome = ?"
        resultado = conexao.execute(sql, (nome,)).fetchone()
        # none
        if not resultado:
            # realização do cadastro
            hash = generate_password_hash(senha)
            sql = "INSERT INTO users(nome, senha) VALUES(?,?)"
            conexao.execute(sql, (nome, hash))
            conexao.commit() 

            # definir o usuário para logar
            user = User(nome=nome, senha=senha)
            user.id = nome

            login_user(user)

            # flash('Cadastro realizado com sucesso!', category='error')
            return redirect(url_for('dash'))

        conexao.close()
        
        flash('Problema no cadastro', category='error')
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dash():
    return render_template('dash.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))