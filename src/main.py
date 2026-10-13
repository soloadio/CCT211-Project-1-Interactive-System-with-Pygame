"""
    Project 1: Interactive System with Pygame
    Word Merger
    CCT 211
    Solomon Ador-Dionisio & Brandon Lok-tim Wong
    Python 3.12.10
"""
import pygame
from wordbubble import *
from userinterface import *
from states import *
import gensim.downloader as api
from wonderwords import RandomWord
import json
import os

# --- Game Classes

class Game:
    """ This class represents the Game. It contains all the game objects. """
    def __init__(self):
        """ Set up the game on creation. """

        # Initialize Pygame
        print("Loading model... (this may take up to 30 seconds)")
        pygame.init()
        # --- Create the window
        # Set the height and width of the screen
        self.screen = pygame.display.set_mode(
            [1400, 1000])
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.state = States()
        self.held_bubble = None
        self.offsetx = 0
        self.offsety = 0
        
        # Create font
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # Setup word prediction model
        self.model = api.load("glove-wiki-gigaword-50")

        self.emoji_map = self.setup_emoji()

        # Setup goals
        self.rw = RandomWord()
        self.targetword = self.rw.word()
        self.win = False
        self.score = 0

        # --- Sprite lists
        # This is a list of every sprite.
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

    def restart(self):
        self.exitButton.kill()
        self.restartButton.kill()
        self.winlabel.kill()
        self.wordbubbles.empty()
        self.win = False
        self.held_bubble = None
        self.targetword = self.rw.word()
        self.targetlabel.set_text("Target: " + self.targetword)
        self.score = 0
        self.score_label.set_text("Score: " + str(self.score))
        self.exitButton = None
        self.restartButton = None
        self.winlabel = None


    def setup_emoji(self):
        with open("src/assets/openmoji.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        emoji_map = {}
        for emoji in data:
            if "-" in emoji["hexcode"]: # skip the different skin tone
                continue
            words = emoji["annotation"].lower().split()
            model_known = []
            for word in words:
                if word.isalpha() and word in self.model:
                    model_known.append(word)

            if len(model_known) == 0:
                continue
            elif len(model_known) == 1 and model_known[0] not in emoji_map:
                emoji_map[model_known[0]] = emoji["hexcode"]
            else:
                for knownwords in model_known:
                    if knownwords not in emoji_map:
                        emoji_map[knownwords] = emoji["hexcode"]

        return emoji_map

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state.change_state(ENDED)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.pauseButton.is_clicked(event.pos):
                    if self.state.check_state(PAUSED):
                        self.state.change_state(RUNNING)
                    elif self.state.check_state(RUNNING):
                        self.state.change_state(PAUSED)
                if self.win:
                    if self.exitButton.is_clicked(event.pos):
                        self.state.change_state(ENDED)
                    elif self.restartButton.is_clicked(event.pos):
                        self.restart()
                    continue
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
                if result == pygame.K_ESCAPE:
                    if self.state.check_state(RUNNING):
                        self.state.change_state(PAUSED)
                    else:
                        self.state.change_state(RUNNING)
                elif result:
                    if result == self.targetword:
                        print("You cannot cheat.")
                    else:
                        self.score += 1
                        self.score_label.set_text("Score: " + str(self.score))
                        make_wordbubble(self.screen_width, self.screen_height, self.wordbubbles, self.font, result, get_emoji(self.model, self.emoji_map, result))
    def update(self, deltatime):
        if self.win:
            return
        self.checkwin()
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
                mergeword(wordbubble, collidedwordbubble, self.screen_width, self.screen_height, self.wordbubbles, self.font, self.model, self.emoji_map)
                if collidedwordbubble is self.held_bubble or wordbubble is self.held_bubble:
                    self.held_bubble = None
                return

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

    def checkwin(self):
        if self.win:
            return
        for wordbubble in self.wordbubbles:
            if wordbubble.word == self.targetword:
                self.win = True
                self.winlabel = Label(self.uigroup, self.font, "You Win!", self.screen_width//2, self.screen_height//2)
                self.restartButton = Button(self.uigroup, self.font, "Restart", self.screen_width//2, self.screen_height//2+70)
                self.exitButton = Button(self.uigroup, self.font, "Exit", self.screen_width//2, self.screen_height//2+130)
                break
 




if __name__ == '__main__':
    g = Game()
    print("starting...")
    g.run()
    print("shuting down...")
    pygame.quit()