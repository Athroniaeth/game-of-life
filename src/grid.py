import itertools
import logging
from collections import deque
from typing import Tuple, Optional, Set, Deque

import numpy
import pygame

from src.core.keyboard import KeyboardInfo
from src.core.mouse import MouseInfo


class GridModel:
    """
    Grid model class that holds the grid state and the game logic.

    Attributes:
        grid (numpy.ndarray): The grid of the game.
        memory_changes (Set[Tuple[int, int]]): The memory of the changes made.
        memory_color (Optional[int]): The memory of the color to use.
        history (Deque[numpy.ndarray]): The history of the grid states.
        limit_history (int): The limit of the history.

    """

    grid: numpy.ndarray
    memory_changes: Set[Tuple[int, int]]
    memory_color: Optional[int] = None

    history: Deque[numpy.ndarray]
    limit_history: int

    def __init__(self, shape: Tuple[int, int] = (16, 16), limit_history: int = 500):
        self.grid = numpy.zeros(shape, dtype=int)
        self.memory_changes = set()
        self.memory_color = None

        self.history = deque(maxlen=limit_history)
        self.limit_history = limit_history

    def toggle_cell(self, row: int, column: int):
        """
        Toggle the cell state at the given row and column.

        Notes:
            if memory_color is None, the color is set to the opposite of the current cell value.

        Args:
            row (int): The row of the cell.
            column (int): The column of the cell.

        """
        if self.memory_color is None:
            value = self.grid[row][column].item()
            self.memory_color = abs(value - 1)

        self.grid[row][column] = self.memory_color
        self.memory_changes.add((row, column))

    def reset_memory(self):
        """Reset the memory of the changes made."""
        logging.info(f"Resetting memory: {len(self.memory_changes)} changes made")
        self.memory_changes.clear()
        self.memory_color = None

    def is_valid_index(self, row: int, column: int):
        """
        Check if the row and column are valid indexes.

        Args:
            row (int): The row index.
            column (int): The column index.

        Returns:
            bool: True if the indexes are valid, False otherwise
        """
        width, height = self.grid.shape
        conditions = (
            0 <= row < width,
            0 <= column < height,
        )

        return all(conditions)

    def next_generation(self):
        """
        Generate the next generation of the grid.

        Returns:
            numpy.ndarray: The new grid state.
        """
        print(f"History: {len(self.history)}")
        self.history.append(self.grid)

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

        if numpy.array_equal(self.grid, new_grid):
            logging.info("No changes were made, the grid is stable")
            self.history.pop()

        self.grid = new_grid.copy()

    def _get_neighbors(self, row: int, column: int):
        """
        Get the neighbors of the cell at the given row and column.

        Args:
            row (int): The row of the cell.
            column (int): The column of the cell.

        Returns:
            List[int]: The list of neighbors.
        """
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
        """Clear the grid of all live cells."""
        logging.info("Clearing the grid")
        self.grid = numpy.zeros_like(self.grid)
        self.memory_changes.clear()
        self.memory_color = None

    def reshape(self, width: int, height: int):
        """
        Reshape the grid to the given width and height.

        Args:
            width (int): The new width.
            height (int): The new height.

        """
        logging.info(f"Reshaping the grid to: {width} x {height}")
        self.grid = numpy.zeros((width, height), dtype=int)
        self.memory_changes.clear()
        self.memory_color = None


class GridView:
    """
    Grid view class that holds the view of the grid.

    Attributes:
        title (str): The title of the view.
        screen (pygame.Surface): The screen to draw on.
        screen_x (int): The x coordinate of the screen.
        screen_y (int): The y coordinate of the screen.
        screen_height (int): The height of the screen.
        screen_width (int): The width of
    """

    title: str
    screen: pygame.Surface
    screen_x: int
    screen_y: int
    screen_height: int
    screen_width: int

    def __init__(self, screen: pygame.Surface):
        self.title = "Game of Life"
        self.screen = screen
        self.screen_x, self.screen_y, self.screen_height, self.screen_width = (
            screen.get_rect()
        )
        logging.info(
            f"Screen size: {self.screen_width} x {self.screen_height} at {self.screen_x}, {self.screen_y}"
        )

    def grid_width(self, grid: numpy.ndarray):
        """
        Get the width of the grid.

        Args:
            grid (numpy.ndarray): The grid to get the width from.

        Returns:
            int: The width of the grid.
        """
        grid_width = grid.shape[0] * self.cell_size(grid=grid)
        min_width = min(grid_width, self.screen.width)

        return min_width

    def grid_height(self, grid: numpy.ndarray):
        """
        Get the height of the grid.

        Args:
            grid (numpy.ndarray): The grid to get the height from.

        Returns:
            int: The height of the grid.
        """
        grid_height = grid.shape[1] * self.cell_size(grid=grid)
        min_height = min(grid_height, self.screen.height)

        return min_height

    def cell_size(self, grid: numpy.ndarray):
        """
        Get the size of the cell.

        Args:
            grid (numpy.ndarray): The grid to get the cell size from.

        Returns:
            int: The size of the cell in pixels.
        """
        return min(
            self.screen.width // grid.shape[0], self.screen.height // grid.shape[1]
        )

    def draw(self, grid: numpy.ndarray):
        """
        Draw the grid on the screen.

        Args:
            grid (numpy.ndarray): The grid to draw.

        """
        cell_size = self.cell_size(grid)
        grid_width = self.grid_width(grid=grid)
        grid_height = self.grid_height(grid=grid)

        self.screen.fill(
            "white", (self.screen_x, self.screen_y, grid_width, grid_height)
        )

        self._draw_cells(grid, cell_size)
        self._draw_grid(cell_size, grid_width, grid_height)
        self._draw_title()

    def _draw_grid(self, cell_size: int, grid_width: int, grid_height: int):
        """
        Draw the grid lines on the screen.

        Notes:
            Order of drawing is important, draw the vertical lines first then the horizontal lines.

        Args:
            cell_size (int): The size of the cell.
            grid_width (int): The width of the grid.
            grid_height (int): The height of the grid.

        """
        # Draw vertical lines
        for i in range(0, grid_width, cell_size):
            pygame.draw.line(self.screen, "black", (i, 0), (i, grid_height))

        # Draw the last vertical line
        pygame.draw.line(
            self.screen, "black", (grid_width - 1, 0), (grid_width - 1, grid_height)
        )

        # Draw horizontal lines
        for i in range(0, grid_height, cell_size):
            pygame.draw.line(self.screen, "black", (0, i), (grid_width, i))

        # Draw the last horizontal line
        pygame.draw.line(
            self.screen, "black", (0, grid_height - 1), (grid_width, grid_height - 1)
        )

    def _draw_cells(self, grid: numpy.ndarray, cell_size: int):
        """
        Draw the cells on the screen.

        Args:
            grid (numpy.ndarray): The grid to draw.
            cell_size (int): The size of the cell.

        """
        nbr_rows, nbr_columns = grid.shape
        generator = itertools.product(range(nbr_rows), range(nbr_columns))

        middle_row = [nbr_rows // 2]
        middle_column = [nbr_columns // 2]

        if nbr_rows % 2 == 0:
            middle_row += [nbr_rows // 2 - 1]

        if nbr_columns % 2 == 0:
            middle_column += [nbr_columns // 2 - 1]

        # Draw grey lines to indicate the middle (vertically, horizontally)
        for row, column in generator:
            if (row in middle_row) or (column in middle_column):
                x = row * cell_size
                y = column * cell_size
                pygame.draw.rect(
                    self.screen, (225, 225, 230), (x, y, cell_size, cell_size)
                )

            # Draw the live cells
            if grid[row][column] == 1:
                x = row * cell_size
                y = column * cell_size
                pygame.draw.rect(self.screen, "black", (x, y, cell_size, cell_size))

    def _draw_title(self):
        # Note, on garde cette façon de faire pour garder la possibilité d'afficher sur l'écran
        # Change le titre de la fenêtre pour afficher les coordonnées de la cellule survolée
        """
        Change the title of the window to display info.

        Notes:
            We keep this way of doing things to keep the possibility of displaying on the screen.
            Change the title of the window to display the coordinates of the cell hovered over.

        """
        pygame.display.set_caption(self.title)


class GridController:
    """
    Grid controller class that handles the game logic and the view.

    Attributes:
        model (GridModel): The model of the game.
        view (GridView): The view of the game.

    """

    model: GridModel
    view: GridView

    def __init__(
        self,
        model: GridModel,
        view: GridView,
    ):
        self.model = model
        self.view = view

    def draw(self):
        """Draw the grid on the screen."""
        self.view.draw(self.model.grid)

    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo):
        """
        Handle the events of the game.

        Args:
            mouse_info (MouseInfo): The mouse information.
            keyboard_info (KeyboardInfo): The keyboard information.

        """
        row, column = self._get_cell_index(mouse_info.x, mouse_info.y)
        valid_index = self.model.is_valid_index(row, column)

        # Toggle the cell
        if mouse_info.left_click and valid_index:
            logging.info(
                f"Clicked on cell: {row}, {column} at {mouse_info.x}, {mouse_info.y}"
            )
            self.model.toggle_cell(row, column)

        # Clear all cells
        elif mouse_info.right_click and valid_index:
            self.model.clear_grid()
            self.model.history.clear()

        # Maintain the left click to draw
        elif mouse_info.left_held and valid_index:
            self.model.toggle_cell(row, column)

        # Reset the memory of holding the left click
        elif mouse_info.left_up:
            self.model.reset_memory()

        # Generate the next generation
        if keyboard_info.keyboard_click[" "] or keyboard_info.keyboard_hard_held[" "]:
            self.model.next_generation()

        # Go back to the last generation
        if keyboard_info.keyboard_click["r"] or keyboard_info.keyboard_hard_held["r"]:
            if len(self.model.history) != 0:
                self.model.grid = self.model.history.pop()

        self._update_info(row, column)

    def _get_cell_index(self, x: int, y: int):
        """
        Get the cell index from the x and y coordinates

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.

        Returns:
            Tuple[int, int]: The row and column of the cell.
        """
        cell_size = self.view.cell_size(self.model.grid)
        row = x // cell_size
        column = y // cell_size
        return row, column

    def _update_info(self, row: int, column: int):
        """
        Update the title of the view with the cell hovered

        Args:
            row (int): The row of the cell.
            column (int): The column of the cell.

        Returns:
            str: The title of the view.
        """
        length_history = len(self.model.history)
        self.view.title = f"Game of Life  ("
        self.view.title += f"x={row}, y={column} - "
        self.view.title += f"history: {length_history}/{self.model.limit_history})"
