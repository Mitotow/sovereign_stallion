import pygame


class Game():
    def __init__(self, window_size):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False

            self.screen.fill("black")

            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
