import pygame
import random

class Bubble(pygame.sprite.Sprite):
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self, color, x, y, change_x, change_y, spritegroup, screen_width, screen_height, ball_size, font, word):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, spritegroup)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ball_size = ball_size

        text = font.render(word, True, (0,0,0))
        textRect = text.get_rect()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([textRect.width, textRect.height])
        pygame.draw.rect(self.image, color, self.image.get_rect())
        textRect.center = self.image.get_rect().center

        self.image.blit(text, textRect)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.change_x = change_x
        self.change_y = change_y
        self.word = word

        self.dragging = False

    def update(self, deltatime):
        if self.dragging == True:
            return
        # TODO Move the ball's center
        self.rect.x += self.change_x*deltatime
        self.rect.y += self.change_y*deltatime

        
        # TODO Bounce the ball if needed
        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.change_x *= -1
        if self.rect.top < 0 or self.rect.bottom > self.screen_height:
            self.change_y *= -1


def make_wordbubble(screen_width, screen_height, spritegroup, font, word, x=None, y=None):
    """
    Function to make a new, random ball.
    """
    BALL_SIZE = 10
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    if x == None and y == None:
        width = random.randrange(BALL_SIZE, screen_width - BALL_SIZE)
        height = random.randrange(BALL_SIZE, screen_height - BALL_SIZE)
    else:
        width = x
        height = y
    # TODO give the ball a random colour
    colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # Speed and direction of ball
    change_x = random.randrange(50, 150)*random.choice([-1, 1])
    change_y = random.randrange(50, 150)*random.choice([-1, 1])
    ball = Bubble(colour, width, height, change_x, change_y, spritegroup, screen_width, screen_height, BALL_SIZE, font, word)

    return ball


def mergeword(word1, word2, screenwidth, screenheight, spritegroup, font):
    midx = (word1.rect.center[0]+word2.rect.center[0])//2
    midy = (word1.rect.center[1]+word2.rect.center[1])//2
    make_wordbubble(screenwidth, screenheight, spritegroup, font, predictword(word1.word, word2.word), midx, midy)
    word1.kill()
    word2.kill()


def predictword(text1, text2):
    return text1 + text2