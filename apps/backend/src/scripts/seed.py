import sys
import os

# adiciona a raiz do projeto ao path
sys.path.insert(0, os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
))

from dotenv import load_dotenv

load_dotenv()

from src.app import create_app
from src.database import db
from src.models import Characters, Dragons, Houses, Swords


CHARACTERS = [
    {
        "id": 1,
        "title": "Theon Greyjoy",
        "description": "Protegido de Ned Stark, herdeiro das Ilhas de Ferro",
    },
]

DRAGONS = [
    {
        "id": 1,
        "title": "Caraxes",
        "description": "Dragão de Daemon Targaryen",
    },
]

HOUSES = [
    {
        "id": 1,
        "title": "Stark",
        "description": "O inverno está chegando.",
    },
]

SWORDS = [
    {
        "id": 1,
        "title": "Needle",
        "description": "Espada de Arya Stark",
    },
]


def seed():
    """Popula o banco de dados com os dados iniciais."""

    app = create_app()

    with app.app_context():

        # cria as tabelas automaticamente
        db.create_all()

        # verifica se já existem dados
        if Characters.query.first():
            print("Banco já possui dados. Pulando seed.")
            return

        print("Populando banco de dados...")

        for c in CHARACTERS:
            db.session.add(Characters(**c))

        print(f"{len(CHARACTERS)} personagens inseridos")

        for d in DRAGONS:
            db.session.add(Dragons(**d))

        print(f"{len(DRAGONS)} dragões inseridos")

        for h in HOUSES:
            db.session.add(Houses(**h))

        print(f"{len(HOUSES)} casas inseridas")

        for s in SWORDS:
            db.session.add(Swords(**s))

        print(f"{len(SWORDS)} espadas inseridas")

        db.session.commit()

        print("Seed concluído com sucesso!")


if __name__ == "__main__":
    seed()

