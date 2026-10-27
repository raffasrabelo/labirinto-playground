"""Paleta de cores e fontes da interface."""
import pygame

BG = (244, 245, 247)
PANEL = (255, 255, 255)
BORDER = (226, 232, 240)
TEXT = (31, 41, 51)
MUTED = (107, 114, 128)
ACCENT = (37, 99, 235)
ACCENT_HOVER = (29, 78, 216)
ACCENT_SOFT = (219, 234, 254)
HOVER = (241, 245, 249)
DISABLED = (176, 186, 199)
WHITE = (255, 255, 255)

GRID_LINE = (226, 232, 240)
CELL_EMPTY = (255, 255, 255)
CELL_WALL = (39, 49, 63)
CELL_MUD = (205, 170, 125)

STATE_COLORS = {
    "frontier": (253, 224, 120),
    "visited": (165, 205, 252),
    "dead": (252, 180, 180),
    "path": (40, 200, 140),
}
CURRENT = (245, 130, 11)
START = (37, 99, 235)
GOAL = (220, 38, 38)

_fonts = {}


def font(size: int) -> pygame.font.Font:
    """Fonte padrão do Pygame (funciona também no navegador via pygbag)."""
    if size not in _fonts:
        _fonts[size] = pygame.font.Font(None, size)
    return _fonts[size]
