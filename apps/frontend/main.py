import flet as ft

from src.state import state
from src.api import (
    get_characters, create_character, update_character, delete_character,
    get_houses,    create_house,     update_house,     delete_house,
    get_dragons,   create_dragon,    update_dragon,    delete_dragon,
    get_swords,    create_sword,     update_sword,     delete_sword,
)
from src.views.characters import build_characters_view
from src.views.houses     import build_houses_view
from src.views.dragons    import build_dragons_view
from src.views.swords     import build_swords_view


def main(page: ft.Page):
    page.title = "Game of Thrones API"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width  = 450
    page.window.height = 800

    # ------------------------------------------------------------------
    # RENDER
    # ------------------------------------------------------------------
    def render(view_content: ft.Control):
        """Limpa a tela e renderiza novo conteúdo."""
        page.clean()
        page.add(view_content)
        page.update()

    # ------------------------------------------------------------------
    # NAVEGAÇÃO
    # ------------------------------------------------------------------
    def build_navigation():
        return ft.Row(
            [
                ft.ElevatedButton("Personagens", on_click=lambda e: show_characters()),
                ft.ElevatedButton("Casas",        on_click=lambda e: show_houses()),
                ft.ElevatedButton("Dragões",      on_click=lambda e: show_dragons()),
                ft.ElevatedButton("Espadas",      on_click=lambda e: show_swords()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
            wrap=True,
        )

    # ------------------------------------------------------------------
    # TOOLBAR GET / POST / PUT / DELETE
    # ------------------------------------------------------------------
    def build_route_toolbar(on_get, on_post, on_put, on_delete,
                            put_disabled=False, delete_disabled=False):
        return ft.Row(
            [
                ft.ElevatedButton("GET",    on_click=on_get),
                ft.ElevatedButton("POST",   on_click=on_post),
                ft.ElevatedButton("PUT",    on_click=on_put,    disabled=put_disabled),
                ft.ElevatedButton("DELETE", on_click=on_delete, disabled=delete_disabled),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

    # ==================================================================
    # PERSONAGENS
    # ==================================================================
    def show_characters():
        state.current_character = None

        view = build_characters_view(on_character_click=show_character_detail)
        toolbar = build_route_toolbar(
            on_get    = lambda e: show_characters(),
            on_post   = lambda e: show_add_character(),
            on_put    = lambda e: show_update_character(state.current_character) if state.current_character else None,
            on_delete = lambda e: delete_character_action(state.current_character["id"]) if state.current_character else None,
            put_disabled=True,
            delete_disabled=True,
        )

        content = ft.Column(
            [ft.Text("Personagens", size=28, weight="bold"), ft.Divider(), toolbar, view],
            spacing=10,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_character_detail(character):
        state.current_character = character

        toolbar = build_route_toolbar(
            on_get    = lambda e: show_characters(),
            on_post   = lambda e: show_add_character(),
            on_put    = lambda e: show_update_character(character),
            on_delete = lambda e: delete_character_action(character["id"]),
        )

        back_btn = ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_characters())

        rows = [ft.Row([back_btn, ft.Container(expand=True)]),
                ft.Text(character.get("name", ""), size=24, weight="bold"),
                ft.Text(f"ID: {character.get('id', '?')}", size=14, color="grey"),
                ft.Divider()]
        for k, v in character.items():
            if k != "id":
                rows.append(ft.Text(f"{k.capitalize()}: {v}"))

        content = ft.Column([toolbar] + rows, spacing=12)
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_add_character():
        name_input   = ft.TextField(label="Nome",  hint_text="Ex: Jon Snow")
        house_input  = ft.TextField(label="Casa",  hint_text="Ex: Stark")
        title_input  = ft.TextField(label="Título", hint_text="Ex: King in the North")
        status_input = ft.TextField(label="Status", hint_text="Alive / Deceased", value="Alive")
        feedback     = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome do personagem!"
                page.update()
                return
            try:
                create_character(name, house_input.value.strip(),
                                 title_input.value.strip(), status_input.value.strip())
                show_characters()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Novo Personagem", size=25, weight="bold"), ft.Divider(),
             name_input, house_input, title_input, status_input,
             ft.Row([ft.ElevatedButton("Cadastrar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_update_character(character):
        if not character:
            show_characters(); return

        name_input   = ft.TextField(label="Nome",   value=character.get("name", ""))
        house_input  = ft.TextField(label="Casa",   value=character.get("house", ""))
        title_input  = ft.TextField(label="Título", value=character.get("title", ""))
        status_input = ft.TextField(label="Status", value=character.get("status", ""))
        feedback     = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome do personagem!"
                page.update()
                return
            try:
                update_character(character["id"], name, house_input.value.strip(),
                                 title_input.value.strip(), status_input.value.strip())
                show_characters()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Editar Personagem", size=25, weight="bold"), ft.Divider(),
             name_input, house_input, title_input, status_input,
             ft.Row([ft.ElevatedButton("Salvar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def delete_character_action(char_id):
        if not char_id:
            show_characters(); return
        try:
            delete_character(char_id)
            show_characters()
        except Exception as err:
            render(ft.Column([build_navigation(),
                               ft.Text(f"Erro ao excluir personagem: {err}", color="red")],
                              scroll=ft.ScrollMode.AUTO))

    # ==================================================================
    # CASAS
    # ==================================================================
    def show_houses():
        state.current_house = None

        view = build_houses_view(on_house_click=show_house_detail)
        toolbar = build_route_toolbar(
            on_get    = lambda e: show_houses(),
            on_post   = lambda e: show_add_house(),
            on_put    = lambda e: show_update_house(state.current_house) if state.current_house else None,
            on_delete = lambda e: delete_house_action(state.current_house["id"]) if state.current_house else None,
            put_disabled=True,
            delete_disabled=True,
        )

        content = ft.Column(
            [ft.Text("Casas", size=28, weight="bold"), ft.Divider(), toolbar, view],
            spacing=10,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_house_detail(house):
        state.current_house = house

        toolbar = build_route_toolbar(
            on_get    = lambda e: show_houses(),
            on_post   = lambda e: show_add_house(),
            on_put    = lambda e: show_update_house(house),
            on_delete = lambda e: delete_house_action(house["id"]),
        )

        back_btn = ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_houses())

        rows = [ft.Row([back_btn, ft.Container(expand=True)]),
                ft.Text(house.get("name", ""), size=24, weight="bold"),
                ft.Text(f"ID: {house.get('id', '?')}", size=14, color="grey"),
                ft.Divider()]
        for k, v in house.items():
            if k != "id":
                rows.append(ft.Text(f"{k.capitalize()}: {v}"))

        content = ft.Column([toolbar] + rows, spacing=12)
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_add_house():
        name_input   = ft.TextField(label="Nome",   hint_text="Ex: House Stark")
        words_input  = ft.TextField(label="Lema",   hint_text="Ex: Winter is Coming")
        seat_input   = ft.TextField(label="Sede",   hint_text="Ex: Winterfell")
        region_input = ft.TextField(label="Região", hint_text="Ex: The North")
        feedback     = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome da casa!"
                page.update()
                return
            try:
                create_house(name, words_input.value.strip(),
                             seat_input.value.strip(), region_input.value.strip())
                show_houses()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Nova Casa", size=25, weight="bold"), ft.Divider(),
             name_input, words_input, seat_input, region_input,
             ft.Row([ft.ElevatedButton("Cadastrar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_update_house(house):
        if not house:
            show_houses(); return

        name_input   = ft.TextField(label="Nome",   value=house.get("name", ""))
        words_input  = ft.TextField(label="Lema",   value=house.get("words", ""))
        seat_input   = ft.TextField(label="Sede",   value=house.get("seat", ""))
        region_input = ft.TextField(label="Região", value=house.get("region", ""))
        feedback     = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome da casa!"
                page.update()
                return
            try:
                update_house(house["id"], name, words_input.value.strip(),
                             seat_input.value.strip(), region_input.value.strip())
                show_houses()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Editar Casa", size=25, weight="bold"), ft.Divider(),
             name_input, words_input, seat_input, region_input,
             ft.Row([ft.ElevatedButton("Salvar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def delete_house_action(house_id):
        if not house_id:
            show_houses(); return
        try:
            delete_house(house_id)
            show_houses()
        except Exception as err:
            render(ft.Column([build_navigation(),
                               ft.Text(f"Erro ao excluir casa: {err}", color="red")],
                              scroll=ft.ScrollMode.AUTO))

    # ==================================================================
    # DRAGÕES
    # ==================================================================
    def show_dragons():
        state.current_dragon = None

        view = build_dragons_view(on_dragon_click=show_dragon_detail)
        toolbar = build_route_toolbar(
            on_get    = lambda e: show_dragons(),
            on_post   = lambda e: show_add_dragon(),
            on_put    = lambda e: show_update_dragon(state.current_dragon) if state.current_dragon else None,
            on_delete = lambda e: delete_dragon_action(state.current_dragon["id"]) if state.current_dragon else None,
            put_disabled=True,
            delete_disabled=True,
        )

        content = ft.Column(
            [ft.Text("Dragões", size=28, weight="bold"), ft.Divider(), toolbar, view],
            spacing=10,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_dragon_detail(dragon):
        state.current_dragon = dragon

        toolbar = build_route_toolbar(
            on_get    = lambda e: show_dragons(),
            on_post   = lambda e: show_add_dragon(),
            on_put    = lambda e: show_update_dragon(dragon),
            on_delete = lambda e: delete_dragon_action(dragon["id"]),
        )

        back_btn = ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_dragons())

        rows = [ft.Row([back_btn, ft.Container(expand=True)]),
                ft.Text(dragon.get("name", ""), size=24, weight="bold"),
                ft.Text(f"ID: {dragon.get('id', '?')}", size=14, color="grey"),
                ft.Divider()]
        for k, v in dragon.items():
            if k != "id":
                rows.append(ft.Text(f"{k.capitalize()}: {v}"))

        content = ft.Column([toolbar] + rows, spacing=12)
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_add_dragon():
        name_input   = ft.TextField(label="Nome",   hint_text="Ex: Drogon")
        color_input  = ft.TextField(label="Cor",    hint_text="Ex: Black and red")
        owner_input  = ft.TextField(label="Dono",   hint_text="Ex: Daenerys Targaryen")
        status_input = ft.TextField(label="Status", hint_text="Alive / Deceased", value="Alive")
        feedback     = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome do dragão!"
                page.update()
                return
            try:
                create_dragon(name, color_input.value.strip(),
                              owner_input.value.strip(), status_input.value.strip())
                show_dragons()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Novo Dragão", size=25, weight="bold"), ft.Divider(),
             name_input, color_input, owner_input, status_input,
             ft.Row([ft.ElevatedButton("Cadastrar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_update_dragon(dragon):
        if not dragon:
            show_dragons(); return

        name_input   = ft.TextField(label="Nome",   value=dragon.get("name", ""))
        color_input  = ft.TextField(label="Cor",    value=dragon.get("color", ""))
        owner_input  = ft.TextField(label="Dono",   value=dragon.get("owner", ""))
        status_input = ft.TextField(label="Status", value=dragon.get("status", ""))
        feedback     = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome do dragão!"
                page.update()
                return
            try:
                update_dragon(dragon["id"], name, color_input.value.strip(),
                              owner_input.value.strip(), status_input.value.strip())
                show_dragons()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Editar Dragão", size=25, weight="bold"), ft.Divider(),
             name_input, color_input, owner_input, status_input,
             ft.Row([ft.ElevatedButton("Salvar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def delete_dragon_action(dragon_id):
        if not dragon_id:
            show_dragons(); return
        try:
            delete_dragon(dragon_id)
            show_dragons()
        except Exception as err:
            render(ft.Column([build_navigation(),
                               ft.Text(f"Erro ao excluir dragão: {err}", color="red")],
                              scroll=ft.ScrollMode.AUTO))

    # ==================================================================
    # ESPADAS
    # ==================================================================
    def show_swords():
        state.current_sword = None

        view = build_swords_view(on_sword_click=show_sword_detail)
        toolbar = build_route_toolbar(
            on_get    = lambda e: show_swords(),
            on_post   = lambda e: show_add_sword(),
            on_put    = lambda e: show_update_sword(state.current_sword) if state.current_sword else None,
            on_delete = lambda e: delete_sword_action(state.current_sword["id"]) if state.current_sword else None,
            put_disabled=True,
            delete_disabled=True,
        )

        content = ft.Column(
            [ft.Text("Espadas", size=28, weight="bold"), ft.Divider(), toolbar, view],
            spacing=10,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_sword_detail(sword):
        state.current_sword = sword

        toolbar = build_route_toolbar(
            on_get    = lambda e: show_swords(),
            on_post   = lambda e: show_add_sword(),
            on_put    = lambda e: show_update_sword(sword),
            on_delete = lambda e: delete_sword_action(sword["id"]),
        )

        back_btn = ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: show_swords())

        rows = [ft.Row([back_btn, ft.Container(expand=True)]),
                ft.Text(sword.get("name", ""), size=24, weight="bold"),
                ft.Text(f"ID: {sword.get('id', '?')}", size=14, color="grey"),
                ft.Divider()]
        for k, v in sword.items():
            if k != "id":
                rows.append(ft.Text(f"{k.capitalize()}: {v}"))

        content = ft.Column([toolbar] + rows, spacing=12)
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_add_sword():
        name_input     = ft.TextField(label="Nome",     hint_text="Ex: Longclaw")
        type_input     = ft.TextField(label="Tipo",     hint_text="Ex: Valyrian Steel Bastard Sword")
        owner_input    = ft.TextField(label="Dono",     hint_text="Ex: Jon Snow")
        material_input = ft.TextField(label="Material", hint_text="Ex: Valyrian Steel")
        feedback       = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome da espada!"
                page.update()
                return
            try:
                create_sword(name, type_input.value.strip(),
                             owner_input.value.strip(), material_input.value.strip())
                show_swords()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Nova Espada", size=25, weight="bold"), ft.Divider(),
             name_input, type_input, owner_input, material_input,
             ft.Row([ft.ElevatedButton("Cadastrar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def show_update_sword(sword):
        if not sword:
            show_swords(); return

        name_input     = ft.TextField(label="Nome",     value=sword.get("name", ""))
        type_input     = ft.TextField(label="Tipo",     value=sword.get("type", ""))
        owner_input    = ft.TextField(label="Dono",     value=sword.get("owner", ""))
        material_input = ft.TextField(label="Material", value=sword.get("material", ""))
        feedback       = ft.Text("", color="red")

        def on_submit(e):
            name = name_input.value.strip()
            if not name:
                feedback.value = "Informe o nome da espada!"
                page.update()
                return
            try:
                update_sword(sword["id"], name, type_input.value.strip(),
                             owner_input.value.strip(), material_input.value.strip())
                show_swords()
            except Exception as err:
                feedback.value = f"✗ Erro: {err}"
                page.update()

        content = ft.Column(
            [ft.Text("Editar Espada", size=25, weight="bold"), ft.Divider(),
             name_input, type_input, owner_input, material_input,
             ft.Row([ft.ElevatedButton("Salvar", on_click=on_submit)],
                    alignment=ft.MainAxisAlignment.CENTER),
             feedback],
            spacing=15,
        )
        render(ft.Column([build_navigation(), content, ft.Container(expand=True)],
                         scroll=ft.ScrollMode.AUTO))

    def delete_sword_action(sword_id):
        if not sword_id:
            show_swords(); return
        try:
            delete_sword(sword_id)
            show_swords()
        except Exception as err:
            render(ft.Column([build_navigation(),
                               ft.Text(f"Erro ao excluir espada: {err}", color="red")],
                              scroll=ft.ScrollMode.AUTO))

    # ------------------------------------------------------------------
    # INÍCIO
    # ------------------------------------------------------------------
    show_characters()


if __name__ == "__main__":
    ft.app(target=main)