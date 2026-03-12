import pygame
from entities.player import Player


class Game():
    def __init__(self, window_size, debug_mode=False):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.debug_mode = debug_mode
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.player = None
        self.list_sprites = pygame.sprite.Group()

    def setup(self):
        self.player = Player(pygame.Vector2(0, 0))
        self.list_sprites.add(self.player)

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            self.screen.fill("black")

            if self.player:
                self.player.run(self.dt, self.screen)
                self.player.draw(self.screen, self.debug_mode)

            # self.list_sprites.update()
            # self.list_sprites.draw(self.screen)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
