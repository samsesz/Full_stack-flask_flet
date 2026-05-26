from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Houses
from src.schemas.houses_schema import HousesSchema
from pydantic import ValidationError

houses_bp = Blueprint('houses', __name__, url_prefix='/houses')

@houses_bp.route('/', methods=['GET'])
def get_all():
    """
    Lista todas as casas
    ---
    tags:
      - Houses
    responses:
      200:
        description: OK
    """
    houses = Houses.query.all()
    result = [HousesSchema(**c.to_dict()).model_dump() for c in houses]
    return jsonify(result), 200

@houses_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    Lista uma casa específica pelo ID
    ---
    tags:
      - Houses
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
    houses = Houses.query.get(id)

    if not houses:
        return jsonify({"error": "Casa não encontrada"}), 404

    return jsonify(houses.to_dict()), 200


@houses_bp.route('/', methods=['POST'])
def create():
    """
    Criar uma nova Casa
    ---
    tags:
      - Houses
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Houses'
    responses:
      200:
        description: Personagem criado com sucesso
        schema:
          $ref: '#/definitions/Houses'
    """
    try:
       data = HousesSchema(**request.json)
       novo_houses = Houses(**data.model_dump())
       db.session.add(novo_houses)
       db.session.commit()
       
       return jsonify(novo_houses.to_dict()),201
    except ValidationError as err:
      return jsonify({"errors": err.errors()}), 400

@houses_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Atualizar uma casa existente
    ---
    tags:
      - Houses
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Houses'
    responses:
      200:
        description: OK
    """
    houses = Houses.query.get(id)

    if not houses:
        return jsonify ({"error": "Casa não encontrada"}), 404
    try:
        data = HousesSchema(**request.json)

        houses.title = data.title
        houses.description = data.description

        db.session.commit()
        return jsonify(houses.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@houses_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Exclui uma casa
    ---
    tags:
      - Houses
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
    houses = Houses.query.get(id)

    if not houses:
        return jsonify({"error": "Casa não encontrada"}), 404

    db.session.delete(houses)
    db.session.commit()

    return jsonify({"mensagem":"Casa removida com sucesso"}), 200