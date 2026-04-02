from pygame import sprite, Rect, Vector2, transform, Surface
from core.sprite.spritesheet import Spritesheet


class Entity(sprite.Sprite):
    def __init__(self, screen: Surface, position: Vector2, size: tuple,
                 hb_size: tuple = None, hb_x_offset=0,
                 hb_y_offset=0):
        super().__init__()
        self.screen = screen

        # Paramètres de base
        self.position = position
        self.image = Surface(size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position

        # Physique
        self.velocity = Vector2(0, 0)
        self.gravity = 0          # 0 = pas affecté par la gravité
        self.is_grounded = False
        self.is_solid = True
        self.is_static = False

        # Hitbox
        self.hb_offset = (0, 0)
        self.hb_x_offset = hb_x_offset
        self.hb_y_offset = hb_y_offset
        self.hb_size = hb_size or size
        self.hb = Rect(*position, *self.hb_size)

        self.texture: Surface | None = None
        self.sync_hitbox()
        self.nb_sauts = 0
        self.max_sauts = 2
        self.is_grounded = False

    def sync_hitbox(self):
        self.hb_offset = (
            (self.rect.width - self.hb.width) // 2 + self.hb_x_offset,
            self.hb_y_offset
        )
        self.hb.bottomleft = (
            self.rect.bottomleft[0] + self.hb_offset[0],
            self.rect.bottomleft[1] + self.hb_y_offset
        )

    def apply_position(self):
        """Synchronise rect et hitbox avec self.position"""
        self.rect.bottomleft = (self.position.x, self.position.y)
        self.sync_hitbox()


class AnimableEntity(Entity):
    def __init__(self, screen: Surface, position: Vector2, size: tuple, current_state: str,
                 animations: dict[str, Spritesheet], animation_speed=0.15,
                 hitbox_size: tuple = None, hb_x_offset=0,
                 hb_y_offset=0):
        super().__init__(screen, position, size, hitbox_size, hb_x_offset, hb_y_offset)
        self.animations = animations
        self.animation_speed = animation_speed
        self.facing_right = False
        self.current_state = current_state
        self.frame_index = 0
        self.current_animation = self.animations[self.current_state]

    def set_state(self, state: str):
        if self.is_state(state):
            return
        self.current_state = state
        self.current_animation = self.animations[self.current_state]
        self.frame_index = 0
        
    def is_state(self, state: str) -> bool:
        return self.current_state and self.current_state == state

    def animate(self, speed_ratio=1):
        is_ended = self.is_animation_ended()
        if not self.current_animation.loop and is_ended:
            return
        if self.current_animation.loop and is_ended:
            self.frame_index = 0

        self.frame_index += self.current_animation.animation_speed * speed_ratio

        image = self.current_animation.frames[int(self.frame_index)]
        if self.facing_right:
            image = transform.flip(image, True, False)
        self.image = transform.scale(image, (self.rect.width, self.rect.height))
        
    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y - self.current_animation.offset_y))

    def is_animation_ended(self):
        return int(self.frame_index) >= len(self.current_animation.frames) - 1
