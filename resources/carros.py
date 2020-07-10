from flask import Blueprint, jsonify, request
from banco import db
from models.modelCarro import Carro
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

carros = Blueprint('carros', __name__)


@carros.route('/carros')
def listagem():
    carros = Carro.query.order_by(Carro.modelo).all()
    return jsonify([carro.to_json() for carro in carros])


@carros.route('/carros', methods=['POST'])
@jwt_required
def inclusao():
    carro = Carro.from_json(request.json)
    db.session.add(carro)
    db.session.commit()
    return jsonify(carro.to_json()), 201


@carros.route('/carros/destaque')
def detaques():
    carros = Carro.query.order_by(Carro.modelo).filter(Carro.destaque == 'x').all()
    return jsonify([carro.to_json() for carro in carros])


@carros.route('/carros/filtro/<busca>')
def filtro(busca):
    carros = Carro.query.order_by(Carro.modelo).filter(Carro.modelo.like(f'%{busca}%')).all()
    return jsonify([carro.to_json() for carro in carros])
    #carro.nome.like(f'%{palavra}%'))

@carros.route('/carros/<int:id>', methods=['DELETE'])
@jwt_required
def excluir(id):
    Carro.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Carro excluído com sucesso'}), 200


@carros.route('/carros/<int:id>')
def filtraCarro(id):
    carros = Carro.query.order_by(Carro.id).filter(Carro.id.like(f'{id}')).all()
    return jsonify([carro.to_json() for carro in carros])


@carros.route('/carros/<int:id>', methods=['PUT'])
def alteracao(id):
    carro = Carro.query.get_or_404(id)
    
    carro.modelo = request.json['modelo']
    carro.cor = request.json['cor']
    carro.ano = request.json['ano']
    carro.preco = request.json['preco']
    carro.foto = request.json['foto']
    carro.destaque = request.json['destaque']
    carro.marca_id = request.json['marca_id']

    db.session.add(carro)
    db.session.commit()



@carros.route('/carros/destacar/<int:id>', methods=['PUT'])
def destacar(id):
    carro = Carro.query.get_or_404(id)
    
    if carro.destaque == 'x':
        carro.destaque = ''
    elif carro.destaque == '':
        carro.destaque = 'x'
 
    db.session.add(carro)
    db.session.commit()
    return jsonify(carro.to_json()), 204


@carros.route('/cadastros')
def carroscad():
    carros = db.session.query(db.func.year(Carro.data_cad)+'-'+db.func.month(Carro.data_cad), db.func.count(Carro.id)) \
                       .group_by(db.func.year(Carro.data_cad)+'-'+db.func.month(Carro.data_cad)) \
                       .filter(Carro.data_cad > datetime.today() - timedelta(180))
    print(carros)

    lista = []
    for carro in carros:
        lista.append({'anomes': carro[0], 'num': carro[1]})
    
    print(lista)
    
    return jsonify(lista), 201