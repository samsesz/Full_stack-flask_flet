from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Characters
from src.schemas.characters_schema import CharactersSchema
from pydantic import ValidationError

characters_bp = Blueprint('characters', __name__, url_prefix='/characters')

@characters_bp.route('/', methods=['GET'])
def get_all():
    """
    Lista todos os personagens
    ---
    tags:
      - Characters
    responses:
      200:
        description: OK
    """
    characters = Characters.query.all()
    result = [CharactersSchema(**c.to_dict()).model_dump() for c in characters]
    return jsonify(result), 200

@characters_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    Lista um personagem específico pelo ID
    ---
    tags:
      - Characters
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
    character = Characters.query.get(id)

    if not character:
        return jsonify({"error": "Personagem não encontrado"}), 404

    return jsonify(character.to_dict()), 200


@characters_bp.route('/', methods=['POST'])
def create():
    """
    Criar um novo Personagem
    ---
    tags:
      - Characters
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Characters'
    responses:
      200:
        description: Personagem criado com sucesso
        schema:
          $ref: '#/definitions/Characters'
    """
    try:
       data = CharactersSchema(**request.json)
       novo_personagem = Characters(**data.model_dump())
       db.session.add(novo_personagem)
       db.session.commit()
       
       return jsonify(novo_personagem.to_dict()),201
    except ValidationError as err:
      return jsonify({"errors": err.errors()}), 400

@characters_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Atualizar um personagem existente
    ---
    tags:
      - Characters
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Characters'
    responses:
      200:
        description: OK
    """
    character = Characters.query.get(id)

    if not character:
        return jsonify ({"error": "Personagem não encontrado"}), 404
    try:
        data = CharactersSchema(**request.json)

        character.title = data.title
        character.description = data.description

        db.session.commit()
        return jsonify(character.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@characters_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Exclui um personagem
    ---
    tags:
      - Characters
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
    character = Characters.query.get(id)

    if not character:
        return jsonify({"error": "Personagem não encontrado"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({"mensagem":"Personagem removido com sucesso"}), 200