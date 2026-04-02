import pygame
from entities.base import AnimableEntity
from core.sprite.spritesheet import Spritesheet
import core.constants as constants


def load_player_animations():
    return {
        constants.IDLE: Spritesheet("assets/player/IDLE.png", 96, 96, 0.15, offset_y=-40),
        constants.WALK: Spritesheet("assets/player/WALK.png", 96, 96, 0.2, offset_y=-40),
        constants.RUN: Spritesheet("assets/player/RUN.png", 96, 96, 0.35, offset_y=-40),
        constants.JUMP_START: Spritesheet("assets/player/JUMP-START.png", 96, 96, 0.15, loop=False, offset_y=-40),
        constants.JUMP_TRANSITION: Spritesheet("assets/player/JUMP-TRANSITION.png", 96, 96, 0.15, loop=False, offset_y=-40),
        constants.JUMP: Spritesheet("assets/player/JUMP.png", 96, 96, 0.2, loop=True, offset_y=-40),
        constants.JUMP_FALL: Spritesheet("assets/player/JUMP-FALL.png", 96, 96, 0.15, loop=False, offset_y=-40),
        constants.ATTACK: Spritesheet("assets/player/ATTACK 1.png", 96, 96, 0.3, loop=False, offset_y=-40),
        constants.HURT: Spritesheet("assets/player/HURT.png", 96, 96, 0.2, loop=False, offset_y=-40),
        constants.HEALING: Spritesheet("assets/player/HEALING.png", 96, 96, 0.3, loop=False, offset_y=-40),
        constants.DASH: Spritesheet("assets/player/DASH.png", 96, 96, 0.3, loop=True, offset_y=-40)
    }

JUMP_STATES = [constants.JUMP, constants.JUMP_FALL, constants.JUMP_START, constants.JUMP_TRANSITION]

class Player(AnimableEntity):
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2):
        self.animations = load_player_animations()
        super().__init__(screen, position, (256, 256), "IDLE",
                         self.animations, hitbox_size=(40, 100))

        # Physique
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 150
        self.speed_run = 200
        self.gravity = 2000
        self.f_jump = -800
        self.is_freeze = False
        self.is_running = False
        
        # DASH
        self.is_dashing = False
        self.dash_duration = 0.2  # Durée du dash en secondes
        self.dash_cooldown = 0.5  # Temps de recharge
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.dash_speed = 1000  # Vitesse du dash
        self.can_dash = True
        self.dash_direction = 1  # 1 pour droite, -1 pour gauche

    def jump(self):
        if self.is_grounded or self.nb_sauts < self.max_sauts:
            self.velocity.y = self.f_jump
            self.nb_sauts += 1
            self.is_grounded = False  # Dès qu'on saute, on n'est plus au sol
            self.set_state(constants.JUMP)

    def attack(self):
        if self.current_state != constants.ATTACK:
            self.is_freeze = True
            self.set_state(constants.ATTACK)

    def take_damage(self, damage: int):
        self.set_state(constants.HURT)
            
    def heal(self, hp: int):
        if self.current_state != constants.HEALING:
            self.is_freeze = True
            self.set_state(constants.HEALING)

    def handle_input(self, keys) -> int:
        h_acceleration = 0


        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            h_acceleration += self.acceleration
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            h_acceleration -= self.acceleration

        # --- Logique de Saut (Double Saut) ---
        # On vérifie Z, la flèche du haut et on peut même ajouter Espace si tu veux
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            if not self.jump_pressed:
                self.jump()  # Appelle la logique de saut (sol ou air)
                self.jump_pressed = True  # Bloque l'input jusqu'au relâchement
        else:
            self.jump_pressed = False  # Autorise un nouveau saut quand la touche est lâchée

        if keys[pygame.K_SPACE]:
            self.attack()
        if keys[pygame.K_s]:
            self.take_damage(100)
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.jump()
        if keys[pygame.K_e]:
            self.heal(100)
        if keys[pygame.K_LCTRL] and self.can_dash:
            self.dash()
        self.is_running = keys[pygame.K_LSHIFT] and h_acceleration != 0

        return h_acceleration

    def move(self, h_acceleration, dt):
        """
        Update velocity of player
        """
        
        if h_acceleration != 0:
            self.velocity.x += h_acceleration * dt
        else:
            self.velocity.x *= (1 - self.friction)
            if abs(self.velocity.x) < 0.5:
                self.velocity.x = 0
                
    def dash(self):
        if self.can_dash and not self.is_dashing and not self.is_freeze:
            self.is_dashing = True
            self.can_dash = False
            self.dash_timer = 0
            self.dash_direction = 1 if self.facing_right else -1

            # Déclenche l'animation de dash
            self.set_state(constants.DASH)

            # Désactive la gravité pendant le dash
            self.gravity_enabled = False
            self.velocity.y = 0
            
    def update_dash(self, dt):
        if self.is_dashing:
            self.dash_timer += dt

            # Mouvement horizontal pendant le dash
            self.velocity.x = self.dash_speed * self.dash_direction

            # Fin du dash
            if self.dash_timer >= self.dash_duration:
                self.is_dashing = False
                self.gravity_enabled = True
                self.velocity.x = 0

                # Retour à l'animation précédente
                if self.is_grounded:
                    self.set_state(constants.IDLE)
                else:
                    self.set_state(constants.JUMP_FALL)

        # Gestion du cooldown
        if not self.can_dash:
            self.dash_cooldown_timer += dt
            if self.dash_cooldown_timer >= self.dash_cooldown:
                self.can_dash = True
                self.dash_cooldown_timer = 0

    def update_animation(self):
        """
        Update current animation
        """
        is_backward = self.velocity.x < 0
        abs_velocity_x = abs(self.velocity.x)
        can_change = self.is_animation_ended() if not self.current_animation.loop else True

        if self.velocity.x != 0:
            self.facing_right = is_backward
            
        # Gestion des états aériens
        if not self.is_grounded:
            if self.current_state in (constants.IDLE, constants.WALK, constants.RUN):
                self.set_state(constants.JUMP_START)
            elif self.current_state == constants.JUMP_START and can_change:
                self.set_state(constants.JUMP_TRANSITION)
            elif self.current_state == constants.JUMP_TRANSITION and can_change:
                if can_change or self.velocity.y > 0:
                    self.set_state(constants.JUMP_FALL)

        # Gestion au sol
        elif self.is_grounded and (can_change or self.current_state in JUMP_STATES):
            if abs_velocity_x > 0:
                self.set_state(constants.WALK if not self.is_running else constants.RUN)
            else:
                self.set_state(constants.IDLE)

        # Calcul du speed_ratio pour l'animation
        # => augmente la vitesse de l'animation en fonction de
        # la vitesse du personnage
        speed_ratio = 1
        if self.current_state == constants.WALK:
            speed_ratio = (abs_velocity_x / self.max_speed) ** 0.15
        elif self.current_state == constants.RUN:
            speed_ratio = (abs_velocity_x / (self.max_speed + self.speed_run)) ** 0.15

        self.animate(speed_ratio)


    def update(self, dt):
        keys = pygame.key.get_pressed()
        h_acceleration = self.handle_input(keys)
        
        # Gestion spécifique de certains états
        if self.current_state in (constants.ATTACK, constants.HURT, constants.HEALING):
            if self.is_animation_ended():
                self.is_freeze = False
                self.set_state(constants.IDLE)
        else:
            self.move(h_acceleration, dt)

        # Limite vitesse
        speed_limit = self.max_speed + (self.speed_run if self.is_running else 0)
        if abs(self.velocity.x) > speed_limit:
            mult = -1 if self.velocity.x < 0 else 1
            self.velocity.x = speed_limit * mult

        # Si freeze, pas de déplacement
        if self.is_freeze:
            self.velocity.x = 0

        self.update_animation()
