import pygame


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()


        try:

            image_source = pygame.image.load("assets/bg/wp1.png")


            self.background = pygame.transform.scale(image_source, (self.screen_rect.width, self.screen_rect.height))


            self.background = self.background.convert()
        except pygame.error:
            print("Erreur: Image du menu introuvable. Un fond noir sera utilisé.")
            self.background = pygame.Surface(self.screen_rect.size)
            self.background.fill((10, 10, 15))


        try:
            self.title_font = pygame.font.Font("assets/fonts/font.otf", 80)
        except pygame.error:
            print("Erreur : Police introuvable. Chargement de la police par défaut.")
            self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.SysFont("Arial", 30, bold=True)

        self.title_surf = self.title_font.render("SOVEREIGN STALLION", True, (200, 0, 0))
        self.title_rect = self.title_surf.get_rect(center=(self.screen_rect.centerx, 200))

        self.shadow_surf = self.title_font.render("SOVEREIGN STALLION", True, (0, 0, 0))

        self.shadow_rect = self.shadow_surf.get_rect(center=(self.screen_rect.centerx + 4, 204))

        self.prompt_surf = self.subtitle_font.render("Appuyez sur ENTRER pour commencer", True, (0, 0, 0))
        self.prompt_rect = self.prompt_surf.get_rect(center=(self.screen_rect.centerx, 500))

        self.timer = 0

    def start_music(self):
        try:
            pygame.mixer.music.load("assets/audio/musicmenu.mp3")
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("Fichier audio du menu introuvable.")

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return "START"
        return "MENU"

    def draw(self):

        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.shadow_surf, self.shadow_rect)


        self.screen.blit(self.title_surf, self.title_rect)


        self.timer += 1
        if (self.timer // 30) % 2 == 0:
            self.screen.blit(self.prompt_surf, self.prompt_rect)