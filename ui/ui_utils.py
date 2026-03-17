def blit_text_center(surface, text, rect, police, color=(255, 255, 255)):
        """ Centrer le texte dans un rectangle. """
        txt_surface = police.render(text, True, color)
        txt_rect = txt_surface.get_rect()
        txt_rect.center = rect.center
        surface.blit(txt_surface, txt_rect)