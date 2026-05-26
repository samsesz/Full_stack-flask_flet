import flet as ft

def main(page: ft.Page):
    # Configuração da Página
    page.title = "Olá, Flet!"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Criando o Controle
    lbl_ola = ft.Text("Olá, MergeSkills!", size=40, weight="bold", color="blue")

    def on_click(e):
        lbl_ola.value = "Botão Clicado!"
        page.update() # ESSENCIAL: Avisa o Flet que algo mudou na tela

    btn = ft.Button("Clique aqui", on_click=on_click)

    # Adicionar na tela
    page.add(lbl_ola, btn)

ft.run(main)