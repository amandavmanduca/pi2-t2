from flask import Blueprint, jsonify, request
from banco import db
from models.modelProposta import Proposta
from models.modelCarro import Carro
from flask_jwt_extended import jwt_required
from email.message import EmailMessage
import smtplib

propostas = Blueprint('propostas', __name__)


@propostas.route('/propostas')
def listagem():
    propostas = Proposta.query.order_by(Proposta.id).all()
    return jsonify([proposta.to_json() for proposta in propostas])


@propostas.route('/propostas', methods=['POST'])
def inclusao():
    proposta = Proposta.from_json(request.json)
    db.session.add(proposta)
    db.session.commit()

    if proposta.valor_item == '':
        total = proposta.valor
    else:
        total = proposta.valor + proposta.valor_item
    carros = Carro.query.filter(Carro.id == proposta.carro_id).all()

    if proposta.item_troca == '':
        message = ('Subject: Proposta Revenda Herbie Carro# ' + str(proposta.carro_id) + ' [' + str(carros[0].modelo) + '-' + str(carros[0].ano) +']\n\n'  """\
            Olá %s !
            Recebemos os detalhes da sua Proposta #%s no Valor de R$%s.
            Foram incluídos também os detalhes: "%s".
            Essa oferta foi feita para o veículo: %s Ano %s cor %s com oferta de R$%s.

            Agradecemos sua preferência
            EQUIPE REVENDA HERBIE 2020
            """ % (str(proposta.nome), str(proposta.id), str(proposta.valor), str(proposta.detalhes), str(carros[0].modelo), str(carros[0].ano), str(carros[0].cor), str(carros[0].preco))).encode()
    else:
        message = ('Subject: Proposta Revenda Herbie Carro# ' + str(proposta.carro_id) + ' [' + str(carros[0].modelo) + '-' + str(carros[0].ano) +']\n\n'  """\
            Olá %s !
            Recebemos os detalhes da sua Proposta #%s no Valor de R$%s, além da entrega do ítem %s no valor de R$%s.
            Com isso, sua proposta acaba totalizando R$%s.
            Foram incluídos também os detalhes: "%s".
            Essa oferta foi feita para o veículo: %s Ano %s cor %s com oferta de R$%s.\n

            Agradecemos sua preferência
            EQUIPE REVENDA HERBIE 2020
            """ % (str(proposta.nome), str(proposta.id), str(proposta.valor), str(proposta.item_troca), str(proposta.valor_item), str(total), str(proposta.detalhes), str(carros[0].modelo), str(carros[0].ano), str(carros[0].cor), str(carros[0].preco))).encode()


        #Olá %s !
        #Recebemos os detalhes da sua Proposta #%s no Valor de R$%s, além da entrega do ítem %s no valor de R$%s.
        #Com isso, sua proposta acaba totalizando R$%s.
        #Foram incluídos também os detalhes:
        #    %s.

        #Essa oferta foi feita para o seguinte veículo:
        #%s %s Ano %s cor %s com oferta de R$%s.
    
    #carros = Carro.query.order_by(Carro.modelo).filter(Carro.destaque == 'x').all()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('teste.senac.pi2@gmail.com', 'testesenacpi2')
    server.set_debuglevel(1)
    server.sendmail('teste.senac.pi2@gmail.com', 
                    str(proposta.email), 
                    message)
    server.quit()
    return jsonify(proposta.to_json()), 201


@propostas.route('/propostas/<int:id>', methods=['DELETE'])
@jwt_required
def excluir(id):
    Proposta.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Proposta excluída com sucesso'}), 200


@propostas.route('/repplyproposta/<int:id>', methods=['POST'])
#@jwt_required
def repply(id):

    proposta = Proposta.query.filter(Proposta.id == id).all()


    message = ('Subject: Proposta Revenda Herbie Carro# ' + str(proposta[0].id) +'\n\n'  """\
            Olá %s !
            Temos interesse na sua Proposta #%s.

            Por favor, entre em contato com a nossa equipe!           


            Agradecemos sua preferência
            EQUIPE REVENDA HERBIE 2020
            """ % (str(proposta[0].nome), str(proposta[0].id))).encode()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('teste.senac.pi2@gmail.com', 'testesenacpi2')
    server.set_debuglevel(1)
    server.sendmail('teste.senac.pi2@gmail.com', 
                    str(proposta[0].email), 
                    message)
    server.quit()
    return jsonify(), 201
