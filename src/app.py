import pygame
import typer

from src.cli import cli
from src.grid import GridModel, GridView, GridController
from src.mouse import MouseInfo


class Game:
    def __init__(self, _cli: typer.Typer, limit_fps: int = 30):
        pygame.init()

        self.cli = _cli
        self.fps = limit_fps

        screen_info = pygame.display.Info()  # noqa: F841
        self.screen_size = (1280, 720)

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        self.grid_model = GridModel(shape=(16, 9))
        self.grid_view = GridView(screen=self.screen)
        self.grid_controller = GridController(self.grid_model, self.grid_view)

        self.mouse_info = MouseInfo()
        self.font = pygame.font.Font(None, 32)

    def run(self):
        while True:
            events = self._get_events()
            self.mouse_info.update(events)

            self.screen.fill((225, 225, 225))

            self.grid_controller.handle_event(self.mouse_info)
            self.grid_controller.draw()

            if self.mouse_info.left_click:
                command = "hello World azd"
                self._command(command)

            pygame.display.update()
            self.clock.tick(self.fps)

    def _command(self, command: str):
        try:
            self.cli(command.split())
        except SystemExit as exception:
            return_code = exception.code
            print("Return code:", return_code)
            if return_code != 0:
                raise Exception(f"Error while executing command: {command}") from exception

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
