import pygame

from src.grid import GridModel, GridView, GridController
from src.mouse import MouseInfo


def app(fps=30):
    pygame.init()

    screen_info = pygame.display.Info()  # noqa: F841
    screen_size = (1280, 720)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    grid_model = GridModel()
    grid_view = GridView(screen=screen)
    grid_controller = GridController(grid_model, grid_view)

    while True:
        events = _get_events()
        mouse_info = MouseInfo.from_events(events)

        screen.fill((225, 225, 225))

        pygame.display.update()
        clock.tick(fps)


def _get_events():
    events = pygame.event.get()
    generator = (event for event in events if event.type == pygame.QUIT)
    user_ask_quit = next(generator, False)

    if user_ask_quit:
        pygame.quit()
        raise SystemExit(0)

    return events
