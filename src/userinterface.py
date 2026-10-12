import pygame
import random

class TextBar(pygame.sprite.Sprite):
    """
    A textbar for the user to input words.
    """

    def __init__(self, spritegroup, screen_width, screen_height, font):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, spritegroup)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (128, 128, 128)

        self.font = font
        self.current_text = ""

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([500, 50])

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen_width//2, screen_height-100)

        self.redraw()


    def update(self, deltatime):
        pass

    def redraw(self):
        pygame.draw.rect(self.image, self.color, self.image.get_rect())
        text = self.font.render(self.current_text, True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = self.image.get_rect().center
        self.image.blit(text, textRect)

    def handle_keypress(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.current_text = self.current_text[:-1]
            elif event.key == pygame.K_RETURN:
                temp = self.current_text
                self.current_text = ""
                self.redraw()
                return temp
            elif event.unicode.isalpha():
                self.current_text+=str(event.unicode)

            self.redraw()


class Label(pygame.sprite.Sprite):
    """
    
    """
    def __init__(self, spritegroup, font, text, x, y, screen_width, screen_height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, spritegroup)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (128, 128, 128)

        self.font = font
        self.current_text = text

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([500, 50], pygame.SRCALPHA)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)

        self.set_text()

    def set_text(self):
        self.image.fill((0, 0, 0, 0))
        text = self.font.render(self.current_text, True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = self.image.get_rect().center
        self.image.blit(text, textRect)