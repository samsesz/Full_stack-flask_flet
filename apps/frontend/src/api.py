import os
import httpx

API_URL = os.environ.get("API_URL", "http://localhost:5000")


def _request_json(
    method: str,
    path: str,
    json_data: dict | None = None
) -> dict | list:
    """Função auxiliar para requisições HTTP."""

    try:

        response = httpx.request(
            method=method,
            url=f"{API_URL}{path}",
            json=json_data,
            timeout=5.0,
            follow_redirects=True,
        )

        print(f"{method} {path}")
        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()

        return response.json()

    except Exception as exc:

        print(f"Erro na API ({path}): {exc}")

        return [] if method == "GET" else {
            "error": str(exc)
        }


# ------------------------------------------------------------------
# PERSONAGENS
# ------------------------------------------------------------------

def get_characters() -> list[dict]:

    return _request_json(
        "GET",
        "/api/characters/"
    )


def create_character(
    title: str,
    description: str
) -> dict:

    return _request_json(
        "POST",
        "/api/characters/",
        json_data={
            "title": title,
            "description": description
        }
    )


def update_character(
    character_id: int,
    title: str,
    description: str
) -> dict:

    return _request_json(
        "PUT",
        f"/api/characters/{character_id}",
        json_data={
            "title": title,
            "description": description
        }
    )


def delete_character(character_id: int) -> dict:

    return _request_json(
        "DELETE",
        f"/api/characters/{character_id}"
    )


# ------------------------------------------------------------------
# CASAS
# ------------------------------------------------------------------

def get_houses() -> list[dict]:

    return _request_json(
        "GET",
        "/api/houses/"
    )


def create_house(
    title: str,
    description: str
) -> dict:

    return _request_json(
        "POST",
        "/api/houses/",
        json_data={
            "title": title,
            "description": description
        }
    )


def update_house(
    house_id: int,
    title: str,
    description: str
) -> dict:

    return _request_json(
        "PUT",
        f"/api/houses/{house_id}",
        json_data={
            "title": title,
            "description": description
        }
    )


def delete_house(house_id: int) -> dict:

    return _request_json(
        "DELETE",
        f"/api/houses/{house_id}"
    )


# ------------------------------------------------------------------
# DRAGÕES
# ------------------------------------------------------------------

def get_dragons() -> list[dict]:

    return _request_json(
        "GET",
        "/api/dragons/"
    )


def create_dragon(
    title: str,
    description: str
) -> dict:

    return _request_json(
        "POST",
        "/api/dragons/",
        json_data={
            "title": title,
            "description": description
        }
    )


def update_dragon(
    dragon_id: int,
    title: str,
    description: str
) -> dict:

    return _request_json(
        "PUT",
        f"/api/dragons/{dragon_id}",
        json_data={
            "title": title,
            "description": description
        }
    )


def delete_dragon(dragon_id: int) -> dict:

    return _request_json(
        "DELETE",
        f"/api/dragons/{dragon_id}"
    )


# ------------------------------------------------------------------
# ESPADAS
# ------------------------------------------------------------------

def get_swords() -> list[dict]:

    return _request_json(
        "GET",
        "/api/swords/"
    )


def create_sword(
    title: str,
    description: str
) -> dict:

    return _request_json(
        "POST",
        "/api/swords/",
        json_data={
            "title": title,
            "description": description
        }
    )


def update_sword(
    sword_id: int,
    title: str,
    description: str
) -> dict:

    return _request_json(
        "PUT",
        f"/api/swords/{sword_id}",
        json_data={
            "title": title,
            "description": description
        }
    )


def delete_sword(sword_id: int) -> dict:

    return _request_json(
        "DELETE",
        f"/api/swords/{sword_id}"
    )

