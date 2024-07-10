import pygame
import typer
from typer.testing import CliRunner

from src import STATIC_PATH
from src.keyboard import KeyboardInfo
from src.mouse import MouseInfo

runner = CliRunner()


class InputText:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,

            active: bool = True,
            font_name: str = 'Arial.ttf',
            font_size: int = 32,
            font_color: pygame.Color = pygame.Color(0, 0, 0),
            background_color: pygame.Color = pygame.Color(200, 200, 200),
    ):
        self.input_text = ""
        self.active = active
        self.textbox_rect = pygame.Rect(x, y, width, height)

        self.font_size = font_size
        self.font_color = font_color
        self.font_path = STATIC_PATH / font_name

        self.background_color = background_color

        if not self.font_path.exists():
            raise FileNotFoundError(f"Font not found: '{self.font_path}'")

    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo):
        if self.active:
            for key in keyboard_info.keyboard_click:
                if keyboard_info.keyboard_click[key]:
                    if key == '\r':
                        self.bind()
                    elif key == '\x08':
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += key

    def draw(self, screen: pygame.Surface):
        if self.active:
            text = _draw_input_text(self, screen)
            padding_horizontal = 20
            padding_vertical = (self.textbox_rect.height - text.get_height()) // 2
            screen.blit(text, (self.textbox_rect.x + padding_horizontal, self.textbox_rect.y + padding_vertical))

    def bind(self):
        self.input_text = ""


class InputTextCLI(InputText):
    cli: typer.Typer

    def __init__(
            self,
            cli: typer.Typer,

            x: int = 0,
            y: int = 0,
            width: int = 1280,
            height: int = 720,

            active: bool = True,
            font_name: str = 'Consolas.ttf',
            font_size: int = 20,

            font_color: pygame.Color = pygame.Color(255, 255, 255),
            background_color: pygame.Color = pygame.Color(0, 0, 0, 200),

            history_limit: int = 30,
            history_font_color: pygame.Color = pygame.Color(220, 220, 220),
    ):
        super().__init__(
            x, y, width, height,
            active, font_name, font_size, font_color, background_color
        )
        self.cli = cli
        self.history = []
        self.history_limit = history_limit
        self.history_font_color = history_font_color

    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo):
        """ Key '²' is used to activate the CLI."""
        if keyboard_info.keyboard_click['²']:
            self.active = not self.active
            return

        super().handle_event(mouse_info, keyboard_info)

    def draw(self, screen: pygame.Surface):
        if self.active:
            text = _draw_input_text(self, screen)
            padding_horizontal = 20
            padding_vertical = screen.size[1] - self.font_size * 2
            screen.blit(text, (self.textbox_rect.x + padding_horizontal, self.textbox_rect.y + padding_vertical))

            if len(self.history) > 0:
                # Imprimer au dessus de l'input jusqu'a la limite d'affichage
                for i, line in enumerate(self.history[:-self.history_limit:-1]):
                    font = pygame.font.Font(self.font_path, self.font_size)
                    text = font.render(line, True, self.history_font_color)
                    padding_vertical = screen.size[1] - self.font_size * 1.5 - (i + 1) * self.font_size
                    screen.blit(text, (self.textbox_rect.x + padding_horizontal, self.textbox_rect.y + padding_vertical))

    def bind(self):
        result = runner.invoke(self.cli, self.input_text.split())
        self.history += result.stdout.split('\n')
        # Todo : Faire une deuxième limite d'historique mémoire
        # self.history = self.history[-self.history_limit:]
        super().bind()


def _draw_input_text(
        input_text: InputText,
        screen: pygame.Surface,
):
    # Créer une surface pour le rectangle de texte
    textbox_surface = pygame.Surface(input_text.textbox_rect.size)

    # Remplir la surface avec la couleur d'arrière-plan
    textbox_surface.fill(input_text.background_color)

    # Rendre la surface transparente
    textbox_surface.set_alpha(input_text.background_color.a)

    # Dessiner la surface sur l'écran
    screen.blit(textbox_surface, input_text.textbox_rect)

    font = pygame.Font(input_text.font_path, input_text.font_size)
    text = font.render(input_text.input_text, True, pygame.Color(input_text.font_color))

    return text
