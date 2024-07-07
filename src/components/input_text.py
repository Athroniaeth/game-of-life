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
    ):
        self.input_text = ""
        self.active = active
        self.textbox_rect = pygame.Rect(x, y, width, height)

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
            pygame.draw.rect(screen, "gray", self.textbox_rect)
            font = pygame.font.Font(None, 32)
            text = font.render(self.input_text, True, "black")
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
    ):
        super().__init__(x, y, width, height, active)
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
