from dataclasses import dataclass
from typing import List

import pygame


@dataclass
class MouseInfo:
    """
    Class that holds the information about the mouse.

    Attributes:
        x (int): The x position of the mouse.
        y (int): The y position of the mouse.

        left_up (bool): Whether the left button was released.
        right_up (bool): Whether the right button was released.

        left_click (bool): Whether the left button was clicked.
        right_click (bool): Whether the right button was clicked.

        left_held (bool): Whether the left button is being held.
        right_held (bool): Whether the right button is being held.

        wheel_up (bool): Whether the wheel was scrolled up.
        wheel_down (bool): Whether the wheel was scrolled down.
    """

    x: int = 0
    y: int = 0

    left_up: bool = False
    right_up: bool = False

    left_click: bool = False
    right_click: bool = False

    left_held: bool = False
    right_held: bool = False

    wheel_up: bool = False
    wheel_down: bool = False

    @property
    def pos(self):
        return self.x, self.y

    def update(self, events: List[pygame.event.Event]):
        """
        Update the mouse information based on the events

        Args:
            events (List[pygame.event.Event]): A list of events from the user.
        """
        # Reset the values, except for the position
        self._reset()

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.x, self.y = event.pos

            # First click, held always False, after always True until release
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = not self.left_held
                    self.left_held = True

                elif event.button == 3:
                    self.right_click = not self.right_held
                    self.right_held = True

                elif event.button == 4:
                    self.wheel_up = True

                elif event.button == 5:
                    self.wheel_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_up = True
                    self.left_held = False

                elif event.button == 3:
                    self.right_up = True
                    self.right_held = False

    def _reset(self):
        """Reset the values of the mouse information."""
        self.left_up = False
        self.right_up = False

        self.left_click = False
        self.right_click = False

        self.wheel_up = False
        self.wheel_down = False
