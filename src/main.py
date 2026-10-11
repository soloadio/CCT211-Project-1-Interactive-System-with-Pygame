"""
    Project 1: Interactive System with Pygame
    Word Merger
    CCT 211
    Solomon Ador-Dionisio & Brandon Lok-tim Wong
"""
import pygame
import random
from wordbubble import *
from userinterface import *

black = (0, 0, 0)

# --- Game Classes

class Game:
    """ This class represents the Game. It contains all the game objects. """

    def __init__(self):
        """ Set up the game on creation. """

        # Initialize Pygame
        pygame.init()
        # --- Create the window
        # Set the height and width of the screen
        self.screen = pygame.display.set_mode(
            [0, 0])
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.running = False
        self.held_bubble = None
        self.offsetx = 0
        self.offsety = 0
        # Create font
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # --- Sprite lists
        # This is a list of every sprite.
        self.wordbubbles = pygame.sprite.Group()
        self.uigroup = pygame.sprite.Group()

        # --- Create the sprites
        self.textbar = TextBar(self.uigroup, self.screen_width, self.screen_height, self.font)



    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for wordbubble in self.wordbubbles:
                    if wordbubble.rect.collidepoint(event.pos):
                        self.held_bubble = wordbubble
                        wordbubble.dragging = True
                        self.offsetx = wordbubble.rect.centerx - event.pos[0]
                        self.offsety = wordbubble.rect.centery - event.pos[1]
                        break
            elif self.held_bubble is not None and event.type == pygame.MOUSEMOTION:
                self.held_bubble.rect.centerx = event.pos[0] + self.offsetx
                self.held_bubble.rect.centery = event.pos[1] + self.offsety
            elif self.held_bubble is not None and event.type == pygame.MOUSEBUTTONUP:
                self.held_bubble.dragging = False
                self.held_bubble = None
            else:
                result = self.textbar.handle_keypress(event)
                if result:
                    make_wordbubble(self.screen_width, self.screen_height, self.wordbubbles, self.font, result)

    def update(self, deltatime):
        self.wordbubbles.update(deltatime)
        self.check_merge()


    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.color.THECOLORS['white'])

        # Draw all the spites
        self.wordbubbles.draw(self.screen)
        self.uigroup.draw(self.screen)

    def check_merge(self):
        for wordbubble in self.wordbubbles.sprites():
            collisions = pygame.sprite.spritecollide(wordbubble, self.wordbubbles, False)
            for collidedwordbubble in collisions:
                if collidedwordbubble is wordbubble:
                    continue
                mergeword(wordbubble, collidedwordbubble, self.screen_width, self.screen_height, self.wordbubbles, self.font)
                if collidedwordbubble is self.held_bubble or wordbubble is self.held_bubble:
                    self.held_bubble = None
                return

    def run(self):
        self.running = True
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        deltatime = 0


        # -------- Main Program Loop -----------
        while self.running:

            # --- Event processing
            self.poll()

            # --- Handle game logic
            self.update(deltatime)

            # --- Draw a frame
            self.draw()

            # Update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit the frames per second
            deltatime = clock.tick(60)/1000


if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shuting down...")
    pygame.quit()
