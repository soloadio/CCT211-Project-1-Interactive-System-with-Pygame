import pygame
from states import PAUSED


class Elements(pygame.sprite.Sprite):
    """
    Parent class for all text based elements in PYGAME.
    """
    def __init__(self, spritegroup, font, width, height, text, backgroundcolor, x, y):
        pygame.sprite.Sprite.__init__(self, spritegroup)

        self.font = font
        self.current_text = text
        self.color = backgroundcolor
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

        self.redraw()

    def redraw(self):   # Redraws the text on the surface.
        self.image.fill(self.color)
        text = self.font.render(self.current_text, True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = self.image.get_rect().center
        self.image.blit(text, textRect)

    def set_text(self, text):   # Sets the text to be displayed and redraws the surface.
        self.current_text = text
        self.redraw()


class TextBar(Elements):
    """
    A textbar for the user to input words.
    """
    def __init__(self, spritegroup, screen_width, screen_height, font):
        super().__init__(spritegroup, font, 800, 50, "", (128, 128, 128), screen_width//2, screen_height-100)

        self.set_text("Press any character and hit enter...")

    def handle_keypress(self, event):
        """
        Keyboard input specific handler.
        """
        # Handle keypresses for the textbar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.current_text == "Press any character and hit enter...":
                    return
                self.set_text(self.current_text[:-1])
                if self.current_text == "":
                    self.set_text("Press any character and hit enter...")
            elif event.key == pygame.K_RETURN:
                if self.current_text == "Press any character and hit enter...":
                    return
                temp = self.current_text
                self.set_text("Press any character and hit enter...")
                return temp
            elif event.key == pygame.K_ESCAPE:
                return pygame.K_ESCAPE
            elif event.unicode.isalpha():
                if self.current_text == "Press any character and hit enter...":
                    self.set_text("")
                self.set_text(self.current_text+str(event.unicode))


class Label(Elements):
    """
    A simple label to display text.
    """
    def __init__(self, spritegroup, font, text, x, y):
        super().__init__(spritegroup, font, 500, 50, text, (0, 0, 0, 0), x, y)


class Button(Elements):
    """
    A simple button to display text.
    """
    def __init__(self, spritegroup, font, text, x, y, width=200, height=50):
        super().__init__(spritegroup, font, width, height, text, (211, 211, 211), x, y)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)