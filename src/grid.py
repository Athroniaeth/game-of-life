import pygame


class GridModel:
    def __init__(self):
        ...


class GridView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen


class GridController:
    def __init__(self, model: GridModel, view: GridView):
        self.model = model
        self.view = view
