import flet as ft

from src.api import (
    get_houses,
    get_dragons,
    get_characters,
    get_swords
)

from src.views.entities import build_entities_view


def main(page: ft.Page):

    page.title = "Game Of Thrones API"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.width = 450
    page.window.height = 800

    # -----------------------------
    # RENDER
    # -----------------------------
    def render(view_content):
        page.controls.clear()
        page.add(view_content)
        page.update()

    # -----------------------------
    # DETALHES
    # -----------------------------
    def show_details(item):

        nome = (
            item.get("name")
            or item.get("title")
            or "Detalhes"
        )

        detalhes = ft.Column(
            spacing=10,
            controls=[
                ft.Text(
                    nome,
                    size=30,
                    weight="bold"
                )
            ]
        )

        for chave, valor in item.items():

            detalhes.controls.append(
                ft.Text(f"{chave}: {valor}")
            )

        detalhes.controls.append(
            ft.Button(
                "Voltar",
                on_click=lambda e: show_menu()
            )
        )

        render(detalhes)

    # -----------------------------
    # CASAS
    # -----------------------------
    def show_houses():

        houses = get_houses()

        render(
            build_entities_view(
                "Casas",
                houses,
                show_details
            )
        )

    # -----------------------------
    # DRAGÕES
    # -----------------------------
    def show_dragons():

        dragons = get_dragons()

        render(
            build_entities_view(
                "Dragões",
                dragons,
                show_details
            )
        )

    # -----------------------------
    # PERSONAGENS
    # -----------------------------
    def show_characters():

        characters = get_characters()

        render(
            build_entities_view(
                "Personagens",
                characters,
                show_details
            )
        )

    # -----------------------------
    # ESPADAS
    # -----------------------------
    def show_swords():

        swords = get_swords()

        render(
            build_entities_view(
                "Espadas",
                swords,
                show_details
            )
        )

    # -----------------------------
    # MENU
    # -----------------------------
    def show_menu():

        menu = ft.Column(
            spacing=20,
            controls=[

                ft.Text(
                    "Catálogo GOT",
                    size=30,
                    weight="bold"
                ),

                ft.Button(
                    "Casas",
                    width=300,
                    on_click=lambda e: show_houses()
                ),

                ft.Button(
                    "Dragões",
                    width=300,
                    on_click=lambda e: show_dragons()
                ),

                ft.Button(
                    "Personagens",
                    width=300,
                    on_click=lambda e: show_characters()
                ),

                ft.Button(
                    "Espadas",
                    width=300,
                    on_click=lambda e: show_swords()
                )
            ]
        )

        render(menu)

    # -----------------------------
    # INÍCIO
    # -----------------------------
    show_menu()


ft.run(main)