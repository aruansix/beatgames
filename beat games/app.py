from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__BEAT__)
app.secret_key = "beatgames_3121"


usuarios = []
jogos = [
    {
        "id": 1,
        "nome": "The Witcher 3",
        "descricao": "Um RPG de mundo aberto com uma história envolvente.",
        "categoria": "RPG",
        "capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg",
        "avaliacao": 4.9
    },
    {
        "id": 2,
        "nome": "Celeste",
        "descricao": "Um jogo de plataforma desafiador sobre superação pessoal.",
        "categoria": "Plataforma",
        "capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/504230/header.jpg",
        "avaliacao": 4.8
    },
    {
        "id": 3,
        "nome": "Hollow Knight",
        "descricao": "Uma aventura sombria e deslumbrante em um mundo subterrâneo.",
        "categoria": "Metroidvania",
        "capa": "https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg",
        "avaliacao": 4.7
    }
]

@app.route('/')
def index():
    return render_template('index.html', jogos=jogos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = next((u for u in usuarios if u['email'] == email and u['senha'] == senha), None)
        if user:
            session['usuario'] = user['nome']
            flash("Login realizado com sucesso!", "sucesso")
            return redirect(url_for('index'))
        else:
            flash("Email ou senha incorretos.", "erro")
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if any(u['email'] == email for u in usuarios):
            flash("Email já cadastrado.", "erro")
        else:
            usuarios.append({"nome": nome, "email": email, "senha": senha})
            flash("Cadastro realizado! Faça login.", "sucesso")
            return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/jogo/<int:jogo_id>')
def jogo(jogo_id):
    jogo = next((j for j in jogos if j["id"] == jogo_id), None)
    if not jogo:
        flash("Jogo não encontrado.", "erro")
        return redirect(url_for('index'))
    return render_template('jogo.html', jogo=jogo)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
