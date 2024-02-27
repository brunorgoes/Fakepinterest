from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo, length, email, ValidationError
from fakepinterest.models import Usuario

class Formlogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao = SubmitField('Entrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('E-mail não cadastrado, crie uma conta ou utilize outro e-mail!')

class Formcriarconta(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), email()])
    usuario = StringField('Usuario', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(),length(min=5, max=16)])
    confirmarsenha = PasswordField('Confirmar senha', validators=[DataRequired(), EqualTo('senha')])
    botaocriarconta = SubmitField('criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado, faça login ou utilize outro e-mail!')

    def validate_confirmarsenha(self, senha, confirmarsenha):
        senha = senha.data
        confirmarsenha = confirmarsenha.data
        if senha != confirmarsenha:
            raise ValidationError('senhas divergentes!')


class Formfoto(FlaskForm):
    foto = FileField('Foto', validators=[DataRequired()])
    botaoenviar = SubmitField('Enviar')