import flet as ft
from src.api import get_houses


def build_houses_view(on_house_click=None):
    houses = get_houses()

    if not houses:
        return ft.Text("Nenhuma casa encontrada.", color="grey")

    tiles = []
    for house in houses:
        name = house.get("name", "Sem nome")
        words = house.get("words", "")
        region = house.get("region", "")

        tile = ft.ListTile(
            leading=ft.Icon(ft.Icons.SHIELD, color="orange"),
            title=ft.Text(name, weight="bold"),
            subtitle=ft.Text(f'"{words}"  •  {region}', italic=True),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            on_click=(lambda e, h=house: on_house_click(h)) if on_house_click else None,
        )
        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(tiles, spacing=0)