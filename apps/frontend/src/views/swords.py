import flet as ft
from src.api import get_swords


def build_swords_view(on_sword_click=None):
    swords = get_swords()

    if not swords:
        return ft.Text("Nenhuma espada encontrada.", color="grey")

    tiles = []
    for sword in swords:
        name = sword.get("name", "Sem nome")
        owner = sword.get("owner", "")
        material = sword.get("material", "")

        valyrian = "Valyrian Steel" in material
        icon_color = "purple" if valyrian else "blueGrey"

        tile = ft.ListTile(
            leading=ft.Icon(ft.Icons.CONSTRUCTION, color=icon_color),
            title=ft.Text(name, weight="bold"),
            subtitle=ft.Text(f"{owner}  •  {material}"),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            on_click=(lambda e, s=sword: on_sword_click(s)) if on_sword_click else None,
        )
        tiles.append(tile)
        tiles.append(ft.Divider(height=1))

    return ft.Column(tiles, spacing=0)