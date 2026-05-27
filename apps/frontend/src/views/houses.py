import flet as ft
from src.api import get_houses


def build_houses_view(on_house_click=None):

    houses = get_houses()

    if not houses:
        return ft.Text(
            "Nenhuma casa encontrada.",
            color="grey"
        )

    tiles = []

    for house in houses:

        title = house.get("title", "Sem nome")
        description = house.get("description", "Sem descrição")

        tile = ft.ListTile(
            leading=ft.Icon(
                ft.Icons.SHIELD,
                color="orange"
            ),

            title=ft.Text(
                title,
                weight=ft.FontWeight.BOLD,
                size=18
            ),

            subtitle=ft.Text(
                description,
                color="grey",
                italic=True
            ),

            trailing=ft.Icon(
                ft.Icons.CHEVRON_RIGHT
            ),

            on_click=(
                lambda e, h=house: on_house_click(h)
            ) if on_house_click else None,
        )

        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(
        controls=tiles,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

