import pygame
from entities.player import Player
from world.ciel.parallax import ParallaxSky
from core import intro
from core import menu


class Game:
    def __init__(self, window_size):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.isRunning = True


        self.state = "CINEMATIC"

        # intro
        self.intro_scene = intro.IntroCinematic(self.screen)
        self.intro_scene.start()

        # menu
        self.menu = menu.MainMenu(self.screen)

        self.player = None
        self.sky = None

    def setup(self):

        self.player = Player((100, 100))
        self.sky = ParallaxSky(self.screen)

    def run(self):
        while self.isRunning:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False


            if self.state == "CINEMATIC":
                if self.intro_scene.update() == "FINISHED":
                    self.state = "MENU"

                    self.menu.start_music()
                self.intro_scene.draw()

            elif self.state == "MENU":
                if self.menu.update() == "START":

                    pygame.mixer.music.fadeout(1000)

                    self.setup()
                    self.state = "PLAYING"
                self.menu.draw()

            elif self.state == "PLAYING":
                self.screen.fill("black")

                # Le ciel doit être dessiné AVANT le joueur
                if self.sky and self.player:
                    self.sky.draw(self.screen, self.player.rect.x)

                if self.player:
                    self.player.run()
                    self.player.draw(self.screen)


            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()