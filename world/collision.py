import pygame
from core.constants import SOLID


class CollisionSystem:
    """
    Système de collision centralisé.
    Gère la physique (gravité, déplacement) et les collisions.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.platforms = pygame.sprite.Group()    # Plateformes
        self.dynamic = pygame.sprite.Group()      # Entités qui se déplace

    def add_platform(self, *platforms):
        self.platforms.add(*platforms)

    def add_dynamic(self, *entities):
        self.dynamic.add(*entities)

    def remove(self, *entities):
        self.platforms.remove(*entities)
        self.dynamic.remove(*entities)

    def update(self, dt):
        """
        Met à jour la physique et les collisions de toutes
        les entités dynamiques.
        """
        for entity in self.dynamic:
            if entity.is_static:
                continue
            self._apply_physics(entity, dt)

    def _apply_physics(self, entity, dt):
        """
        Applique gravité + déplacement + résolution de collision
        pour une seule entité.
        """
        # Gravité
        if entity.gravity != 0:
            entity.velocity.y += entity.gravity * dt

        # Déplacement horizontal + collision
        entity.position.x += entity.velocity.x * dt
        entity.apply_position()
        self._resolve_horizontal(entity)

        # Déplacement vertical + collision
        entity.position.y += entity.velocity.y * dt
        entity.apply_position()
        self._resolve_vertical(entity, dt)

        # Limites écran
        self._clamp_to_screen(entity)

    def _resolve_horizontal(self, entity):
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

    def _resolve_vertical(self, entity, dt):
        entity.is_grounded = False

        for plat in self.platforms:
            if not entity.hb.colliderect(plat.rect):
                continue

            if plat.type == SOLID:
                if entity.velocity.y > 0:
                    entity.hb.bottom = plat.rect.top
                    entity.velocity.y = 0
                    entity.is_grounded = True
                elif entity.velocity.y < 0:
                    entity.hb.top = plat.rect.bottom
                    entity.velocity.y = 0

                self._sync_position_from_hb(entity)


    def _sync_position_from_hb(self, entity):
        """Recalcule la position de l'entité à partir de la hitbox."""
        offset_x = (entity.rect.width - entity.hb.width) // 2 + entity.hb_x_offset
        entity.position.x = entity.hb.left - offset_x
        entity.position.y = entity.hb.bottom - entity.hb_y_offset
        entity.apply_position()

    def _clamp_to_screen(self, entity):
        """
        Bloque une entité dans la surface de l'écran
        """
        
        w = self.screen.get_width()
        h = self.screen.get_height()
        changed = False

        if entity.hb.left < 0:
            entity.hb.left = 0
            entity.velocity.x = 0
            changed = True
        if entity.hb.right > w:
            entity.hb.right = w
            entity.velocity.x = 0
            changed = True
        if entity.hb.top < 0:
            entity.hb.top = 0
            entity.velocity.y = 0
            changed = True
        if entity.hb.bottom > h:
            entity.hb.bottom = h
            entity.velocity.y = 0
            entity.is_grounded = True
            changed = True

        if changed:
            self._sync_position_from_hb(entity)

    def check_overlap(self, entity_a, group) -> list:
        """
        Retourne la liste des entités d'un groupe qui chevauchent entity_a
        """
        
        hits = []
        for entity_b in group:
            if entity_a is not entity_b and entity_a.hb.colliderect(entity_b.hb):
                hits.append(entity_b)
        return hits

    def check_group_overlap(self, group_a, group_b) -> list[tuple]:
        """
        Retourne les paires (a, b) en collision entre deux groupes
        """
        
        collisions = []
        for a in group_a:
            for b in group_b:
                if a is not b and a.hb.colliderect(b.hb):
                    collisions.append((a, b))
        return collisions
