import itertools
import logging
from typing import Tuple, Optional, Set

import numpy
import pygame

from src.keyboard import KeyboardInfo
from src.mouse import MouseInfo


class GridModel:
    grid: numpy.ndarray
    memory_changes: Set[Tuple[int, int]]
    memory_color: Optional[int] = None

    def __init__(self, shape: Tuple[int, int] = (16, 16)):
        self.grid = numpy.zeros(shape, dtype=int)
        self.memory_changes = set()
        self.memory_color = None

    def toggle_cell(self, row: int, column: int):
        if self.memory_color is None:
            self.memory_color = abs(self.grid[row][column] - 1)

        self.grid[row][column] = self.memory_color
        self.memory_changes.add((row, column))

    def reset_memory(self):
        logging.info(f"Resetting memory: {len(self.memory_changes)} changes made")
        self.memory_changes.clear()
        self.memory_color = None

    def is_valid_index(self, row: int, column: int):
        width, height = self.grid.shape
        conditions = (
            0 <= row < width,
            0 <= column < height,
        )

        return all(conditions)

    def next_generation(self):
        new_grid = numpy.zeros_like(self.grid)
        width, height = self.grid.shape

        for row, column in itertools.product(range(width), range(height)):
            neighbors = self._get_neighbors(row, column)
            alive_neighbors = sum(neighbors)
            cell = self.grid[row][column]

            if cell == 1:
                if alive_neighbors < 2 or alive_neighbors > 3:
                    new_grid[row][column] = 0
                else:
                    new_grid[row][column] = 1
            else:
                if alive_neighbors == 3:
                    new_grid[row][column] = 1

        self.grid = new_grid

    def _get_neighbors(self, row: int, column: int):
        width, height = self.grid.shape
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                new_row = row + i
                new_column = column + j

                if 0 <= new_row < width and 0 <= new_column < height:
                    neighbors.append(self.grid[new_row][new_column])

        return neighbors

    def clear_grid(self):
        logging.info("Clearing the grid")
        self.grid = numpy.zeros_like(self.grid)
        self.memory_changes.clear()
        self.memory_color = None


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

        self._draw_cells(grid, cell_size)
        self._draw_grid(cell_size, grid_width, grid_height)

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

        middle_row = [nbr_rows // 2]
        middle_column = [nbr_columns // 2]

        if nbr_rows % 2 == 0:
            middle_row += [nbr_rows // 2 - 1]

        if nbr_columns % 2 == 0:
            middle_column += [nbr_columns // 2 - 1]

        for row, column in generator:
            # Dessine des lignes grises pour indiquer le milieu (verticalement, horizontalement)
            if (row in middle_row) or (column in middle_column):
                x = row * cell_size
                y = column * cell_size
                pygame.draw.rect(self.screen, (225, 225, 230), (x, y, cell_size, cell_size))

            # Dessine les cellules vivantes
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

    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo):
        if mouse_info.left_click:
            row, column = self._get_cell_index(mouse_info.x, mouse_info.y)

            if self.model.is_valid_index(row, column):
                logging.info(f"Clicked on cell: {row}, {column} at {mouse_info.x}, {mouse_info.y}")
                self.model.toggle_cell(row, column)

        elif mouse_info.right_click:
            self.model.clear_grid()

        elif mouse_info.left_held:
            row, column = self._get_cell_index(mouse_info.x, mouse_info.y)
            if self.model.is_valid_index(row, column):
                self.model.toggle_cell(row, column)

        elif mouse_info.left_up:
            self.model.reset_memory()

        # Si il appuie sur ESPACE
        if keyboard_info.keyboard_click[' '] or keyboard_info.keyboard_hard_held[' ']:
            self.model.next_generation()

    def _get_cell_index(self, x: int, y: int):
        cell_size = self.view.cell_size(self.model.grid)
        row = x // cell_size
        column = y // cell_size
        return row, column
