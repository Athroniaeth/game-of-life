import itertools
import logging
from typing import Tuple

import numpy
import pygame

from src.mouse import MouseInfo


class GridModel:
    grid: numpy.ndarray

    def __init__(self, shape: Tuple[int, int] = (16, 16)):
        self.grid = numpy.zeros(shape, dtype=int)


class GridView:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_x, self.screen_y, self.screen_height, self.screen_width = screen.get_rect()
        logging.info(f"Screen size: {self.screen_width} x {self.screen_height} at {self.screen_x}, {self.screen_y}")

    def grid_width(self, grid: numpy.ndarray):
        grid_width = grid.shape[0] * self.cell_size(grid=grid)
        min_width = min(grid_width, self.screen.width)

        return min_width

    def grid_height(self, grid: numpy.ndarray):
        grid_height = grid.shape[1] * self.cell_size(grid=grid)
        min_height = min(grid_height, self.screen.height)

        return min_height

    def cell_size(self, grid: numpy.ndarray):
        return min(self.screen.width // grid.shape[0], self.screen.height // grid.shape[1])

    def draw(self, grid: numpy.ndarray):

        cell_size = self.cell_size(grid)
        grid_width = self.grid_width(grid=grid)
        grid_height = self.grid_height(grid=grid)

        self.screen.fill("white", (self.screen_x, self.screen_y, grid_width, grid_height))
        self._draw_grid(cell_size, grid_width, grid_height)
        self._draw_cells(grid, cell_size)

    def _draw_grid(self, cell_size: int, grid_width: int, grid_height: int):

        # Dessine les lignes de manière verticale
        for i in range(0, grid_width, cell_size):
            pygame.draw.line(self.screen, "black", (i, 0), (i, grid_height))

        # Dessine la dernière ligne verticale
        pygame.draw.line(self.screen, "black", (grid_width - 1, 0), (grid_width - 1, grid_height))

        # Dessine les lignes de manière horizontale
        for i in range(0, grid_height, cell_size):
            pygame.draw.line(self.screen, "black", (0, i), (grid_width, i))

        # Dessine la dernière ligne horizontale
        pygame.draw.line(self.screen, "black", (0, grid_height - 1), (grid_width, grid_height - 1))

    def _draw_cells(self, grid: numpy.ndarray, cell_size: int):
        nbr_rows, nbr_columns = grid.shape
        generator = itertools.product(range(nbr_rows), range(nbr_columns))

        for row, column in generator:
            if grid[row][column] == 1:
                x = row * cell_size
                y = column * cell_size
                pygame.draw.rect(self.screen, "black", (x, y, cell_size, cell_size))


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

    def handle_event(self, mouse_info: MouseInfo):
        if mouse_info.left_click:
            row, column = self._get_cell_index(mouse_info.x, mouse_info.y)

            if self._is_valid_index(row, column):
                logging.info(f"Clicked on cell: {row}, {column} at {mouse_info.x}, {mouse_info.y}")
                self.model.grid[row][column] = abs(self.model.grid[row][column] - 1)

    def _get_cell_index(self, x: int, y: int):
        cell_size = self.view.cell_size(self.model.grid)
        row = x // cell_size
        column = y // cell_size
        return row, column

    def _is_valid_index(self, row: int, column: int):
        width, height = self.model.grid.shape
        conditions = (
            0 <= row < width,
            0 <= column < height,
        )

        return all(conditions)
