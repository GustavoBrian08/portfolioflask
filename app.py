import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
import flask_login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minhachavetop'


@app.route('/')
def index():
    connection = sqlite3.connect('database.db')
    posts = connection.execute('SELECT * FROM post ORDER BY id DESC LIMIT 4').fetchall()
    connection.close()

    return render_template('index.html', session=session, posts=posts)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = str(request.form.get('email'))
        senha = str(request.form.get('senha'))

        conn = sqlite3.connect('database.db')
        usuario = conn.execute('SELECT * FROM usuario WHERE email = ? AND senha = ?', [email, senha]).fetchone()
        conn.close()

        if usuario is None:
            flash('Email ou senha incorretos!', 'error')
        else:
            session['email'] = email
            session['nome'] = usuario[2]
            return redirect(url_for('perfil'))

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session['email'] = ''
    return redirect(url_for('index'))


@app.route('/cadastro', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'POST':

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmarSenha = request.form['confirmarSenha']

        if senha == confirmarSenha:
            if not email:
                flash('Email is required!')
            elif not senha:
                flash('Senha is required!')
            elif not nome:
                flash('Nome is required!')
            else:
                connection = sqlite3.connect('database.db')
                connection.execute('INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
                connection.commit()
                connection.close()
                session['email'] = email
                session['nome'] = nome
                return redirect(url_for('perfil'))
        else:
            flash('Senha e confirmar senha são diferentes!')

    return render_template('cadastro.html')


@app.route('/nova_postagem', methods=('GET', 'POST'))
def nova_postagem():

    if request.method == 'POST' and session['email']:
        titulo = request.form.get('titulo')
        categoria = request.form.get('categoria')
        conteudo = request.form.get('conteudo')

        connection = sqlite3.connect('database.db')
        connection.execute('INSERT INTO post (titulo, categoria, conteudo, usuario) VALUES (?, ?, ?, ?)', (titulo, categoria, conteudo, session['email']))
        connection.commit()
        connection.close()

        return redirect(url_for('postagens'))

    return render_template('new_posts.html')


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/postagens', methods=(['GET']))
def postagens():
    connection = sqlite3.connect('database.db')
    posts = connection.execute('SELECT * FROM post ORDER BY id DESC').fetchall()
    connection.close()
    return render_template('posts.html', posts=posts, session=session)


def pegarValor(propriedade):
    connection = sqlite3.connect('database.db')
    p = connection.execute('SELECT {} FROM usuario WHERE email = ?' .format(propriedade), [session['email']])
    dado = p.fetchone() 
    connection.close()
    return dado[0]


@app.route('/perfil', methods=('GET', 'POST'))
def perfil():
    nomeBanco = pegarValor('nome')
    atuacaoBanco = pegarValor('atuacao')
    senhaBanco = pegarValor('senha')
    enderecoBanco = pegarValor('endereco')
    telefoneBanco = pegarValor('telefone')
    nascimentoBanco = pegarValor('nascimento')
    descricaoBanco = pegarValor('descricao')

    connection = sqlite3.connect('database.db')
    posts = connection.execute('SELECT * FROM post ORDER BY id DESC').fetchall()
    connection.close()

    if request.method == 'POST':
        nome = request.form['nome']
        atuacao = request.form['atuacao']
        senha = request.form['senha']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        nascimento = request.form['nascimento']
        descricao = request.form['descricao']

        if session['email']:
            connection = sqlite3.connect('database.db')
            connection.execute('UPDATE usuario SET nome=?, atuacao=?, senha=?, endereco=?, telefone=?, nascimento=?, descricao=? WHERE email = ? ', (nome, atuacao, senha, endereco, telefone, nascimento, descricao, session['email']))
            connection.commit()
            connection.close()
            redirect(url_for('perfil'))

    return render_template('profile.html', session=session, nome=nomeBanco, atuacao=atuacaoBanco, senha=senhaBanco, endereco=enderecoBanco, telefone=telefoneBanco, nascimento=nascimentoBanco, descricao=descricaoBanco, posts=posts)


@app.route('/editar_postagem/<int:id>', methods=('GET', 'POST'))
def editar_postagem(id):
    connection = sqlite3.connect('database.db')
    post = connection.execute('SELECT * FROM post WHERE ID = ?', [id]).fetchone()
    connection.close()

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        categoria = request.form.get('categoria')
        conteudo = request.form.get('conteudo')

        connection = sqlite3.connect('database.db')
        connection.execute('UPDATE post SET titulo=?, categoria=?, conteudo=? WHERE id = ? ', (titulo, categoria, conteudo, id))
        connection.commit()
        connection.close()
        return redirect(url_for('perfil'))            


    return render_template('edit_post.html', post=post)


@app.route('/deletar/<int:id>', methods=('GET', 'POST'))
def deletar(id):

    connection = sqlite3.connect('database.db')
    connection.execute('DELETE FROM post WHERE id = ?', [id])
    connection.commit()
    connection.close()
    flash('postagem deletada!')
    return redirect(url_for('postagens'))


app.run(host='0.0.0.0', port=81, debug=True)
