import pygame

from src.grid import GridModel, GridView, GridController
from src.mouse import MouseInfo


class App:
    def __init__(self, limit_fps: int = 30):
        pygame.init()
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


# Injection de dépendances
app = App()

if __name__ == "__main__":
    app.run()
