from dataclasses import dataclass
from typing import Tuple

import pygame
import typer

from src.cli import cli
from src.components.console import Console
from src.grid import GridModel, GridView, GridController
from src.core.keyboard import KeyboardInfo
from src.core.mouse import MouseInfo


@dataclass
class Game:
    """ Game class that holds the main loop and the game components. """
    cli: typer.Typer

    console: Console
    screen: pygame.Surface
    clock: pygame.time.Clock

    mouse_info: MouseInfo
    keyboard_info: KeyboardInfo

    screen_size: Tuple[int, int]

    grid_view: GridView
    grid_model: GridModel
    grid_controller: GridController

    limit_fps: int

    @classmethod
    def from_config(cls, _cli: typer.Typer, limit_fps: int = 40):
        """ Create the game instance with the minimal configuration. """
        pygame.init()

        mouse_info = MouseInfo()
        keyboard_info = KeyboardInfo()

        screen_info = pygame.display.Info()  # noqa: F841
        screen_size = (1280, 720)

        screen = pygame.display.set_mode(screen_size)
        clock = pygame.time.Clock()

        grid_model = GridModel(shape=(65, 37))
        grid_view = GridView(screen=screen)
        grid_controller = GridController(grid_model, grid_view)

        console = Console(cli, 0, 0, 1280, 720, active=False, font_size=20)

        return cls(
            cli=_cli,
            console=console,
            screen=screen,
            clock=clock,

            mouse_info=mouse_info,
            keyboard_info=keyboard_info,
            screen_size=screen_size,

            grid_view=grid_view,
            grid_model=grid_model,
            grid_controller=grid_controller,

            limit_fps=limit_fps,
        )

    def run(self):
        """
        Start the main loop of the game.

        The main loop is responsible for handling the events,
        updating the game state and drawing the game components.

        :raises SystemExit: If the user closes the window.
        :raises KeyboardInterrupt: If the user closes the window.
        :raises Exception: If the user closes the window.

        :return: None
        """
        while True:
            events = self._get_events()
            self.mouse_info.update(events)
            self.keyboard_info.update(events)

            self.screen.fill((225, 225, 225))

            if not self.console.active:
                self.grid_controller.handle_event(self.mouse_info, self.keyboard_info)

            self.grid_controller.draw()

            self.console.handle_event(self.mouse_info, self.keyboard_info)
            self.console.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.limit_fps)

    @staticmethod
    def _get_events():
        """
        Get all the events from the user and check if the user wants to quit.

        :return: List of events from the user.
        :rtype: List[pygame.event.Event]

        :raises SystemExit: If the user closes the window.
        """
        events = pygame.event.get()
        generator = (event for event in events if event.type == pygame.QUIT)
        user_ask_quit = next(generator, False)

        if user_ask_quit:
            pygame.quit()
            raise SystemExit(0)

        return events


# Todo: WARNING
# Instantiation, outside a function, allows Typer to capture the application so that it can interact with it.
# I haven't found any other way of doing this, while still allowing the CLI to be detached to create the Console.
app = Game.from_config(cli)

if __name__ == "__main__":
    app.run()
