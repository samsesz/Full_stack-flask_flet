import os
import httpx

API_URL = os.environ.get("API_URL", "http://localhost:5000")


def _request_json(method: str, path: str, json_data: dict | None = None) -> dict | list:
    """Função auxiliar para fazer requisições e tratar erros."""
    try:
        response = httpx.request(
            method=method,
            url=f"{API_URL}{path}",
            json=json_data,
            timeout=5.0,
            follow_redirects=True,
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        print(f"Erro na API ({path}): {exc}")
        raise RuntimeError(f"Erro ao conectar com o servidor: {exc}")


# ------------------------------------------------------------------
# PERSONAGENS
# ------------------------------------------------------------------

def get_characters() -> list[dict]:
    return _request_json("GET", "/api/characters/")


def create_character(name: str, house: str = "", title: str = "", status: str = "Alive") -> dict:
    return _request_json("POST", "/api/characters/", json_data={
        "name": name, "house": house, "title": title, "status": status
    })


def update_character(character_id: int, name: str, house: str = "", title: str = "", status: str = "") -> dict:
    return _request_json("PUT", f"/api/characters/{character_id}", json_data={
        "name": name, "house": house, "title": title, "status": status
    })


def delete_character(character_id: int) -> dict:
    return _request_json("DELETE", f"/api/characters/{character_id}")


# ------------------------------------------------------------------
# CASAS
# ------------------------------------------------------------------

def get_houses() -> list[dict]:
    return _request_json("GET", "/api/houses/")


def create_house(name: str, words: str = "", seat: str = "", region: str = "") -> dict:
    return _request_json("POST", "/api/houses/", json_data={
        "name": name, "words": words, "seat": seat, "region": region
    })


def update_house(house_id: int, name: str, words: str = "", seat: str = "", region: str = "") -> dict:
    return _request_json("PUT", f"/api/houses/{house_id}", json_data={
        "name": name, "words": words, "seat": seat, "region": region
    })


def delete_house(house_id: int) -> dict:
    return _request_json("DELETE", f"/api/houses/{house_id}")


# ------------------------------------------------------------------
# DRAGÕES
# ------------------------------------------------------------------

def get_dragons() -> list[dict]:
    return _request_json("GET", "/api/dragons/")


def create_dragon(name: str, color: str = "", owner: str = "", status: str = "Alive") -> dict:
    return _request_json("POST", "/api/dragons/", json_data={
        "name": name, "color": color, "owner": owner, "status": status
    })


def update_dragon(dragon_id: int, name: str, color: str = "", owner: str = "", status: str = "") -> dict:
    return _request_json("PUT", f"/api/dragons/{dragon_id}", json_data={
        "name": name, "color": color, "owner": owner, "status": status
    })


def delete_dragon(dragon_id: int) -> dict:
    return _request_json("DELETE", f"/api/dragons/{dragon_id}")


# ------------------------------------------------------------------
# ESPADAS
# ------------------------------------------------------------------

def get_swords() -> list[dict]:
    return _request_json("GET", "/api/swords/")


def create_sword(name: str, sword_type: str = "", owner: str = "", material: str = "") -> dict:
    return _request_json("POST", "/api/swords/", json_data={
        "name": name, "type": sword_type, "owner": owner, "material": material
    })


def update_sword(sword_id: int, name: str, sword_type: str = "", owner: str = "", material: str = "") -> dict:
    return _request_json("PUT", f"/api/swords/{sword_id}", json_data={
        "name": name, "type": sword_type, "owner": owner, "material": material
    })


def delete_sword(sword_id: int) -> dict:
    return _request_json("DELETE", f"/api/swords/{sword_id}")