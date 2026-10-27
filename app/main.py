"""Ponto de entrada da plataforma.

Desktop:   python main.py
Navegador: python -m pygbag app      (a partir da pasta raiz do projeto)

O laço principal é assíncrono porque o pygbag (Pygame -> WebAssembly) exige
devolver o controle ao navegador a cada quadro (`await asyncio.sleep(0)`).
"""
import asyncio

import pygame

from ui.playground import H, W, Playground


async def main():
    pygame.init()
    pygame.display.set_caption("Labirinto Playground")
    screen = pygame.display.set_mode((W, H))
    app = Playground(screen)
    while app.running:
        app.tick()
        await asyncio.sleep(0)
    pygame.quit()


asyncio.run(main())
