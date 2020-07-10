from flask import jsonify, request, Blueprint
from banco import db
from models.modelCarro import Carro
from models.modelMarca import Marca
from models.modelProposta import Proposta
from models.modelUsuario import Usuario
from flask_jwt_extended import jwt_required

estatisticas = Blueprint('estatisticas', __name__)


@estatisticas.route('/estatisticas')
def dados2():
    carrosCadastrados = db.session.query(db.func.count(Carro.id)).first()[0]
    propostasCadastradas = db.session.query(db.func.count(Proposta.id)).first()[0]
    marcasCadastradas = db.session.query(db.func.count(Marca.id)).first()[0]
    valorPropostas = (db.session.query(db.func.sum(Proposta.valor))).first()[0]

    return jsonify(carrosCadastrados=carrosCadastrados,
        propostasCadastradas=propostasCadastradas,
        marcasCadastradas=marcasCadastradas,
        valorPropostas=valorPropostas)