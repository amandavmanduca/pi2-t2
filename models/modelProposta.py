from banco import db

class Proposta(db.Model):
    __tablename__ = 'propostas'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    item_troca = db.Column(db.String(30), nullable=True)
    valor_item = db.Column(db.Float, nullable=True)
    carro_id = db.Column(db.Integer, db.ForeignKey('carros.id'), nullable=False)
    detalhes = db.Column(db.String(150), nullable=True)

    carro = db.relationship('Carro')

    def to_json(self):
        json_propostas = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'valor': self.valor,
            'item_troca': self.item_troca,
            'valor_item': self.valor_item,
            'detalhes': self.detalhes,
            'carro_id': self.carro_id,
            'carro_nome': self.carro.modelo,
        }
        return json_propostas

    @staticmethod
    def from_json(json_propostas):
        nome = json_propostas.get('nome')
        email = json_propostas.get('email')
        valor = json_propostas.get('valor')
        item_troca = json_propostas.get('item_troca')
        valor_item = json_propostas.get('valor_item')
        detalhes = json_propostas.get('detalhes')
        carro_id = json_propostas.get('carro_id')
        return Proposta(nome=nome, email=email, valor=valor, item_troca=item_troca, valor_item=valor_item, detalhes=detalhes, carro_id=carro_id)
