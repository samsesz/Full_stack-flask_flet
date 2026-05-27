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
            follow_redirects=True  # Segue redirects automaticamente
        )
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        print(f"Erro na API ({path}): {exc}")
        raise RuntimeError(f"Erro ao conectar com o servidor: {exc}")


def get_dragons() -> list[dict]:
    """Busca a lista de filmes do backend."""
    return _request_json("GET", "/dragons/")


def create_dragons(title: str) -> dict:
    """Cria um novo filme no backend."""
    return _request_json(
        "POST",
        "/dragons/",
        json_data={"title": title}
    )


def update_dragons(dragons_id: int, title: str) -> dict:
    """Atualiza um filme no backend."""
    return _request_json(
        "PUT",
        f"/dragons/{dragons_id}",
        json_data={"title": title}
    )


def delete_dragons(dragons_id: int) -> dict:
    """Exclui um filme no backend."""
    return _request_json(
        "DELETE",
        f"/dragons/{dragons_id}"
    )


def get_characterss() -> list[dict]:
    """Busca a lista de atores do backend."""
    return _request_json("GET", "/characterss/")


def create_characters(name: str) -> dict:
    """Cria um novo ator no backend."""
    return _request_json(
        "POST",
        "/characterss/",
        json_data={"name": name}
    )


def update_characters(characters_id: int, name: str) -> dict:
    """Atualiza um ator no backend."""
    return _request_json(
        "PUT",
        f"/characterss/{characters_id}",
        json_data={"name": name}
    )


def delete_characters(characters_id: int) -> dict:
    """Exclui um ator no backend."""
    return _request_json(
        "DELETE",
        f"/characterss/{characters_id}"
    )


def get_houses() -> list[dict]:
    """Busca a lista de gêneros do backend."""
    return _request_json("GET", "/houses/")


def create_houses(name: str) -> dict:
    """Cria um novo gênero no backend."""
    return _request_json(
        "POST",
        "/houses/",
        json_data={"name": name}
    )


def update_houses(houses_id: int, name: str) -> dict:
    """Atualiza um gênero no backend."""
    return _request_json(
        "PUT",
        f"/houses/{houses_id}",
        json_data={"name": name}
    )


def delete_houses(houses_id: int) -> dict:
    """Exclui um gênero no backend."""
    return _request_json(
        "DELETE",
        f"/houses/{houses_id}"
    )


def get_swords() -> list[dict]:
    """Busca a lista de séries do backend."""
    return _request_json("GET", "/swords/")


def create_swords(title: str) -> dict:
    """Cria uma nova série no backend."""
    return _request_json(
        "POST",
        "/swords/",
        json_data={"title": title}
    )


def update_swords(swords_id: int, title: str) -> dict:
    """Atualiza uma série no backend."""
    return _request_json(
        "PUT",
        f"/swords/{swords_id}",
        json_data={"title": title}
    )


def delete_swords(swords_id: int) -> dict:
    """Exclui uma série no backend."""
    return _request_json(
        "DELETE",
        f"/swords/{swords_id}"
    )


def get_characterss() -> list[dict]:
    """Busca a lista de atores do backend."""
    return _request_json("GET", "/characterss/")


def get_houses() -> list[dict]:
    """Busca a lista de gêneros do backend."""
    return _request_json("GET", "/houses/")


def get_swords() -> list[dict]:
    """Busca a lista de séries do backend."""
    return _request_json("GET", "/swords/")