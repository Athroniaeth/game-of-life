import pygame
import typer

from src.cli import cli
from src.components.input_text import InputTextCLI
from src.grid import GridModel, GridView, GridController
from src.keyboard import KeyboardInfo
from src.mouse import MouseInfo


class Game:
    def __init__(self, _cli: typer.Typer, limit_fps: int = 30):
        pygame.init()

        self.cli = _cli
        self.fps = limit_fps

        self.mouse_info = MouseInfo()
        self.keyboard_info = KeyboardInfo()

        screen_info = pygame.display.Info()  # noqa: F841
        self.screen_size = (1280, 720)

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        self.grid_model = GridModel(shape=(65, 37))
        self.grid_view = GridView(screen=self.screen)
        self.grid_controller = GridController(self.grid_model, self.grid_view)

        self.input_text = InputTextCLI(self.cli, 0, 0, 1280, 720, active=False, font_size=20)

    def run(self):
        while True:
            events = self._get_events()
            self.mouse_info.update(events)
            self.keyboard_info.update(events)

            self.screen.fill((225, 225, 225))

            if not self.input_text.active:
                self.grid_controller.handle_event(self.mouse_info, self.keyboard_info)

            self.grid_controller.draw()

            self.input_text.handle_event(self.mouse_info, self.keyboard_info)
            self.input_text.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.fps)

    @staticmethod
    def _get_events():
        events = pygame.event.get()
        generator = (event for event in events if event.type == pygame.QUIT)
        user_ask_quit = next(generator, False)

        if user_ask_quit:
            pygame.quit()
            raise SystemExit(0)

        return events


app = Game(cli)

if __name__ == "__main__":
    app.run()
