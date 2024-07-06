import pygame

from src.grid import GridModel, GridView, GridController
from src.mouse import MouseInfo


class Game:
    def __init__(self, fps=30):
        pygame.init()
        self.fps = fps

        screen_info = pygame.display.Info()  # noqa: F841
        self.screen_size = (1280, 720 + 50)

        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        # Reserve specific area for the grid
        self.screen_grid = self.screen.subsurface((0, 0, self.screen_size[0], self.screen_size[1] - 50))

        self.grid_model = GridModel(shape=(16, 9))
        self.grid_view = GridView(screen=self.screen_grid)
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

