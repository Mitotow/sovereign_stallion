def blit_texte_centre(surface, texte, rect, police, color=(255, 255, 255)):
        """Petite fonction pour centrer le texte dans un rectangle."""
        txt_surface = police.render(texte, True, color)
        txt_rect = txt_surface.get_rect()
        txt_rect.center = rect.center
        surface.blit(txt_surface, txt_rect)