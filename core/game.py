import pygame
from entities.player import Player


class Game():
    def __init__(self, window_size):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True
        self.player = None

    def setup(self):
        self.player = Player((0, 0))

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            self.screen.fill("black")

            if self.player:
                self.player.run()
                self.player.draw(self.screen)

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
