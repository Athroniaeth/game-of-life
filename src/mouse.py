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

    @classmethod
    def from_events(cls, events: List[pygame.event.Event]):
        x, y = 0, 0

        left_up = False
        right_up = False

        left_click = False
        right_click = False

        wheel_up = False
        wheel_down = False

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_click = True
                elif event.button == 3:
                    right_click = True
                elif event.button == 4:
                    wheel_up = True
                elif event.button == 5:
                    wheel_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_up = True
                elif event.button == 3:
                    right_up = True

        return cls(
            x=x, y=y,

            left_up=left_up,
            right_up=right_up,

            left_click=left_click,
            right_click=right_click,

            wheel_up=wheel_up,
            wheel_down=wheel_down,
        )
