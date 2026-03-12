from core.spritesheet import Spritesheet
from entities.base import AnimableEntity
import pygame


def load_player_animations() -> dict[str, Spritesheet]:
    return {
        "IDLE": Spritesheet("assets/player/IDLE.png", 96, 96, 0.15),
        "RUN":  Spritesheet("assets/player/RUN.png", 96, 96, 0.35),
    }


class Player(AnimableEntity):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, (256, 256), "IDLE",
                         load_player_animations(), hitbox_size=(75, 100),
                         hb_y_offset=20)
        # largeur, hauteur du personnage
        self.image = pygame.Surface((self.rect.width, self.rect.height))

        # deplacements
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 300
        self.gravity = 2000  # Force d'attraction
        self.f_jump = -450  # Impulsion
        self.is_grounded = False

    def jump(self):
        if self.is_grounded:
            self.velocity.y = self.f_jump
            self.is_grounded = False

    def update_grounded(self, screen: pygame.Surface):
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.velocity.y = 0
            self.is_grounded = True

    def run(self, dt, screen):
        keys = pygame.key.get_pressed()
        h_acceleration = 0  # init acceleration à 0

        # Gestion des inputs
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            h_acceleration += self.acceleration
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            h_acceleration -= self.acceleration
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()

        # Application de la force d'attraction
        self.velocity.y += self.gravity * dt

        # Gestion des déplacements sur x + ralentissement par friction
        if h_acceleration != 0:
            self.velocity.x += h_acceleration * dt
        else:
            self.velocity.x *= (1 - self.friction)
            if abs(self.velocity.x) < 0.5:
                self.velocity.x = 0

        is_backward = self.velocity.x < 0
        abs_velocity_x = abs(self.velocity.x)

        # Gestion du changement de sens du sprite
        if self.velocity.x != 0:
            self.facing_right = is_backward

        # Gestio de l'animation courante et calcul de la vitesse de
        # l'animation en fonction de la velocité
        speed_ratio = 1
        if abs_velocity_x > 0:
            speed_ratio = (abs_velocity_x / self.max_speed) ** 0.15
            self.current_state = "RUN"
        else:
            self.current_state = "IDLE"

        # Prend en compte la limite de vitesse
        if abs(self.velocity.x) > self.max_speed:
            mult = -1 if is_backward else 1
            self.velocity.x = self.max_speed * mult

        # Mise à jour de la position
        self.position.x += self.velocity.x * dt
        if not self.is_grounded:
            self.position.y += self.velocity.y * dt
        self.rect.bottomleft = (self.position.x, self.position.y)

        self.sync_hitbox()
        self.update_grounded(screen)
        self.animate(speed_ratio)

    def draw(self, screen, debug_mode):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, "red", self.hb, 2)
