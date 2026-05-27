import flet as ft
from src.api import get_dragons


def build_dragons_view(on_dragon_click=None):
    dragons = get_dragons()

    if not dragons:
        return ft.Text("Nenhum dragão encontrado.", color="grey")

    tiles = []
    for dragon in dragons:
        name = dragon.get("name", "Sem nome")
        owner = dragon.get("owner", "")
        status = dragon.get("status", "")

        status_color = "green" if status == "Alive" else "red"

        tile = ft.ListTile(
            leading=ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color="deeporange"),
            title=ft.Text(name, weight="bold"),
            subtitle=ft.Text(f"{owner}  •  {status}", color=status_color),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            on_click=(lambda e, d=dragon: on_dragon_click(d)) if on_dragon_click else None,
        )
        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(tiles, spacing=0)