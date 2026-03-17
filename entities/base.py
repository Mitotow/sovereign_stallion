from pygame import sprite, Rect, Vector2, transform, Surface
from core.sprite.spritesheet import Spritesheet


class Entity(sprite.Sprite):
    def __init__(self, position: Vector2, size: tuple,
                 hb_size: tuple = None, hb_x_offset=0,
                 hb_y_offset=0):
        super().__init__()
        self.position = position
        self.image = Surface(size)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position
        self.hb_offset = (0, 0)
        self.hb_x_offset = hb_x_offset
        self.hb_y_offset = hb_y_offset

        # Gestion de la hitbox séparée
        hb_size = hb_size or size
        self.hb = Rect(*position, *size)
        self.sync_hitbox()

    def sync_hitbox(self):
        """
        Met à jour la position de la hitbox sur la position du joueur
        """

        # Permet de garder la hitbox centrée sur la position du joueur
        self.hb_offset = (
            (self.rect.width - self.hb.width) / 2 + self.hb_x_offset,
            (self.rect.height - self.hb.height) / 2 + self.hb_y_offset
        )

        # Met à jour la position de la hitbox par rapport au joueur
        self.hb.topleft = (
            self.rect.x + self.hb_offset[0],
            self.rect.y + self.hb_offset[1]
        )


class AnimableEntity(Entity):
    def __init__(self, position: Vector2, size: tuple, current_state: str,
                 animations: dict[str, Spritesheet], animation_speed=0.15,
                 hitbox_size: tuple = None, hb_x_offset=0,
                 hb_y_offset=0):
        super().__init__(position, size, hitbox_size, hb_x_offset, hb_y_offset)
        self.animations = animations
        self.animation_speed = animation_speed
        self.current_state = current_state
        self.facing_right = False
        self.frame_index = 0
        self.animation_speed = 0.15

    def animate(self, speed_ratio=1):
        """
        Effectue le changement de sprite pour l'animation de l'entité
        """

        rect = self.rect
        animation = self.animations[self.current_state]
        self.frame_index += animation.animation_speed * speed_ratio

        if self.frame_index >= len(animation.frames):
            if not animation.loop:
                pass
            self.frame_index = 0

        image = animation.frames[int(self.frame_index)]

        if self.facing_right:
            image = transform.flip(image, True, False)

        self.image = transform.scale(image, (rect.width, rect.height))
