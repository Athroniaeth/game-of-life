from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict

import pygame


@dataclass
class KeyboardInfo:
    """
    Class that holds the information about the keyboard.

    Attributes:
        keyboard_click (Dict[str, bool]): A dictionary tracking whether each key has been clicked.
        keyboard_soft_held (Dict[str, bool]): A dictionary tracking whether each key is being softly held.
        keyboard_hard_held (Dict[str, bool]): A dictionary tracking whether each key is being hard held.
        keyboard_delay (Dict[str, float]): A dictionary storing the delay times for each key.
        delay_hard_held (int): The delay time in milliseconds for hard-held keys.
    """

    keyboard_click: Dict[str, bool] = field(default_factory=lambda: defaultdict(bool))
    keyboard_soft_held: Dict[str, bool] = field(
        default_factory=lambda: defaultdict(bool)
    )
    keyboard_hard_held: Dict[str, bool] = field(
        default_factory=lambda: defaultdict(bool)
    )

    keyboard_delay: Dict[str, float] = field(default_factory=lambda: defaultdict(float))

    delay_hard_held: int = 150

    def update(self, events: List[pygame.event.Event]):
        """
        Update the keyboard information based on the events.

        Args:
            events (List[pygame.event.Event]): A list of events from the user.
        """
        # Generator foreach key that is softly held
        generator = (
            key
            for key in self.keyboard_soft_held.keys()
            if self.keyboard_soft_held[key]
        )

        for key in generator:
            # It's not the first click
            self.keyboard_click[key] = False

            # If the key exceeds the hard delay time
            calcul = pygame.time.get_ticks() - self.keyboard_delay[key]

            if calcul > self.delay_hard_held:
                self.keyboard_hard_held[key] = True

        for event in events:
            if event.type == pygame.KEYDOWN and event.unicode != "":
                # If the key is not already held, attribute the first click
                if not self.keyboard_soft_held[event.unicode]:
                    self.keyboard_click[event.unicode] = True
                    self.keyboard_soft_held[event.unicode] = True
                    self.keyboard_delay[event.unicode] = pygame.time.get_ticks()

            # Todo : Handle special keys

            # If the key is released, reset the values
            elif event.type == pygame.KEYUP and event.unicode != "":
                self.keyboard_click[event.unicode] = False
                self.keyboard_soft_held[event.unicode] = False
                self.keyboard_hard_held[event.unicode] = False

    def _reset(self):
        """Reset the values of the keyboard information."""
        self.keyboard_click = defaultdict(bool)
        self.keyboard_soft_held = defaultdict(bool)
        self.keyboard_hard_held = defaultdict(bool)

        self.keyboard_delay = defaultdict(float)
