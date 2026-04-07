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
        constants.JUMP_TRANSITION: Spritesheet("assets/player/JUMP-TRANSITION.png", 96, 96, 0.15, loop=False,
                                               offset_y=-40),
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

        # --- SYSTÈME DE VIE ---
        self.hp = 30
        self.is_alive = True

        # Physique
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 150
        self.speed_run = 200
        self.gravity = 2000
        self.f_jump = -800
        self.is_freeze = False
        self.is_running = False
        self.nb_sauts = 0
        self.max_sauts = 2
        self.jump_pressed = False

        # DASH
        self.is_dashing = False
        self.dash_duration = 0.2
        self.dash_cooldown = 0.5
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.dash_speed = 1000
        self.can_dash = True
        self.dash_direction = 1

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
        if keys[pygame.K_LCTRL] and self.can_dash: self.dash()
        self.is_running = keys[pygame.K_LSHIFT] and h_acceleration != 0
        return h_acceleration

    def move(self, h_acceleration, dt):
        if h_acceleration != 0:
            self.velocity.x += h_acceleration * dt
        else:
            self.velocity.x *= (1 - self.friction)
            if abs(self.velocity.x) < 0.5: self.velocity.x = 0

    def dash(self):
        if self.can_dash and not self.is_dashing and not self.is_freeze:
            self.is_dashing = True
            self.can_dash = False
            self.dash_timer = 0
            self.dash_direction = 1 if self.facing_right else -1
            self.set_state(constants.DASH)
            self.velocity.y = 0

    def update_animation(self):
        is_backward = self.velocity.x < 0
        abs_velocity_x = abs(self.velocity.x)
        can_change = self.is_animation_ended() if not self.current_animation.loop else True
        if self.velocity.x != 0: self.facing_right = is_backward
        if not self.is_grounded:
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
        self.animate()

    def update(self, dt):
        if not self.is_alive:
            self.velocity.x = 0
            self.animate()
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
        self.update_animation()