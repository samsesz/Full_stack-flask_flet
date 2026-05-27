class AppState:
    def __init__(self) -> None:
        self.user_id = 1
        self.characters: list[dict] = []
        self.dragons: list[dict] = []
        self.swords: list[dict] = []
        self.houses: list[dict] = []
        self.current_character: dict | None = None
        self.current_dragon: dict | None = None
        self.current_sword: dict | None = None
        self.current_house: dict | None = None
        self.feedback_message = ""
        self.feedback_type = "success"  # "success" ou "error"

    def reset_characters_state(self) -> None:
        """Limpa o estado ao voltar para a lista de personagens."""
        self.current_character = None
        self.feedback_message = ""
        self.feedback_type = "success"


state = AppState()