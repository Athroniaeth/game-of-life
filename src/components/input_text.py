import pygame

from src import STATIC_PATH
from src.keyboard import KeyboardInfo
from src.mouse import MouseInfo


class InputText:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,

            active: bool = True,
            font_name: str = 'Arial.ttf',
            font_size: int = 32,
            font_color: pygame.Color = pygame.Color(0, 0, 0),
            background_color: pygame.Color = pygame.Color(200, 200, 200),
    ):
        self.text = ""
        self.active = active
        self.textbox_rect = pygame.Rect(x, y, width, height)

        self.font_size = font_size
        self.font_color = font_color
        self.font_path = STATIC_PATH / font_name

        self.background_color = background_color

        if not self.font_path.exists():
            raise FileNotFoundError(f"Font not found: '{self.font_path}'")

    def handle_event(self, mouse_info: MouseInfo, keyboard_info: KeyboardInfo):
        if self.active:
            for key in keyboard_info.keyboard_click:
                if keyboard_info.keyboard_click[key]:
                    if key == '\r':
                        self.bind()
                    elif key == '\x08':
                        self.text = self.text[:-1]
                    else:
                        self.text += key

    def draw(self, screen: pygame.Surface):
        if self.active:
            text = _draw_input_text(self, screen)
            padding_horizontal = 20
            padding_vertical = (self.textbox_rect.height - text.get_height()) // 2
            screen.blit(text, (self.textbox_rect.x + padding_horizontal, self.textbox_rect.y + padding_vertical))

    def bind(self):
        self.text = ""


def _draw_input_text(
        input_text: InputText,
        screen: pygame.Surface,
):
    # Créer une surface pour le rectangle de texte
    textbox_surface = pygame.Surface(input_text.textbox_rect.size)

    # Remplir la surface avec la couleur d'arrière-plan
    textbox_surface.fill(input_text.background_color)

    # Rendre la surface transparente
    textbox_surface.set_alpha(input_text.background_color.a)

    # Dessiner la surface sur l'écran
    screen.blit(textbox_surface, input_text.textbox_rect)

    font = pygame.Font(input_text.font_path, input_text.font_size)
    text = font.render(input_text.text, True, pygame.Color(input_text.font_color))

    return text
