import flet as ft

from src.api import (
    get_characters,
    create_character,
    update_character,
    delete_character,

    get_houses,
    create_house,
    update_house,
    delete_house,

    get_dragons,
    create_dragon,
    update_dragon,
    delete_dragon,

    get_swords,
    create_sword,
    update_sword,
    delete_sword,
)


def main(page: ft.Page):

    page.title = "Game of Thrones API"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # ==========================================================
    # BASE LAYOUT
    # ==========================================================

    content = ft.Column(
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    page.add(content)

    # ==========================================================
    # HELPERS
    # ==========================================================

    def show_message(text, color="green"):

        snack = ft.SnackBar(
            ft.Text(text),
            bgcolor=color
        )

        page.snack_bar = snack
        snack.open = True

        page.update()

    def build_card(title, description, on_edit, on_delete):

        return ft.Container(

            content=ft.Column(
                [
                    ft.Text(
                        title,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Text(
                        description,
                        size=16,
                    ),

                    ft.Row(
                        [
                            ft.Button(
                                "Editar",
                                on_click=on_edit
                            ),

                            ft.Button(
                                "Excluir",
                                on_click=on_delete
                            ),
                        ]
                    ),
                ],
                spacing=10,
            ),

            border=ft.Border(
                top=ft.BorderSide(1, "grey"),
                bottom=ft.BorderSide(1, "grey"),
                left=ft.BorderSide(1, "grey"),
                right=ft.BorderSide(1, "grey"),
            ),

            border_radius=10,
            padding=15,
        )

    def build_form(title_text, submit_text, submit_action, item=None):

        title_input = ft.TextField(
            label="Título",
            value=item.get("title", "") if item else ""
        )

        description_input = ft.TextField(
            label="Descrição",
            multiline=True,
            min_lines=3,
            value=item.get("description", "") if item else ""
        )

        feedback = ft.Text(color="red")

        def submit(e):

            try:

                if not title_input.value.strip():

                    feedback.value = "Título obrigatório"
                    page.update()
                    return

                submit_action(
                    title_input.value.strip(),
                    description_input.value.strip()
                )

            except Exception as err:

                feedback.value = str(err)
                page.update()

        return ft.Column(
            [
                ft.Text(
                    title_text,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),

                title_input,
                description_input,

                ft.Button(
                    submit_text,
                    on_click=submit
                ),

                feedback,
            ],
            spacing=15,
        )

    # ==========================================================
    # PERSONAGENS
    # ==========================================================

    def show_characters():

        characters = get_characters()

        cards = []

        for character in characters:

            cards.append(
                build_card(
                    character.get("title", ""),
                    character.get("description", ""),

                    lambda e, c=character: show_edit_character(c),

                    lambda e, c=character: remove_character(c),
                )
            )

        def create_action(title, description):

            create_character(title, description)

            show_message("Personagem criado com sucesso!")

            show_characters()

        content.controls = [

            build_form(
                "Novo Personagem",
                "Cadastrar",
                create_action
            ),

            ft.Divider(),

            ft.Text(
                "Personagens",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            *cards,
        ]

        page.update()

    def show_edit_character(character):

        def update_action(title, description):

            update_character(
                character["id"],
                title,
                description
            )

            show_message("Personagem atualizado!")

            show_characters()

        content.controls = [

            build_form(
                "Editar Personagem",
                "Salvar",
                update_action,
                character
            ),
        ]

        page.update()

    def remove_character(character):

        delete_character(character["id"])

        show_message("Personagem removido!")

        show_characters()

    # ==========================================================
    # CASAS
    # ==========================================================

    def show_houses():

        houses = get_houses()

        cards = []

        for house in houses:

            cards.append(
                build_card(
                    house.get("title", ""),
                    house.get("description", ""),

                    lambda e, h=house: show_edit_house(h),

                    lambda e, h=house: remove_house(h),
                )
            )

        def create_action(title, description):

            create_house(title, description)

            show_message("Casa criada!")

            show_houses()

        content.controls = [

            build_form(
                "Nova Casa",
                "Cadastrar",
                create_action
            ),

            ft.Divider(),

            ft.Text(
                "Casas",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            *cards,
        ]

        page.update()

    def show_edit_house(house):

        def update_action(title, description):

            update_house(
                house["id"],
                title,
                description
            )

            show_message("Casa atualizada!")

            show_houses()

        content.controls = [

            build_form(
                "Editar Casa",
                "Salvar",
                update_action,
                house
            ),
        ]

        page.update()

    def remove_house(house):

        delete_house(house["id"])

        show_message("Casa removida!")

        show_houses()

    # ==========================================================
    # DRAGÕES
    # ==========================================================

    def show_dragons():

        dragons = get_dragons()

        cards = []

        for dragon in dragons:

            cards.append(
                build_card(
                    dragon.get("title", ""),
                    dragon.get("description", ""),

                    lambda e, d=dragon: show_edit_dragon(d),

                    lambda e, d=dragon: remove_dragon(d),
                )
            )

        def create_action(title, description):

            create_dragon(title, description)

            show_message("Dragão criado!")

            show_dragons()

        content.controls = [

            build_form(
                "Novo Dragão",
                "Cadastrar",
                create_action
            ),

            ft.Divider(),

            ft.Text(
                "Dragões",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            *cards,
        ]

        page.update()

    def show_edit_dragon(dragon):

        def update_action(title, description):

            update_dragon(
                dragon["id"],
                title,
                description
            )

            show_message("Dragão atualizado!")

            show_dragons()

        content.controls = [

            build_form(
                "Editar Dragão",
                "Salvar",
                update_action,
                dragon
            ),
        ]

        page.update()

    def remove_dragon(dragon):

        delete_dragon(dragon["id"])

        show_message("Dragão removido!")

        show_dragons()

    # ==========================================================
    # ESPADAS
    # ==========================================================

    def show_swords():

        swords = get_swords()

        cards = []

        for sword in swords:

            cards.append(
                build_card(
                    sword.get("title", ""),
                    sword.get("description", ""),

                    lambda e, s=sword: show_edit_sword(s),

                    lambda e, s=sword: remove_sword(s),
                )
            )

        def create_action(title, description):

            create_sword(title, description)

            show_message("Espada criada!")

            show_swords()

        content.controls = [

            build_form(
                "Nova Espada",
                "Cadastrar",
                create_action
            ),

            ft.Divider(),

            ft.Text(
                "Espadas",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            *cards,
        ]

        page.update()

    def show_edit_sword(sword):

        def update_action(title, description):

            update_sword(
                sword["id"],
                title,
                description
            )

            show_message("Espada atualizada!")

            show_swords()

        content.controls = [

            build_form(
                "Editar Espada",
                "Salvar",
                update_action,
                sword
            ),
        ]

        page.update()

    def remove_sword(sword):

        delete_sword(sword["id"])

        show_message("Espada removida!")

        show_swords()

    # ==========================================================
    # MENU
    # ==========================================================

    menu = ft.Row(
        [
            ft.Button(
                "Personagens",
                on_click=lambda e: show_characters()
            ),

            ft.Button(
                "Casas",
                on_click=lambda e: show_houses()
            ),

            ft.Button(
                "Dragões",
                on_click=lambda e: show_dragons()
            ),

            ft.Button(
                "Espadas",
                on_click=lambda e: show_swords()
            ),
        ],
        wrap=True,
    )

    page.insert(0, menu)

    # ==========================================================
    # START
    # ==========================================================

    show_characters()


if __name__ == "__main__":
    ft.run(main)
