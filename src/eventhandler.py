import pygame
from states import *
from wordbubble import *
from userinterface import *

class EventHandler:
    """
    A helper class to handle events occuring in the Game.
    """

    def __init__(self):
        pass

    def handle_click(self, pos):
        """
        Handles the clicking of pause, exit, and restart button, as well as when the user clicks and drags word bubbles.
        """
        if self.pauseButton.is_clicked(pos):
            self.handle_pause()
        if self.win:
            if self.exitButton.is_clicked(pos):
                self.state.change_state(ENDED)
            elif self.restartButton.is_clicked(pos):
                self.handle_restart()
            return
        for bubble in self.wordbubbles:
            if bubble.rect.collidepoint(pos):
                self.held_bubble = bubble
                bubble.dragging = True
                self.offsetx = bubble.rect.centerx - pos[0]
                self.offsety = bubble.rect.centery - pos[1]
                break

    def handle_pause(self):
        """
        Helper function for pause button.
        """
        if self.state.check_state(RUNNING):
            self.state.change_state(PAUSED)

        elif self.state.check_state(PAUSED):
            self.state.change_state(RUNNING)

    def handle_key(self, event):
        """
        Handles any form of keyboard input rerouting logic to userinterface specific elements.
        """
        result = self.textbar.handle_keypress(event)
        if result == pygame.K_ESCAPE:
            self.handle_pause()
        elif result and result == self.targetword:
            print("You cannot cheat.")
        elif result:
            self.score += 1
            self.score_label.set_text(f"Score: {self.score}")
            make_wordbubble(self.screen_width, self.screen_height, self.wordbubbles, self.font, result, self.wm.get_emoji(result))

    def handle_restart(self):
        """
        Resets the game to the default values.
        """
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

    def check_win(self):
        """
        Checks if the user achieved the target word, creating buttons for replayability.
        """
        if self.win:
            return
        for wordbubble in self.wordbubbles:
            if wordbubble.word == self.targetword:
                self.win = True
                self.winlabel = Label(self.uigroup, self.font, "You Win!", self.screen_width//2, self.screen_height//2)
                self.restartButton = Button(self.uigroup, self.font, "Restart", self.screen_width//2, self.screen_height//2+70)
                self.exitButton = Button(self.uigroup, self.font, "Exit", self.screen_width//2, self.screen_height//2+130)
                break

    def check_merge(self):
        """
        Handles any word bubble sprite collissions, merging accordingly.
        """
        for wordbubble in self.wordbubbles.sprites():
            collisions = pygame.sprite.spritecollide(wordbubble, self.wordbubbles, False)
            for collidedwordbubble in collisions:
                if collidedwordbubble is wordbubble:
                    continue
                merge_word(wordbubble, collidedwordbubble, self.screen_width, self.screen_height, self.wordbubbles, self.font, self.wm)
                if collidedwordbubble is self.held_bubble or wordbubble is self.held_bubble:
                    self.held_bubble = None
                return