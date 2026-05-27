import flet as ft
from src.api import get_characters


def build_characters_view(on_character_click=None):
    characters = get_characters()

    if not characters:
        return ft.Text("Nenhum personagem encontrado.", color="grey")

    tiles = []
    for char in characters:
        name = char.get("name", "Sem nome")
        house = char.get("house", "")
        status = char.get("status", "")

        status_color = "green" if status == "Alive" else "red"

        tile = ft.ListTile(
            leading=ft.Icon(ft.Icons.PERSON, color="blue"),
            title=ft.Text(name, weight="bold"),
            subtitle=ft.Text(f"{house}  •  {status}", color=status_color),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            on_click=(lambda e, c=char: on_character_click(c)) if on_character_click else None,
        )
        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(tiles, spacing=0)