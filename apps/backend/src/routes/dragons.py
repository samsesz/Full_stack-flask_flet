from flask import Blueprint, request, jsonify
from src.database import db
from src.models import Dragons
from src.schemas.dragons_schema import DragonsSchema
from pydantic import ValidationError

dragons_bp = Blueprint('dragons', __name__, url_prefix='/api/dragons')

@dragons_bp.route('/', methods=['GET'])
def get_all():
    """
    Lista todos os dragões
    ---
    tags:
      - Dragons
    responses:
      200:
        description: OK
    """
    dragons = Dragons.query.all()
    result = [DragonsSchema(**c.to_dict()).model_dump() for c in dragons]
    return jsonify(result), 200

@dragons_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """
    Lista um dragão específico pelo ID
    ---
    tags:
      - Dragons
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
    dragon = db.session.get(Dragons, id)

    if not dragon:
        return jsonify({"error": "Dragão não encontrado"}), 404

    return jsonify(dragon.to_dict()), 200



@dragons_bp.route('/', methods=['POST'])
def create():
    """
    Criar um novo Dragão
    ---
    tags:
      - Dragons
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/Dragons'
    responses:
      201:
        description: Dragão criado com sucesso
    """

    try:

        if not request.json:
            return jsonify({
                "error": "JSON não enviado"
            }), 400

        print("JSON RECEBIDO:", request.json)

        data = DragonsSchema(**request.json)

        novo_dragon = Dragons(
            title=data.title,
            description=data.description
        )

        db.session.add(novo_dragon)
        db.session.commit()

        return jsonify(novo_dragon.to_dict()), 201

    except ValidationError as err:

        print("ERRO DE VALIDAÇÃO:", err.errors())

        return jsonify({
            "errors": err.errors()
        }), 400

    except Exception as e:

        print("ERRO GERAL:", str(e))

        return jsonify({
            "error": str(e)
        }), 400


@dragons_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Atualizar um dragão existente
    ---
    tags:
      - Dragons
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Dragons'
    responses:
      200:
        description: OK
    """
    dragon = Dragons.query.get(id)

    if not dragon:
        return jsonify ({"error": "Dragão não encontrado"}), 404
    try:
        data = DragonsSchema(**request.json)

        dragon.title = data.title
        dragon.description = data.description

        db.session.commit()
        return jsonify(dragon.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@dragons_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Exclui um dragão
    ---
    tags:
      - Dragons
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
    dragon = Dragons.query.get(id)

    if not dragon:
        return jsonify({"error": "Dragão não encontrado"}), 404

    db.session.delete(dragon)
    db.session.commit()

    return jsonify({"mensagem":"Dragão removido com sucesso"}), 200