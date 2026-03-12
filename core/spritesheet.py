import pygame


class Spritesheet:
    def __init__(self, path: str, frame_width, frame_height,
                 animation_speed: float):
        self.sheet = pygame.image.load(path).convert_alpha()
        self.animation_speed = animation_speed
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = self.get_frames(frame_width, frame_height)

    def get_frames(self, frame_width: int,
                   frame_height: int) -> list[pygame.Surface]:
        sheet_width = self.sheet.get_width()
        frames = []
        for x in range(0, sheet_width, frame_width):
            frame = self.sheet.subsurface(
                pygame.Rect(x, 0, frame_width, frame_height))
            frames.append(frame)
        return frames
