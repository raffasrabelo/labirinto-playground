"""Cores do labirinto. Espelham os tokens de web/src/style.css (--cell-*)."""
import pygame

BOARD_BG = (255, 255, 255)
GRID_LINE = (236, 239, 243)
CELL_EMPTY = (255, 255, 255)
CELL_WALL = (43, 52, 69)
CELL_MUD = (222, 202, 172)
TEXT = (52, 64, 84)

STATE_COLORS = {
    "frontier": (255, 214, 107),
    "visited": (176, 204, 255),
    "dead": (246, 170, 170),
    "path": (31, 179, 134),
}
CURRENT = (255, 138, 0)
START = (47, 111, 237)
GOAL = (229, 72, 77)
WHITE = (255, 255, 255)

# Q-Learning: mapa de calor do valor aprendido (max Q) e setas da política
HEAT_LOW = (243, 240, 255)
HEAT_HIGH = (124, 58, 237)
ARROW_DARK = (52, 64, 84)
AGENT = CURRENT


def mix(a, b, t: float):
    """Interpola duas cores: t=0 -> a, t=1 -> b."""
    return (round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t),
            round(a[2] + (b[2] - a[2]) * t))

_fonts = {}


def font(size: int) -> pygame.font.Font:
    """Fonte padrão do Pygame (única disponível no navegador sem arquivos extras)."""
    if size not in _fonts:
        _fonts[size] = pygame.font.Font(None, size)
    return _fonts[size]
