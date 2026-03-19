import pygame
import core.constants as constants


class IntroCinematic:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        pygame.mixer.music.load("assets/audio/audiointro.mp3")
        self.fade_duration = 10000  # durée fondu
        self.fade_surface = pygame.Surface(self.screen_rect.size)
        self.fade_surface.fill((0, 0, 0))
        self.original_image = pygame.image.load("assets/ui/landing/imageintro.png").convert_alpha()

        self.zoom_start = 1.5
        self.zoom_end = 0.5
        self.duration = 36000

        self.subtitles = [
            {"start": 5500, "end": 8500, "text": "Qu'est-ce qu'un guerrier sans son étalon ?"},
            {"start": 9500, "end": 12000, "text": "Qu'est-ce qu'un lion sans sa crinière ?"},
            {"start": 13000, "end": 16000, "text": "Qu'est ce que la pluie sans les nuages pour les transporter ?."},
            {"start": 17500, "end": 19500, "text": "Tacos ou kebab ?"},
            {"start": 21000, "end": 26000, "text": "Zélé par la quête de son fidèle destrier,"},
            {"start": 26000, "end": 33000, "text": "Ryu, notre héros est prêt à tout pour parvenir à ses fins."},
            {"start": 34000, "end": 35000, "text": "Prêt à tout pour..."},
            {"start": 36000, "end": 38000, "text": "Sovereign Stallion."}
        ]

        self.font = pygame.font.Font(None, 40)
        self.is_started = False
        self.finished = False

    def start(self):
        pygame.mixer.music.play()
        self.is_started = True

    def handle_key_pressed(self) -> bool:
        keys = pygame.key.get_pressed()
        return keys[pygame.K_ESCAPE]

    def update(self):
        if not self.is_started:
            return constants.INTRO_WAITING
        
        if self.handle_key_pressed():
            pygame.mixer.music.stop()
            self.finished = True
            return constants.INTRO_FINISHED

        current_time = pygame.mixer.music.get_pos()

        if not pygame.mixer.music.get_busy() and current_time == -1:
            self.finished = True
            return constants.INTRO_FINISHED

        return constants.INTRO_RUNNING

    def draw(self):
        current_time = pygame.mixer.music.get_pos()
        if current_time == -1:
            current_time = self.duration

        self.screen.fill((0, 0, 0))

        progress = min(current_time / self.duration, 1.0)

        current_zoom = self.zoom_start - (progress * (self.zoom_start - self.zoom_end))

        new_width = int(self.original_image.get_width() * current_zoom)
        new_height = int(self.original_image.get_height() * current_zoom)

        scaled_image = pygame.transform.smoothscale(self.original_image, (new_width, new_height))

        img_rect = scaled_image.get_rect(center=self.screen_rect.center)
        self.screen.blit(scaled_image, img_rect)

        #SOUS-TITRES
        current_text = ""

        for sub in self.subtitles:
            if sub["start"] <= current_time <= sub["end"]:
                current_text = sub["text"]
                break

        if current_text:
            text_surface = self.font.render(current_text, True, (255, 255, 255))
            shadow_surface = self.font.render(current_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(midbottom=(self.screen_rect.centerx, self.screen_rect.bottom - 50))
            shadow_rect = text_rect.copy()
            shadow_rect.move_ip(2, 2)
            self.screen.blit(shadow_surface, shadow_rect)
            self.screen.blit(text_surface, text_rect)

        if current_time < self.fade_duration:
            fade_progress = current_time / self.fade_duration
            current_alpha = int(255 - (255 * fade_progress))
            self.fade_surface.set_alpha(current_alpha)
            self.screen.blit(self.fade_surface, (0, 0))