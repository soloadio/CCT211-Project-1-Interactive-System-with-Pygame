import pygame
import random
import os

class Bubble(pygame.sprite.Sprite):
    """
    Class to keep track of a bubble's location and vector.
    """

    def __init__(self, x, y, change_x, change_y, spritegroup, screen_width, screen_height, ball_size, font, word, hexcode):
        pygame.sprite.Sprite.__init__(self, spritegroup)

        # Functional properties
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ball_size = ball_size
        self.change_x = change_x
        self.change_y = change_y
        self.word = word
        self.dragging = False

        text = font.render(word, True, (0,0,0))
        textrect = text.get_rect()

        img_path = f"src/assets/emoji/{hexcode}.png" # Defaults to poop emoji if emoji does not exist in the assets
        if not os.path.exists(img_path):
            img_path=f"src/assets/emoji/1F4A9.png"

        # Initiates emoji image for text
        self.emoji = pygame.image.load(img_path).convert_alpha()
        self.emoji = pygame.transform.smoothscale(self.emoji, (64, 64))
        width = max(self.emoji.get_width(), textrect.width)
        gap = 4
        height = self.emoji.get_height() + gap + textrect.height
        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        emojirect = self.emoji.get_rect()
        emojirect.midtop = (width // 2, 0)
        self.image.blit(self.emoji, emojirect)
        textrect.midbottom = (width // 2, height)
        self.image.blit(text, textrect)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, deltatime):
        if self.dragging == True:
            return

        # Bounces the word on edges
        self.rect.x += self.change_x*deltatime
        self.rect.y += self.change_y*deltatime

        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.change_x *= -1
        if self.rect.top < 0 or self.rect.bottom > self.screen_height:
            self.change_y *= -1

        # Clamps the word bubble in the display
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

def make_wordbubble(screen_width, screen_height, spritegroup, font, word, hexcode, x=None, y=None):
    """
    Function to make a new, random word Bubble
    """
    BALL_SIZE = 10
    # Starting position of the word bubble.
    # Take into account the word bubble size so we don't spawn on the edge.
    if x == None and y == None:
        width = random.randrange(BALL_SIZE, screen_width - BALL_SIZE)
        height = random.randrange(BALL_SIZE, screen_height - BALL_SIZE)
    else:
        width = x
        height = y

    # Speed and direction of Bubble
    change_x = random.randrange(50, 150)*random.choice([-1, 1])
    change_y = random.randrange(50, 150)*random.choice([-1, 1])
    ball = Bubble(width, height, change_x, change_y, spritegroup, screen_width, screen_height, BALL_SIZE, font, word, hexcode)

    return ball


def merge_word(word1, word2, screenwidth, screenheight, spritegroup, font, model):
    # Merges two words into a new word bubble
    midx = (word1.rect.center[0]+word2.rect.center[0])//2
    midy = (word1.rect.center[1]+word2.rect.center[1])//2
    predicted_word, hexcode = model.predict_word(word1.word, word2.word)
    make_wordbubble(screenwidth, screenheight, spritegroup, font, predicted_word, hexcode, midx, midy)
    word1.kill()
    word2.kill()
