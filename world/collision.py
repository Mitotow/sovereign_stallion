import pygame
from core.constants import SOLID
from entities.base import Entity
from world.platform import Platform
from core.camera import Camera

class CollisionSystem:
    """
    Système de collision centralisé.
    Gère la physique (gravité, déplacement) et les collisions.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.platforms: list[Platform] = []       # Plateformes
        self.dynamic = pygame.sprite.Group()      # Entités qui se déplace


    def set_platforms(self, platforms):
        self.platforms = platforms

    def add_dynamic(self, *entities):
        self.dynamic.add(*entities)

    def update(self, dt):
        for entity in self.dynamic:
            if entity.is_static:
                continue
            self._apply_gravity(entity, dt)
            self._move_and_resolve(entity, dt)

    def _apply_gravity(self, entity, dt):
        if entity.gravity != 0:
            entity.velocity.y += entity.gravity * dt

    def _move_and_resolve(self, entity, dt):
        # Horizontal

        entity.position.x += entity.velocity.x * dt
        entity.apply_position()
        self._resolve_entity_vs_platforms_x(entity)

        # Déplacement vertical
        entity.position.y += entity.velocity.y * dt
        entity.apply_position()
        self._resolve_entity_vs_platforms_y(entity)

    def _resolve_entity_vs_platforms_x(self, entity):
        for plat in self.platforms:
            if not entity.hb.colliderect(plat.rect):
                continue
            if plat.type == SOLID:
                if entity.velocity.x > 0:
                    entity.hb.right = plat.rect.left
                elif entity.velocity.x < 0:
                    entity.hb.left = plat.rect.right
                entity.velocity.x = 0
                self._sync_position_from_hb(entity)

    def _resolve_entity_vs_platforms_y(self, entity):
        entity.is_grounded = False
        for plat in self.platforms:
            if not entity.hb.colliderect(plat.rect):
                continue
            if plat.type == SOLID:
                if entity.velocity.y > 0:
                    entity.hb.bottom = plat.rect.top
                    entity.is_grounded = True
                elif entity.velocity.y < 0:
                    entity.hb.top = plat.rect.bottom
                entity.velocity.y = 0
                self._sync_position_from_hb(entity)

    def check_overlap(self, entity_a, group) -> list:
        return [b for b in group if entity_a is not b 
                and entity_a.hb.colliderect(b.hb)]

    def check_group_overlap(self, group_a, group_b) -> list[tuple]:
        return [(a, b) for a in group_a for b in group_b 
                if a is not b and a.hb.colliderect(b.hb)]

    def _sync_position_from_hb(self, entity):
        offset_x = (entity.rect.width - entity.hb.width) // 2 + entity.hb_x_offset
        entity.position.x = entity.hb.left - offset_x
        entity.position.y = entity.hb.bottom - entity.hb_y_offset
        entity.apply_position()

    def _clamp_to_screen(self, entity):
        """
        Empêche les entités de sortir, SAUF les projectiles.
        """
        w, h = self.screen.get_size()
        # --- LA CORRECTION EST ICI ---
        # Si c'est un projectile, on arrête la fonction tout de suite
        # pour le laisser sortir et être détruit par son propre update()
        if entity.__class__.__name__ == "Projectile":
            return

        changed = False
        if entity.hb.left < 0:
            entity.hb.left = 0; entity.velocity.x = 0; changed = True
        if entity.hb.right > w:
            entity.hb.right = w; entity.velocity.x = 0; changed = True
        if entity.hb.top < 0:
            entity.hb.top = 0; entity.velocity.y = 0; changed = True
        if entity.hb.bottom > h:
            entity.hb.bottom = h; entity.velocity.y = 0
            entity.is_grounded = True; changed = True
        if changed:
            self._sync_position_from_hb(entity)

    def check_hover_dynamic(self, pos: tuple[int, int], camera: Camera) -> Entity | None:
        return next((e for e in self.dynamic if camera.apply(e.hb).collidepoint(pos)), None)

    def remove(self, *entities):
        for e in entities:
            self.dynamic.remove(e)
