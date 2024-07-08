from typing import List

import pygame
import typer


class InputText:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,

            active: bool = True,
            font_name: str = 'Consolas',
            font_size: int = 24,
            font_color: str = "black",
            background_color: str = "white",
    ):
        self.input_text = ""
        self.active = active
        self.textbox_rect = pygame.Rect(x, y, width, height)

        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color

        self.background_color = background_color

    def handle_event(self, events: List[pygame.event.Event]):
        if self.active:
            for event in events:
                if event.type == pygame.TEXTINPUT:
                    self.input_text += event.text
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.bind()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]

    def draw(self, screen: pygame.Surface):
        if self.active:
            pygame.draw.rect(screen, self.background_color, self.textbox_rect)
            font = pygame.font.SysFont(self.font_name, self.font_size)
            text = font.render(self.input_text, True, pygame.Color(self.font_color))
            screen.blit(text, (self.textbox_rect.x + 5, self.textbox_rect.y + 5))

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
            font_name: str = 'Consolas',
            font_size: int = 24,
            font_color: str = "white",
            background_color: str = "black",
    ):
        super().__init__(
            x, y, width, height,
            active, font_name, font_size, font_color, background_color
        )
        self.cli = cli

    def handle_event(self, events: List[pygame.event.Event]):
        """ Key '²' is used to activate the CLI."""
        for event in events:
            if event.type == pygame.TEXTINPUT:
                if event.text == "²":
                    self.active = not self.active
                    return

        super().handle_event(events)

    def bind(self):
        try:
            commands = self.input_text.split()
            self.cli(commands)
        except SystemExit as exception:
            print(f"Exiting: {exception}")
        finally:
            super().bind()
