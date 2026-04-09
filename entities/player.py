import pygame
from entities.base import AnimableEntity
from core.sprite.spritesheet import Spritesheet
import core.constants as constants


def load_player_animations():
    return {
        constants.IDLE: Spritesheet("assets/player/IDLE.png", 96, 96, 0.15, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.WALK: Spritesheet("assets/player/WALK.png", 96, 96, 0.2, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.RUN: Spritesheet("assets/player/RUN.png", 96, 96, 0.35, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.JUMP_START: Spritesheet("assets/player/JUMP-START.png", 96, 96, 0.15, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.JUMP_TRANSITION: Spritesheet("assets/player/JUMP-TRANSITION.png", 96, 96, 0.15, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.JUMP: Spritesheet("assets/player/JUMP.png", 96, 96, 0.2, loop=True, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.JUMP_FALL: Spritesheet("assets/player/JUMP-FALL.png", 96, 96, 0.15, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.ATTACK: Spritesheet("assets/player/ATTACK 1.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.HURT: Spritesheet("assets/player/HURT.png", 96, 96, 0.2, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.HEALING: Spritesheet("assets/player/HEALING.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.DASH: Spritesheet("assets/player/DASH.png", 96, 96, 0.3, loop=True, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.WALL_SLIDE: Spritesheet("assets/player/WALL SLIDE.png", 96, 96, 0.1, loop=True, offset_y=constants.PLAYER_ANIM_OFFSET_Y)
    }


JUMP_STATES = [constants.JUMP, constants.JUMP_FALL, constants.JUMP_START, constants.JUMP_TRANSITION]


class Player(AnimableEntity):
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2):
        super().__init__(screen, position, constants.PLAYER_SIZE, constants.IDLE,
                         load_player_animations(), hitbox_size=constants.PLAYER_HB_SIZE)

        # --- SYSTÈME DE VIE ---
        self.hp = 30
        self.is_alive = True

        # Physique
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 150
        self.speed_run = 200
        self.gravity = 2000
        self.f_jump = -600
        self.is_freeze = False
        self.is_running = False

        self.nb_sauts = 0
        self.max_sauts = 2
        self.jump_pressed = False

        # Wall Jump
        self.wall_slide_speed = 120  # Vitesse max de chute quand on frotte un mur
        self.wall_jump_force_y = 500  # Force du saut vers le haut
        self.wall_jump_force_x = 400  # Force de répulsion pour s'écarter du mur
        self.wall_sensor_range = 5  # Épaisseur de la zone de détection à gauche/droite

        # États des murs
        self.on_wall_left = False
        self.on_wall_right = False
        self.is_wall_sliding = False

    def take_damage(self, amount: int):
        if not self.is_alive: return
        self.hp -= amount
        self.set_state(constants.HURT)
        print(f"PV restants : {self.hp}")
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.is_freeze = True
            print("GAME OVER")

    def jump(self):
        if self.is_grounded or self.nb_sauts < self.max_sauts:
            self.velocity.y = self.f_jump
            self.nb_sauts += 1
            self.is_grounded = False

        elif self.is_wall_sliding or self.on_wall_left or self.on_wall_right:
            if self.on_wall_left:
                # On pousse vers le haut ET vers la droite
                self.velocity.y = -self.wall_jump_force_y
                self.velocity.x = self.wall_jump_force_x

            elif self.on_wall_right:
                # On pousse vers le haut ET vers la gauche
                self.velocity.y = -self.wall_jump_force_y
                self.velocity.x = -self.wall_jump_force_x

            self.is_wall_sliding = False

            self.set_state(constants.JUMP)

    def attack(self):
        if self.current_state != constants.ATTACK:
            self.is_freeze = True
            self.set_state(constants.ATTACK)

    def handle_input(self, keys) -> int:
        if not self.is_alive: return 0
        h_acceleration = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: h_acceleration += self.acceleration
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: h_acceleration -= self.acceleration
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            if not self.jump_pressed:
                self.jump()
                self.jump_pressed = True
        else:
            self.jump_pressed = False
        if keys[pygame.K_SPACE]: self.attack()
        if keys[pygame.K_e]:
            self.heal(100)
        self.is_running = keys[pygame.K_LSHIFT] and h_acceleration != 0
        return h_acceleration

    def move(self, h_acceleration, dt):
        if h_acceleration != 0:
            self.velocity.x += h_acceleration * dt
        else:
            # Décélération linéaire fluide (basée sur le dt)
            friction_amount = self.friction * 1000 * dt
            if self.velocity.x > 0:
                self.velocity.x = max(0, self.velocity.x - friction_amount)
            elif self.velocity.x < 0:
                self.velocity.x = min(0, self.velocity.x + friction_amount)

    def check_wall_sensors(self, platforms):
        # On crée un capteur à gauche et un à droite, légèrement plus petits que la hauteur du joueur
        # pour éviter de détecter le sol comme un mur.
        left_sensor = pygame.Rect(self.hb.left - self.wall_sensor_range, self.hb.top + 5,
                                  self.wall_sensor_range, self.hb.height - 10)

        right_sensor = pygame.Rect(self.hb.right, self.hb.top + 5,
                                   self.wall_sensor_range, self.hb.height - 10)

        self.on_wall_left = False
        self.on_wall_right = False

        for plat in platforms:
            if left_sensor.colliderect(plat.rect):
                self.on_wall_left = True
            if right_sensor.colliderect(plat.rect):
                self.on_wall_right = True

    def update_animation(self, dt):
        is_backward = self.velocity.x < 0
        abs_velocity_x = abs(self.velocity.x)
        can_change = self.is_animation_ended() if not self.current_animation.loop else True

        # Orientation par défaut basée sur le mouvement
        if self.velocity.x != 0:
            self.facing_right = is_backward

        # --- TON BLOC WALL SLIDE MODIFIÉ ---
        if self.is_wall_sliding:
            self.set_state(constants.WALL_SLIDE)

            # On force le regard selon le mur touché :
            if self.on_wall_left:
                # Sur le mur de gauche, on regarde à droite
                # (Attention : selon le sens de ton image de base, tu devras peut-être mettre True ou False ici)
                self.facing_right = False

            elif self.on_wall_right:
                # Sur le mur de droite, on regarde à gauche
                self.facing_right = True
        elif not self.is_grounded:
            if self.current_state in (constants.IDLE, constants.WALK, constants.RUN):
                self.set_state(constants.JUMP_START)
            elif self.current_state == constants.JUMP_START and can_change:
                self.set_state(constants.JUMP_TRANSITION)
            elif self.current_state == constants.JUMP_TRANSITION and can_change:
                self.set_state(constants.JUMP_FALL)
        elif self.is_grounded and (can_change or self.current_state in JUMP_STATES):
            if abs_velocity_x > 0:
                self.set_state(constants.WALK if not self.is_running else constants.RUN)
            else:
                self.set_state(constants.IDLE)
        self.animate(dt)

    def update(self, dt):
        if not self.is_alive:
            self.velocity.x = 0
            self.animate(dt)
            return
        if self.is_grounded: self.nb_sauts = 0
        keys = pygame.key.get_pressed()
        h_acceleration = self.handle_input(keys)
        if self.current_state in (constants.ATTACK, constants.HURT):
            if self.is_animation_ended():
                self.is_freeze = False
                self.set_state(constants.IDLE)
        else:
            self.move(h_acceleration, dt)
        speed_limit = self.max_speed + (self.speed_run if self.is_running else 0)
        if abs(self.velocity.x) > speed_limit: self.velocity.x = speed_limit * (-1 if self.velocity.x < 0 else 1)
        if self.is_freeze: self.velocity.x = 0
        self.update_animation(dt)

        self.is_wall_sliding = False

        # Si on est en l'air et qu'on tombe (vélocité Y positive)
        if not self.is_grounded and self.velocity.y > 0:
            # On utilise h_acceleration pour savoir si le joueur POUSSE le joystick vers le mur
            if (self.on_wall_left and h_acceleration < 0) or (self.on_wall_right and h_acceleration > 0):
                self.is_wall_sliding = True

        # Si on frotte le mur, on limite la vitesse de chute
        if self.is_wall_sliding:
            if self.velocity.y > self.wall_slide_speed:
                self.velocity.y = self.wall_slide_speed

    def draw(self, camera=None):
        # 1. On récupère la position à l'écran via la caméra
        draw_rect = camera.apply(self.rect) if camera else self.rect

        # 2. Décalage visuel horizontal par défaut
        offset_x = 0

        # 3. Si on glisse, on rapproche l'image du mur pour combler les pixels transparents
        if self.current_state == constants.WALL_SLIDE:
            if self.on_wall_left:
                offset_x = -16  # Décale l'image vers la gauche
            elif self.on_wall_right:
                offset_x = 16  # Décale l'image vers la droite

        # 4. On dessine l'image avec l'offset X, et l'offset Y (déjà existant pour l'animation)
        self.screen.blit(
            self.image,
            (draw_rect.x + offset_x, draw_rect.y - self.current_animation.offset_y)
        )