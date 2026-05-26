import flet as ft


def build_entities_view(title, items, on_item_click):
    list_items = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    for item in items:

        nome = (
            item.get("name")
            or item.get("title")
            or "Sem nome"
        )

        descricao = (
            item.get("description")
            or item.get("house")
            or item.get("actor")
            or "Sem descrição"
        )

        list_items.controls.append(
            ft.Container(
                content=ft.ListTile(
                    title=ft.Text(
                        nome,
                        weight="bold"
                    ),
                    subtitle=ft.Text(descricao),
                    on_click=lambda e, current=item: on_item_click(current)
                ),
                border=ft.border.Border(
                    left=ft.border.BorderSide(1, "black"),
                    right=ft.border.BorderSide(1, "black"),
                    top=ft.border.BorderSide(1, "black"),
                    bottom=ft.border.BorderSide(1, "black"),
                ),
                border_radius=10,
                padding=5
            )
        )

    return ft.Column([
        ft.Text(
            title,
            size=25,
            weight="bold"
        ),
        list_items
    ])