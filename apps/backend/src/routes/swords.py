from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Swords
from src.schemas.swords_schema import SwordsSchema
from pydantic import ValidationError

swords_bp = Blueprint('swords', __name__, url_prefix='/api/swords')

@swords_bp.route('/', methods=['GET'])
def get_all():
    """
    Lista todos as espadas
    ---
    tags:
      - Swords
    responses:
      200:
        description: OK
    """
    swords = Swords.query.all()
    result = [SwordsSchema(**c.to_dict()).model_dump() for c in swords]
    return jsonify(result), 200

@swords_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    Lista um espada específico pelo ID
    ---
    tags:
      - Swords
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do registro
    responses:
      200:
        description: OK
    """
    swords = db.session.get(Swords, id)

    if not swords:
        return jsonify({"error": "Espada não encontrada"}), 404

    return jsonify(swords.to_dict()), 200


@swords_bp.route('/', methods=['POST'])
def create():
    """
    Criar um novo Espada
    ---
    tags:
      - Swords
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Swords'
    responses:
      200:
        description: Espada criada com sucesso
        schema:
          $ref: '#/definitions/Swords'
    """
    try:
       data = SwordsSchema(**request.json)
       novo_sword = Swords(**data.model_dump())
       db.session.add(novo_sword)
       db.session.commit()
       
       return jsonify(novo_sword.to_dict()),201
    except ValidationError as err:
      return jsonify({"errors": err.errors()}), 400

@swords_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Atualizar um espada existente
    ---
    tags:
      - Swords
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Swords'
    responses:
      200:
        description: OK
    """
    sword = Swords.query.get(id)

    if not sword:
        return jsonify ({"error": "Espada não encontrada"}), 404
    try:
        data = SwordsSchema(**request.json)

        sword.title = data.title
        sword.description = data.description

        db.session.commit()
        return jsonify(sword.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@swords_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Exclui um espada
    ---
    tags:
      - Swords
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do registro a ser removido
    responses:
      200:
        description: OK
      404:
        description: Não encontrado
    """  
    swords = Swords.query.get(id)

    if not swords:
        return jsonify({"error": "Espada não encontrada"}), 404

    db.session.delete(swords)
    db.session.commit()

    return jsonify({"mensagem":"Espada removida com sucesso"}), 200