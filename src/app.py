import pygame

from src.grid import GridModel, GridView, GridController
from src.mouse import MouseInfo


def app(fps=30):
    pygame.init()

    screen_info = pygame.display.Info()  # noqa: F841
    screen_size = (1280, 720 + 50)

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    # Reserve specific area for the grid
    screen_grid = screen.subsurface((0, 0, screen_size[0], screen_size[1] - 50))

    grid_model = GridModel(shape=(16, 9))
    grid_view = GridView(screen=screen_grid)
    grid_controller = GridController(grid_model, grid_view)

    mouse_info = MouseInfo()

    while True:
        events = _get_events()
        mouse_info.update(events)

        screen.fill((225, 225, 225))

        grid_controller.handle_event(mouse_info)
        grid_controller.draw()

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
