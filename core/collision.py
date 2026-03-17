def gerer_collisions(perso, plateformes):
    # --- Horizontal ---
    perso.position.x += perso.vitesse.x
    perso.rect.x = int(perso.position.x)

    for plat in plateformes:
        if perso.rect.colliderect(plat.rect):
            if plat.type == "solide":
                if perso.vitesse.x > 0: perso.rect.right = plat.rect.left
                if perso.vitesse.x < 0: perso.rect.left = plat.rect.right
                perso.position.x = perso.rect.x

    # --- Vertical ---
    perso.position.y += perso.vitesse.y
    perso.rect.y = int(perso.position.y)
    perso.au_sol = False

    for plat in plateformes:
        if perso.rect.colliderect(plat.rect):
            if plat.type == "solide":
                if perso.vitesse.y > 0:
                    perso.rect.bottom = plat.rect.top
                    perso.vitesse.y = 0
                    perso.au_sol = True
                elif perso.vitesse.y < 0:
                    perso.rect.top = plat.rect.bottom
                    perso.vitesse.y = 0

            elif plat.type == "traversable":
                if perso.vitesse.y > 0 and not perso.descend:
                    if (perso.position.y - perso.vitesse.y + perso.rect.height) <= plat.rect.top:
                        perso.rect.bottom = plat.rect.top
                        perso.vitesse.y = 0
                        perso.au_sol = True

    perso.position.y = perso.rect.y


def limiter_ecran(perso, largeur, hauteur):
    if perso.rect.left < 0:
        perso.rect.left = 0
        perso.position.x = 0
    if perso.rect.right > largeur:
        perso.rect.right = largeur
        perso.position.x = largeur - perso.rect.width
    if perso.rect.top < 0:
        perso.rect.top = 0
        perso.position.y = 0
        perso.vitesse.y = 0
    if perso.rect.bottom > hauteur:
        perso.rect.bottom = hauteur
        perso.position.y = hauteur - perso.rect.height
        perso.vitesse.y = 0
        perso.au_sol = True