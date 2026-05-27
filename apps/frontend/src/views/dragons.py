import flet as ft
from src.api import get_dragons


def build_dragons_view(on_dragon_click=None):

    dragons = get_dragons()

    if not dragons:
        return ft.Text(
            "Nenhum dragão encontrado.",
            color="grey"
        )

    tiles = []

    for dragon in dragons:

        title = dragon.get("title", "Sem nome")
        description = dragon.get("description", "Sem descrição")

        tile = ft.ListTile(
            leading=ft.Icon(
                ft.Icons.LOCAL_FIRE_DEPARTMENT,
                color="deeporange"
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
                lambda e, d=dragon: on_dragon_click(d)
            ) if on_dragon_click else None,
        )

        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(
        controls=tiles,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

