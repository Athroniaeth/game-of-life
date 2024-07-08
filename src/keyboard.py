from collections import defaultdict
from typing import List, Dict, DefaultDict

import pygame


class KeyboardInfo:
    keyboard_click: Dict[str, bool]
    keyboard_soft_held: Dict[str, bool]
    keyboard_hard_held: Dict[str, bool]

    keyboard_delay: Dict[str, float]

    delay_hard_held: int = 150

    def __init__(self):
        self._reset()

    def update(self, events: List[pygame.event.Event]):
        # Si la touche est enfoncée
        generator = (key for key in self.keyboard_soft_held.keys() if self.keyboard_soft_held[key])
        for key in generator:
            self.keyboard_click[key] = False

            # Si la touche dépasse le temps de delay "hard"
            calcul = pygame.time.get_ticks() - self.keyboard_delay[key]

            if calcul > self.delay_hard_held:
                self.keyboard_hard_held[key] = True


        for event in events:
            if event.type == pygame.KEYDOWN and event.unicode != "":
                # Si la touche n'est pas déjà enfoncée
                if not self.keyboard_soft_held[event.unicode]:
                    self.keyboard_click[event.unicode] = True
                    self.keyboard_soft_held[event.unicode] = True
                    self.keyboard_delay[event.unicode] = pygame.time.get_ticks()

            # Todo : Gérer les touches spéciales

            # Si la touche est relâchée
            elif event.type == pygame.KEYUP and event.unicode != "":
                self.keyboard_click[event.unicode] = False
                self.keyboard_soft_held[event.unicode] = False
                self.keyboard_hard_held[event.unicode] = False

            # Après l'attribution de valeurs, on vérifie si la touche est maintenue

            # Pour chaque touche enfoncée


    def _reset(self):
        self.keyboard_click = defaultdict(bool)
        self.keyboard_soft_held = defaultdict(bool)
        self.keyboard_hard_held = defaultdict(bool)

        self.keyboard_delay = defaultdict(float)
