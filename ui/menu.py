import pygame
from abc import ABC, abstractmethod

class Menu(ABC):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
    def setup(self) -> None:
        """
        Setup les éléments du menu
        """
        pass
    
    def setdown(self) -> None:
        """
        Setdown les éléments du menu
        """
        pass

    @abstractmethod
    def update(self) -> str:
        """
        Met à jour la logique du menu
        et renvoi un game state
        """
        pass
    
    @abstractmethod
    def draw(self) -> None:
        """
        Dessine les éléments graphique de l'écran
        """
        pass