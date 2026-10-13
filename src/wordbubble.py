import pygame
import random
import os

class Bubble(pygame.sprite.Sprite):
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self, color, x, y, change_x, change_y, spritegroup, screen_width, screen_height, ball_size, font, word, hexcode):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, spritegroup)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ball_size = ball_size

        text = font.render(word, True, (0,0,0))
        textrect = text.get_rect()

        img_path = f"src/assets/emoji/{hexcode}.png"
        if not os.path.exists(img_path):
            img_path=f"src/assets/emoji/1F4A9.png"

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
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


def make_wordbubble(screen_width, screen_height, spritegroup, font, word, hexcode, x=None, y=None):
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
    ball = Bubble(colour, width, height, change_x, change_y, spritegroup, screen_width, screen_height, BALL_SIZE, font, word, hexcode)

    return ball


def mergeword(word1, word2, screenwidth, screenheight, spritegroup, font, model, emoji_map):
    midx = (word1.rect.center[0]+word2.rect.center[0])//2
    midy = (word1.rect.center[1]+word2.rect.center[1])//2
    predicted_word, hexcode = predictword(word1.word, word2.word, model, emoji_map)
    make_wordbubble(screenwidth, screenheight, spritegroup, font, predicted_word, hexcode, midx, midy)
    word1.kill()
    word2.kill()


def predictword(text1, text2, model, emoji_map):
    try:
        predictedword = model.most_similar(positive=[text1, text2])[0][0]
    except:
        predictedword = text1 + text2
    print(predictedword)

    hexcode = get_emoji(model, emoji_map, predictedword)

    return predictedword, hexcode

def get_emoji(model, emoji_map, text):

    try:
        similar_emoji = model.most_similar_to_given(text, list(emoji_map.keys()))
        print(similar_emoji)
        hexcode = emoji_map[similar_emoji]
    except:
        hexcode = "1F4A9"
    return hexcode