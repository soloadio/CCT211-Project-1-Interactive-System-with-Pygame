"""
    Project 1: Interactive System with Pygame
    Word Merger
    CCT 211
    Solomon Ador-Dionisio & Brandon Lok-tim Wong
    Python 3.12.10

    Run Instructions:
    - Use Python 3.12.10
    - pip install -r requirements.txt
"""
import pygame
from wordbubble import *
from userinterface import *
from states import *
from wordmodel import *
from eventhandler import *

# --- Game Class
class Game(EventHandler):
    """ This class represents the Game. It contains all the game objects. """
    def __init__(self):
        # Pygame Window initialization
        print("For first time running, the model will be downloaded to cache.")
        pygame.init()
        self.screen = pygame.display.set_mode(
            [1400, 1000])
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # Functional properties
        self.state = States()
        self.held_bubble = None
        self.offsetx = 0
        self.offsety = 0
        self.win = False
        self.score = 0
        
        # Create font
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # Setup word prediction model
        print("Loading model... (this may take up to 30 seconds)")
        self.wm = WordModel()
        self.targetword = self.wm.setup()

        # --- Sprite lists
        self.wordbubbles = pygame.sprite.Group()
        self.uigroup = pygame.sprite.Group()

        # --- Create the sprites
        self.textbar = TextBar(self.uigroup, self.screen_width, self.screen_height, self.font)
        self.targetlabel = Label(self.uigroup, self.font, "Target Word: " + self.targetword, self.textbar.rect.centerx, self.textbar.rect.top-10)
        self.score_label = Label(self.uigroup, self.font, "Score: " + str(self.score), self.screen_width-100, 100)
        self.exitButton = None
        self.restartButton = None
        self.pauseButton = Button(self.uigroup, self.font, "Time Stop or (ESC)", 200, 100, 300, 50)
        self.winlabel = None

    def poll(self): # Polls for events and handles them accordingly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # If user clicked close
                self.state.change_state(ENDED)
            elif event.type == pygame.MOUSEBUTTONDOWN: # If the user clicked the mouse
                self.handle_click(event.pos)
            elif self.held_bubble is not None and event.type == pygame.MOUSEMOTION: # If the user is dragging a bubble
                self.held_bubble.rect.center = (event.pos[0] + self.offsetx, event.pos[1] + self.offsety)
            elif self.held_bubble is not None and event.type == pygame.MOUSEBUTTONUP:   # If the user released the mouse button
                self.held_bubble.dragging = False
                self.held_bubble = None
            else:   # If the user pressed a key
                self.handle_key(event)
    
    def update(self, deltatime):    
        # Updates the game state, including checking for win conditions 
        # and updating the word bubbles
        if self.win:
            return
        self.check_win()
        self.wordbubbles.update(deltatime)
        self.check_merge()

    def draw(self):
        # Clear the screen
        self.screen.fill(pygame.color.THECOLORS['white'])

        # Draw all the spites
        self.wordbubbles.draw(self.screen)
        self.uigroup.draw(self.screen)

    def run(self):
        self.state.change_state(RUNNING)
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        deltatime = 0

        # -------- Main Program Loop -----------
        while self.state.get_state() != ENDED:
            
            # --- Event processing
            self.poll()

            # --- Handle game logic, skips update
            if not self.state.check_state(PAUSED):
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