import logging

import numpy
import pygame

from src.mouse import MouseInfo


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
        self._draw_cells(grid=grid)

    def _draw_grid(self, grid: numpy.ndarray):
        # Le nombre de colonnes devrait être identique
        cell_size = self.width // grid.shape[0]

        # Dessine les lignes de manière verticale
        for i in range(0, self.width, cell_size):
            pygame.draw.line(self.screen, "black", (i, 0), (i, self.height))

        # Dessine les lignes de manière horizontale
        for i in range(0, self.height, cell_size):
            pygame.draw.line(self.screen, "black", (0, i), (self.width, i))

    def _draw_cells(self, grid: numpy.ndarray):
        grid_width = grid.shape[0]
        grid_height = grid.shape[1]
        cell_size = self.width // grid_width

        generator = ((index_x, index_y) for index_x in range(grid_width) for index_y in range(grid_height))

        for index_x, index_y in generator:
            cell_x = index_x * cell_size
            cell_y = index_y * cell_size

            if grid[index_x][index_y] == 1:
                pygame.draw.rect(self.screen, "black", (cell_x, cell_y, cell_size, cell_size))


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
        cell_size = self.view.width // self.model.grid.shape[0]
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
