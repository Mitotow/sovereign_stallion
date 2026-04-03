import pygame
from entities.base import AnimableEntity
from core.sprite.spritesheet import Spritesheet


def load_player_animations():
    return {
        "IDLE": Spritesheet("assets/player/idle.png", 96, 96, 0.15),
        "RUN": Spritesheet("assets/player/run.png", 96, 96, 0.35),
        "JUMP": Spritesheet("assets/player/jumpsheet.png", 96, 96, 0.2, False),
    }


class Player(AnimableEntity):
    def __init__(self, position: pygame.Vector2):
        self.animations = load_player_animations()
        super().__init__(position, (256, 256), "IDLE",
                         self.animations, hitbox_size=(75, 100))

        # deplacements
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 300
        self.gravity = 2000  # Force d'attraction
        self.f_jump = -800  # Impulsion
        self.is_grounded = False
        self.is_falling = False

    def jump(self):
        """
        Fait en sorte que le joueur saute
        """

        if self.is_grounded:
            self.velocity.y = self.f_jump
            self.is_grounded = False
            self.current_state = "JUMP"
            self.frame_index = 0

    def update_grounded(self, screen: pygame.Surface):
        """
        Vérifie si le joueur touche le sol
        """

        rect = self.rect
        if rect.bottom > screen.get_height():
            rect.bottom = screen.get_height()
            self.velocity.y = 0
            self.is_grounded = True
        else:
            self.is_falling = self.is_grounded and self.veloc

    def handle_input(self, keys) -> int:
        h_acceleration = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            h_acceleration += self.acceleration
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            h_acceleration -= self.acceleration

        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()

        return h_acceleration

    def move(self, h_acceleration, dt):
        """
        Met à jour les coordonnées du joeur en fonction de l'acceleration
        du joueur sur l'axe x
        """

        if h_acceleration != 0:
            self.velocity.x += h_acceleration * dt
        else:
            self.velocity.x *= (1 - self.friction)
            if abs(self.velocity.x) < 0.5:
                self.velocity.x = 0

    def update_animation(self):
        """
        Méthode permettant de mettre à jour l'animation.
            - Flip le sprite en fonction de la direction du joueur
            - La ratio de vitesse en fonction de la velocity du joueur
            - Changer l'animation en cours
        """

        is_backward = self.velocity.x < 0
        abs_velocity_x = abs(self.velocity.x)

        # Gestion du changement de sens du sprite
        if self.velocity.x != 0:
            self.facing_right = is_backward

        # Gestio de l'animation courante et calcul de la vitesse de
        # l'animation en fonction de la velocité
        speed_ratio = 1
        if (self.current_state == "JUMP" and self.is_grounded) or self.is_grounded:
            if abs_velocity_x > 0:
                speed_ratio = (abs_velocity_x / self.max_speed) ** 0.15
                self.current_state = "RUN"
            else:
                self.current_state = "IDLE"

        self.animate(speed_ratio)

    def run(self, dt, screen):
        keys = pygame.key.get_pressed()
        h_acceleration = self.handle_input(keys)

        # Application de la force d'attraction
        self.velocity.y += self.gravity * dt

        # Gestion des déplacements sur x + ralentissement par friction
        self.move(h_acceleration, dt)

        self.update_animation()

        # Prend en compte la limite de vitesse
        if abs(self.velocity.x) > self.max_speed:
            mult = -1 if self.velocity.x < 0 else 1
            self.velocity.x = self.max_speed * mult

        # Mise à jour de la position
        self.position.x += self.velocity.x * dt
        if not self.is_grounded:
            self.position.y += self.velocity.y * dt
        self.rect.bottomleft = (self.position.x, self.position.y)

        self.sync_hitbox()
        self.update_grounded(screen)

    def draw(self, screen):
        screen.blit(self.image, self.rect)