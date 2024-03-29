from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.forms import Formlogin, Formcriarconta, Formfoto
from fakepinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename


@app.route('/', methods=['GET', 'POST'])
def homepage():
    formlogin = Formlogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"),formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = Formcriarconta()

    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data).decode("utf-8")
        usuario = Usuario(nome=formcriarconta.usuario.data, email = formcriarconta.email.data, senha = senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)

        return redirect(url_for('perfil', id_usuario=usuario.id))

    return render_template('criarconta.html', form=formcriarconta)

@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get(int(id_usuario))
    if int(id_usuario) == int(current_user.id):
        formfoto = Formfoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)
            #registrar no banco de dados
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template('perfil.html', usuario=current_user, form=formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_foto.desc()).all()
    return render_template('feed.html', fotos=fotos, form=None)
