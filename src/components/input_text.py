import pygame
import typer

from src import STATIC_PATH
from src.keyboard import KeyboardInfo
from src.mouse import MouseInfo


class InputText:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,

            active: bool = True,
            font_name: str = 'Arial',
            font_size: int = 32,
            font_color: pygame.Color = pygame.Color(0, 0, 0),
            background_color: pygame.Color = pygame.Color(200, 200, 200),
    ):
        self.input_text = ""
        self.active = active
        self.textbox_rect = pygame.Rect(x, y, width, height)

        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color

        self.background_color = background_color

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
            # Créer une surface pour le rectangle de texte
            textbox_surface = pygame.Surface(self.textbox_rect.size)

            # Remplir la surface avec la couleur d'arrière-plan
            textbox_surface.fill(self.background_color)

            # Rendre la surface transparente
            textbox_surface.set_alpha(self.background_color.a)

            # Dessiner la surface sur l'écran
            screen.blit(textbox_surface, self.textbox_rect)

            font = pygame.Font(STATIC_PATH / 'Inconsolata.ttf', self.font_size)
            text = font.render(self.input_text, True, pygame.Color(self.font_color))

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

            x: int,
            y: int,
            width: int,
            height: int,

            active: bool = True,
            font_name: str = 'Inconsolata.ttf',
            font_size: int = 32,

            font_color: pygame.Color = pygame.Color(255, 255, 255),
            background_color: pygame.Color = pygame.Color(0, 0, 0, 170),
    ):
        super().__init__(
            x, y, width, height,
            active, font_name, font_size, font_color, background_color
        )
        self.cli = cli

    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo):
        """ Key '²' is used to activate the CLI."""
        if keyboard_info.keyboard_click['²']:
            self.active = not self.active
            return

        super().handle_event(mouse_info, keyboard_info)

    def bind(self):
        try:
            commands = self.input_text.split()
            self.cli(commands)
        except SystemExit as exception:
            print(f"Exiting: {exception}")
        finally:
            super().bind()
