import flet as ft
from src.api import get_characters


def build_characters_view(on_character_click=None):

    characters = get_characters()

    if not characters:
        return ft.Text(
            "Nenhum personagem encontrado.",
            color="grey"
        )

    tiles = []

    for char in characters:

        title = char.get("title", "Sem nome")
        description = char.get("description", "Sem descrição")

        tile = ft.ListTile(
            leading=ft.Icon(
                ft.Icons.PERSON,
                color="blue"
            ),

            title=ft.Text(
                title,
                weight=ft.FontWeight.BOLD,
                size=18
            ),

            subtitle=ft.Text(
                description,
                color="grey"
            ),

            trailing=ft.Icon(
                ft.Icons.CHEVRON_RIGHT
            ),

            on_click=(
                lambda e, c=char: on_character_click(c)
            ) if on_character_click else None,
        )

        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(
        controls=tiles,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

