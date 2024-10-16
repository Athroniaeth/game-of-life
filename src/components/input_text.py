import pygame

from src import STATIC_PATH
from src.components.base import Component
from src.core.keyboard import KeyboardInfo
from src.core.mouse import MouseInfo


class InputText(Component):
    """
    Component to handle input text from the user.

    Attributes:
        text (str): The text in the input.
        active (bool): Whether the input is active.
        textbox_rect (pygame.Rect): The rectangle of the input.

        font_size (int): The size of the font.
        font_color (pygame.Color): The color of the font.
        font_path (Path): The path to the font.

        background_color (pygame.Color): The color of the background.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        active: bool = True,
        font_name: str = "Arial.ttf",
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
        """Delete last character, add character or bind the input text."""
        if self.active:
            for key in keyboard_info.keyboard_click:
                if keyboard_info.keyboard_click[key]:
                    if key == "\r":  # Enter
                        self.bind()
                    elif key == "\x08":  # Backspace
                        self.text = self.text[:-1]
                    else:
                        self.text += key

    def draw(self, screen: pygame.Surface):
        """Draw the input text on the screen."""
        if self.active:
            padding_horizontal = 20  # Todo: Make this dynamic and not hardcoded
            text = _draw_input_text(self, screen)
            padding_vertical = (self.textbox_rect.height - text.get_height()) // 2
            screen.blit(
                text,
                (
                    self.textbox_rect.x + padding_horizontal,
                    self.textbox_rect.y + padding_vertical,
                ),
            )

    def bind(self):
        """Empty the input text."""
        self.text = ""


def _draw_input_text(
    input_text: InputText,
    screen: pygame.Surface,
):
    """
    Draw the input text on the screen

    Args:
        input_text (InputText): The input text to draw.
        screen (pygame.Surface): The screen to draw on.

    Returns:
        pygame.Surface: The surface with the input text.
    """
    # Create a surface for the textbox rectangle
    textbox_surface = pygame.Surface(input_text.textbox_rect.size)

    # Fill the surface with the background color
    textbox_surface.fill(input_text.background_color)

    # Make the surface transparent
    textbox_surface.set_alpha(input_text.background_color.a)

    # Draw the surface on the screen
    screen.blit(textbox_surface, input_text.textbox_rect)

    font = pygame.Font(input_text.font_path, input_text.font_size)
    text = font.render(input_text.text, True, pygame.Color(input_text.font_color))

    return text
