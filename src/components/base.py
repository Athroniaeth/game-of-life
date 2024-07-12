from abc import ABC, abstractmethod

import pygame

from src.core.keyboard import KeyboardInfo
from src.core.mouse import MouseInfo


class Component(ABC):
    """ Interface for all components. """

    @abstractmethod
    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo) -> None:
        """ Handle the pygame events for the component. """
        raise NotImplementedError("Method 'handle_event' must be implemented.")

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """ Draw the component on the screen. """
        raise NotImplementedError("Method 'draw' must be implemented.")

    @abstractmethod
    def bind(self) -> None:
        """ Function to be launched at a specific time. """
        raise NotImplementedError("Method 'bind' must be implemented.")
