import pygame
from entities.player import Player
from core.constants import FPS


class Game():
    def __init__(self, window_size, debug_mode=False):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.debug_mode = debug_mode
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

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

        debug_surface = self.font.render(f"pos_x={self.player.rect.x}, pos_y={self.player.rect.y}, hb_x={
                                         self.player.hb.x}, hb_y={self.player.hb.y}", False, (255, 255, 255))
        self.screen.blit(debug_surface, (0, 0))

        debug_surface = self.font.render(f"vel_x={self.player.velocity.x:.2f}, vel_y={self.player.velocity.y:.2f}, is_grounded={
                                         self.player.is_grounded}, is_falling={self.player.is_falling}", False, (255, 255, 255))
        self.screen.blit(debug_surface, (0, 20))

        debug_surface = self.font.render(f"current_state={self.player.current_state}, spritesheet_len={
                                         len(self.player.animations[self.player.current_state].frames)}", False, (255, 255, 255))
        self.screen.blit(debug_surface, (0, 40))
