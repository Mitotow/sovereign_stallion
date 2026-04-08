import pygame
from entities.base import AnimableEntity
from core.sprite.spritesheet import Spritesheet
import core.constants as constants


def load_player_animations():
    return {
        constants.IDLE: Spritesheet("assets/player/IDLE.png", 96, 96, 0.15, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.WALK: Spritesheet("assets/player/WALK.png", 96, 96, 0.2, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.RUN: Spritesheet("assets/player/RUN.png", 96, 96, 0.35, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.JUMP_START: Spritesheet("assets/player/JUMP-START.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.JUMP_TRANSITION: Spritesheet("assets/player/JUMP-TRANSITION.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.JUMP_FALL: Spritesheet("assets/player/JUMP-FALL.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.ATTACK: Spritesheet("assets/player/ATTACK 1.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.HURT: Spritesheet("assets/player/HURT.png", 96, 96, 0.2, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.HEALING: Spritesheet("assets/player/HEALING.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.DASH: Spritesheet("assets/player/DASH.png", 96, 96, 0.3, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y),
        constants.DEATH: Spritesheet("assets/player/DEATH.png", 96, 96, 0.15, loop=False, offset_y=constants.PLAYER_ANIM_OFFSET_Y)
    }


JUMP_STATES = [constants.JUMP_FALL, constants.JUMP_START, constants.JUMP_TRANSITION]


class Player(AnimableEntity):
    def __init__(self, screen: pygame.Surface, position: pygame.Vector2):
        super().__init__(screen, position, constants.PLAYER_SIZE, constants.IDLE,
                         load_player_animations(), hitbox_size=constants.PLAYER_HB_SIZE)

        # Health
        self.hp = 30
        self.is_alive = True
        self.can_damage = True
        self.damage_cooldown = 0

        # Physique
        self.acceleration = 2500
        self.friction = 0.4
        self.max_speed = 150
        self.speed_run = 200
        self.gravity = 2000
        self.f_jump = -600
        self.is_freeze = False
        self.is_running = False
        self.is_parring = False

        self.nb_sauts = 0
        self.jump_pressed = False

    def take_damage(self, amount: int):
        # Joueur mort ou ne peut pas prendre de damage
        if not self.is_alive or not self.can_damage: return
        
        self.hp -= amount
        self.set_state(constants.HURT)
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.is_freeze = True
        else:
            self.can_damage = False
            self.damage_cooldown = constants.PLAYER_DAM_COOLDOWN
            
    def heal(self, hp: int):
        if self.hp >= constants.PLAYER_HEAL_VALUE: return
        self.set_state(constants.HEALING)
        self.hp += hp
        if self.hp > constants.PLAYER_MAX_HP: self.hp = constants.PLAYER_MAX_HP

    def jump(self):
        if self.is_grounded or self.nb_sauts < constants.PLAYER_NB_JUMP:
            self.velocity.y = self.f_jump
            self.nb_sauts += 1
            self.is_grounded = False
            self.set_state(constants.JUMP_START)

    def attack(self):
        if self.current_state != constants.ATTACK:
            self.is_freeze = True
            self.set_state(constants.ATTACK)

    def handle_input(self, keys) -> int:
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
        if keys[pygame.K_e]: self.heal(100)
            
        self.is_running = keys[pygame.K_LSHIFT] and h_acceleration != 0
        return h_acceleration

    def move(self, h_acceleration, dt):
        if h_acceleration != 0:
            self.velocity.x += h_acceleration * dt
        else:
            self.velocity.x *= (1 - self.friction) ** (dt * constants.FPS)
            if abs(self.velocity.x) < 0.5:
                self.velocity.x = 0
    
    def update_animation(self):
        can_change = self.is_animation_ended() if not self.current_animation.loop else True
        
        # Mort
        if self.is_state(constants.DEATH):
            if can_change: self.is_alive = False
            self.animate()
            return

        # Actions bloquantes (représenté par des animations qui ne boucle pas)
        if not self.current_animation.loop and self.current_state not in JUMP_STATES and not can_change:
            self.animate()
            return

        # Mouvements / Saut
        is_backward = self.velocity.x < 0
        if self.velocity.x != 0: self.facing_right = is_backward

        if not self.is_grounded:
            # On ne déclenche JUMP_START que si on vient d'un état au sol
            if self.current_state not in JUMP_STATES:
                self.set_state(constants.JUMP_START)
            elif self.current_state == constants.JUMP_START and can_change:
                self.set_state(constants.JUMP_TRANSITION)
            elif self.current_state == constants.JUMP_TRANSITION and can_change:
                self.set_state(constants.JUMP_FALL)
        else:
            # Ground
            if abs(self.velocity.x) > 0.5:
                self.set_state(constants.WALK if not self.is_running else constants.RUN)
            else:
                self.set_state(constants.IDLE)
                
        self.animate()

    def update(self, dt):       
        if self.is_grounded: self.nb_sauts = 0
        if not self.can_damage:
            self.damage_cooldown -= 1
            if self.damage_cooldown <= 0:
                self.damage_cooldown = 0
                self.can_damage = True

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