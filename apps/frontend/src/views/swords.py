import flet as ft
from src.api import get_swords


def build_swords_view(on_sword_click=None):

    swords = get_swords()

    if not swords:
        return ft.Text(
            "Nenhuma espada encontrada.",
            color="grey"
        )

    tiles = []

    for sword in swords:

        title = sword.get("title", "Sem nome")
        description = sword.get("description", "Sem descrição")

        tile = ft.ListTile(
            leading=ft.Icon(
                ft.Icons.CONSTRUCTION,
                color="brown"
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
                lambda e, s=sword: on_sword_click(s)
            ) if on_sword_click else None,
        )

        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(
        controls=tiles,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

