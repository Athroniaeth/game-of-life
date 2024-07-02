from dataclasses import dataclass
from typing import List

import pygame


@dataclass
class MouseInfo:
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
        # Reset the values, except for the position
        self._reset()

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.x, self.y = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = True
                    self.left_held = True
                elif event.button == 3:
                    self.right_click = True
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
        self.left_click = False
        self.right_click = False

        self.left_up = False
        self.right_up = False

        self.wheel_up = False
        self.wheel_down = False
