import pygame
from entities.player import Player
from core.constants import FPS
from world.parallax import ParallaxSky
from ui.landing.intro import IntroCinematic
from ui.landing.landing_menu import LandingMenu
from ui.main_menu import MainMenu
from ui.ui_utils import blit_text
import core.constants as constants


class Game():
    def __init__(self, window_size, debug_mode=False, fullscreen=False):
        pygame.init()
    
        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(window_size)
        self.debug_mode = debug_mode
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.game_state = constants.INTRO
        self.game_difficulty = constants.DEFAULT_DIFFICULTY

        # UI
        self.intro = IntroCinematic(self.screen)
        self.landing_menu = LandingMenu(self.screen)
        self.main_menu = MainMenu(self.screen)

        # Start intro cinematic
        self.intro.start()

        self.player = None
        self.sky = None
        self.font = None

    def setup_font(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 16)

    def setup(self):
        self.setup_font()
        self.player = Player(pygame.Vector2(0, 0))
        self.sky = ParallaxSky(self.screen)

    def run(self):
        while self.isRunning:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.isRunning = False

            if self.game_state == constants.INTRO:
                # Handle intro
                if self.intro.update() == constants.INTRO_FINISHED:
                    self.game_state = constants.LANDING_MENU
                    self.landing_menu.start_music()
                self.intro.draw()

            elif self.game_state == constants.LANDING_MENU:
                # Handle landing menu
                if self.landing_menu.update() == constants.MAIN_MENU:
                    pygame.mixer.music.fadeout(1000)
                    self.game_state = constants.MAIN_MENU
                self.landing_menu.draw()

            elif self.game_state == constants.MAIN_MENU:
                # Handle main menu
                self.main_menu.draw(self.screen)
                choice = self.main_menu.check_click()
                if choice == constants.PLAYING:
                    self.game_difficulty = self.main_menu.selected_difficulty
                    self.setup()
                self.game_state = choice

            elif self.game_state == constants.PLAYING:
                # Handle playing
                self.screen.fill("black")
                if self.player:
                    self.sky.draw(self.screen, self.player.rect.x)
                    self.player.run(self.dt, self.screen)
                    self.player.draw(self.screen)
                    if self.debug_mode and self.font:
                        self.show_debug()
            elif self.game_state == constants.QUIT:
                self.isRunning = False

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