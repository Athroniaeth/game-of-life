from functools import partial
from typing import List

import pygame
import typer
from typer.testing import CliRunner

from src.components.input_text import InputText, _draw_input_text
from src.keyboard import KeyboardInfo
from src.mouse import MouseInfo

runner = CliRunner()


class Console:
    """
    Console allowing the user to interact with the application.

    Attributes:
        active (bool): Whether the console is active.
        cli (typer.Typer): The CLI application to bind to.
        input_text (InputText): The input text component.

        history (List[str]): The history of the console.
        history_limit (int): The limit of the history.
        history_font_color (pygame.Color): The color of the history font
    """
    active: bool
    cli: typer.Typer
    input_text: InputText

    history: List[str]
    history_limit: int
    history_font_color: pygame.Color

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
        self.input_text = InputText(
            x, y, width, height,
            active, font_name, font_size, font_color, background_color
        )

        self.input_text.bind = self.bind
        self.cli = cli
        self.history = []
        self.active = active
        self.history_limit = history_limit
        self.history_font_color = history_font_color

    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo):
        """ Open / Close the console by activating / deactivating components"""
        # Key '²' is used to activate the CLI. (like Skyrim :DDD)
        if keyboard_info.keyboard_click['²']:
            active = not self.active
            self.active = active
            self.input_text.active = active
            return

        self.input_text.handle_event(mouse_info, keyboard_info)

    def draw(self, screen: pygame.Surface):
        """ Draws text entry and old commands. """
        if self.active:
            text = _draw_input_text(self.input_text, screen)
            padding_horizontal = 20
            padding_vertical = screen.size[1] - self.input_text.font_size * 2
            screen.blit(text, (self.input_text.textbox_rect.x + padding_horizontal, self.input_text.textbox_rect.y + padding_vertical))

            if len(self.history) > 0:
                # Imprimer au dessus de l'input jusqu'a la limite d'affichage
                for i, line in enumerate(self.history[:-self.history_limit:-1]):
                    font = pygame.font.Font(self.input_text.font_path, self.input_text.font_size)
                    text = font.render(line, True, self.history_font_color)
                    padding_vertical = screen.size[1] - self.input_text.font_size * 1.5 - (i + 1) * self.input_text.font_size
                    screen.blit(text, (self.input_text.textbox_rect.x + padding_horizontal, self.input_text.textbox_rect.y + padding_vertical))

    def bind(self):
        """ Runs command and adds result to history. """
        result = runner.invoke(self.cli, self.input_text.text.split())
        self.history += result.stdout.split('\n')
        # Todo : Faire une deuxième limite d'historique mémoire
        # self.history = self.history[-self.history_limit:]
        self.input_text.text = ""
