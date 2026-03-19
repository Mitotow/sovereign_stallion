import pygame
import core.constants as constants


class LandingMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        image_source = pygame.image.load("assets/ui/landing/wp1.png")
        self.background = pygame.transform.scale(image_source, (self.screen_rect.width, self.screen_rect.height))
        self.background = self.background.convert()

        self.title_font = pygame.font.Font("assets/fonts/title_font.otf", 80)
        self.subtitle_font = pygame.font.SysFont("Arial", 30, bold=True)

        self.title_surf = self.title_font.render("SOVEREIGN STALLION", True, (200, 0, 0))
        self.title_rect = self.title_surf.get_rect(center=(self.screen_rect.centerx, 200))

        self.shadow_surf = self.title_font.render("SOVEREIGN STALLION", True, (0, 0, 0))
        self.shadow_rect = self.shadow_surf.get_rect(center=(self.screen_rect.centerx + 4, 204))

        self.prompt_surf = self.subtitle_font.render("Appuyez sur ENTRER pour commencer", True, (0, 0, 0))
        self.prompt_rect = self.prompt_surf.get_rect(center=(self.screen_rect.centerx, 500))

        self.timer = 0

    def start_music(self):
        pygame.mixer.music.load("assets/audio/musicmenu.mp3")
        pygame.mixer.music.play(-1)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return constants.MAIN_MENU
        return constants.LANDING_MENU

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.shadow_surf, self.shadow_rect)
        self.screen.blit(self.title_surf, self.title_rect)
        self.timer += 1
        if (self.timer // 30) % 2 == 0:
            self.screen.blit(self.prompt_surf, self.prompt_rect)