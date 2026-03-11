# Sovereign Stallion

**Sovereign Stallion** est un jeu de plateforme 2D développé avec PyGame.

## Concept & Game Design (GDD)

### 1. Synopsis & Personnage
Le joueur incarne un **Samurai** armé de son fidèle katana, poursuivi sans relâche par une entité vaporeuse nommée le **"Voile Obscur"**. 
* **Le Secret :** Ce voile représente en réalité ses propres crimes passés.
* **La Quête :** Le héros prend d'assaut un château médiéval défendu par de valeureux chevaliers pour récupérer un trésor sacré.
* **Le Plot-Twist :** Le trésor s'avère être une voiture de luxe moderne, créant un décalage avec l'univers médiéval.

### 2. Gameplay & Contrôles
L'expérience repose sur la précision et le timing (parades et dashs).
* **Mouvements :** `ZQSD` ou `Flèches directionnelles`.
  * **Haut :** Saut | **Bas :** S'accroupir.
* **Combat :**
  * **Attaque / Défense :** `Espace` ou `Pavé numérique 0`.
  * **Parade (Parry) :** Une parade réussie avec le bon timing étourdit l'adversaire.
  * **Dash :** `Ctrl` (esquive rapide avec frames d'invincibilité).
* **Action Spéciale :** `Shift` (utilité à définir).

### 3. Environnement & Ennemis
Le jeu se déroule dans un univers **Dark Medieval Fantasy** composé de plateformes fixes, mouvantes et traversables.
* **Obstacles :** Les ronces ralentissent le mouvement du joueur.
* **Bestiaire :**
  * **Chevalier :** Attaque au corps à corps (épée).
  * **Archer :** Attaque à distance (flèches).

### 4. Systèmes de Power-ups
* **Heal (Soin) :** Régénère la vie (apparition aléatoire).
* **Buff Arme :** Améliore les dégâts/portée du katana (trouvé dans des coffres).
* **Coup Ultime :** Débloqué après $X$ éliminations. L'écran se fige, des éclairs traversent les ennemis qui explosent lors de la reprise du temps.

### 5. Interface Utilisateur (UI)
* **Santé :** Plus la vie diminue, plus l'écran s'assombrit d'un voile rouge sang.
* **Buff Arme :** L'aspect de l'arme change selon le Buff actif.
* **Coup Ultime :** Des étincelles électriques entourent le joueur quand l'Ultime est prêt.

## Installation & Développement

### Récupération du dépôt
```bash
git clone git@github.com:Mitotow/sovereign_stallion.git
cd sovereign_stallion
```

### Configuration de l'environnement

1. **Création :** `python -m venv sovereign_stallion`
2. **Activation :**
* Windows : `.\sovereign_stallion\Scripts\activate`
* Mac/Linux : `source sovereign_stallion/bin/activate`

3. **Installation des dépendances :** `pip install -r requirements.txt`

## Workflow Git (Équipe de 3)

Nous utilisons un modèle simplifié pour garantir la fluidité du développement :

* **`main`** : Code stable et fonctionnel uniquement.
* **`dev`** : Branche d'intégration des fonctionnalités.
* **Branches Personnelles** : Chaque développeur travaille sur sa propre branche avant de fusionner vers `dev`.
