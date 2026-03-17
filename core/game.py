import pygame
from entities.player import Player
from ui.main_menu import MainMenu
import core.constants as constants


class Game():
    def __init__(self, window_size):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

        self.game_state = constants.MAIN_MENU
        self.game_difficulty = constants.DEFAULT_DIFFICULTY
        self.menu = MainMenu(self.screen)
        self.player = None
        self.plateforms = []

    def setup(self):
        self.player = Player(pygame.Vector2(100, 100))

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if self.game_state == constants.MAIN_MENU:
                self.menu.draw(self.screen)
                choice = self.menu.check_click()

                if choice == constants.PLAYING:
                    self.game_state = constants.PLAYING
                    self.game_difficulty = self.menu.selected_difficulty
                    self.setup()
                elif choice == constants.QUIT:
                    self.isRunning = False

            elif self.game_state == constants.PLAYING:
                self.screen.fill("black")
                if self.player:
                    self.player.run(self.plateforms)
                    self.player.draw(self.screen)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
