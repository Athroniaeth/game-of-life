import logging

import numpy
import pygame


class GridModel:
    grid: numpy.ndarray

    def __init__(self, size: int = 20):
        self.grid = numpy.zeros((size, size), dtype=int)


class GridView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.x, self.y, self.width, self.height = screen.get_rect()
        logging.info(f"Screen size: {self.width} x {self.height} started at {self.x}, {self.y}")

    def draw(self, grid: numpy.ndarray):
        self.screen.fill("white", (self.x, self.y, self.width, self.height))
        self._draw_grid(grid=grid)

    def _draw_grid(self, grid: numpy.ndarray):
        # Le nombre de colonnes devrait être identique
        cell_size = self.width // grid.shape[0]

        # Dessine les lignes de manière verticale
        for i in range(0, self.width, cell_size):
            pygame.draw.line(self.screen, "black", (i, 0), (i, self.height))

        # Dessine les lignes de manière horizontale
        for i in range(0, self.height, cell_size):
            pygame.draw.line(self.screen, "black", (0, i), (self.width, i))


class GridController:
    def __init__(
            self,
            model: GridModel,
            view: GridView,
    ):
        self.model = model
        self.view = view

    def draw(self):
        self.view.draw(self.model.grid)
