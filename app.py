from flask import Flask, jsonify
from config import config
from banco import db
from resources.carros import carros
from resources.marcas import marcas
from resources.usuarios import usuarios
from resources.estatisticas import estatisticas
from resources.propostas import propostas
from flask_jwt_extended import JWTManager
from blacklist import blacklist
import smtplib

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(carros)
app.register_blueprint(marcas)
app.register_blueprint(usuarios)
app.register_blueprint(propostas)
app.register_blueprint(estatisticas)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/')
def raiz():
    return '<h2>Revenda Herbie</h2>'


@app.route('/envia_email')
def envia():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('edeciofernando@gmail.com', '*********')
    server.set_debuglevel(1)
    server.sendmail('edeciofernando@gmail.com', 
                    'edeciofernando@gmail.com', 
                    'Subject: Aula de PI2\nOlá... testando mensagem')
    server.quit()
    return jsonify({"Message": "E-mail enviado..."})


@app.route('/criadb')
def criadb():
    db.create_all()
    return "Ok! Tabelas criadas com sucesso"


if __name__ == '__main__':
    app.run(debug=True)
