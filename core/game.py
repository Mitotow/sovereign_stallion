import pygame
from entities.player import Player
from core.constants import FPS
from ui.main_menu import MainMenu
from ui.ui_utils import blit_text
import core.constants as constants


class Game():
    def __init__(self, window_size, debug_mode=False):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.debug_mode = debug_mode
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

        self.game_state = constants.MAIN_MENU
        self.game_difficulty = constants.DEFAULT_DIFFICULTY
        self.menu = MainMenu(self.screen)
        self.player = None
        self.font = None

    def setup_font(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)

    def setup(self):
        self.setup_font()
        self.player = Player(pygame.Vector2(0, 0))

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
                    self.player.run(self.dt, self.screen)
                    self.player.draw(self.screen)

            if self.debug_mode and self.font:
                self.show_debug()
            pygame.display.flip()
            self.dt = self.clock.tick(FPS) / 1000

        pygame.quit()

    def show_debug(self):
        pygame.draw.rect(self.screen, "red", self.player.hb, 2)

        blit_text(self.screen, f"pos_x={self.player.rect.x}, pos_y={self.player.rect.y}, hb_x={self.player.hb.x}, hb_y={self.player.hb.y}", (0, 0), self.font)
        blit_text(self.screen, f"vel_x={self.player.velocity.x:.2f}, vel_y={self.player.velocity.y:.2f}, is_grounded={
            self.player.is_grounded}, is_falling={self.player.is_falling}", (0, 20), self.font)
        blit_text(self.screen, f"current_state={self.player.current_state}, spritesheet_len={
                                         len(self.player.animations[self.player.current_state].frames)}", (0, 40), self.font)
        
