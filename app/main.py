"""Ponto de entrada da plataforma.

Navegador (produto):  python tools/build_web.py --serve   (na raiz do projeto)
Desktop (desenvolvimento, só o labirinto + atalhos de teclado):  python main.py

No navegador, a página HTML (web/src/) e o Python conversam por uma ponte
simples em JSON:
  - a página enfileira comandos em window.labirinto e o Python os lê a cada
    quadro com pull();
  - o Python envia o retrato do estado com push() sempre que algo muda.
O laço é assíncrono porque o pygbag exige devolver o controle ao navegador a
cada quadro (`await asyncio.sleep(0)`).
"""
import asyncio
import json
import sys

import pygame

from core.session import Session
from ui.board import BoardView

IS_WEB = sys.platform == "emscripten"


class WebBridge:
    """Troca de mensagens com a página (web/src/app.js)."""

    def __init__(self):
        import platform  # no pygbag, dá acesso ao `window` do JavaScript
        self.page = platform.window.labirinto
        self.last = None

    def pull(self) -> list:
        raw = self.page.pull()
        return json.loads(raw) if raw else []

    def push(self, snapshot: dict) -> None:
        data = json.dumps(snapshot)
        if data != self.last:
            self.page.push(data)
            self.last = data


class DesktopBridge:
    """Sem HTML: atalhos de teclado e status na barra de título da janela."""

    KEYS = {
        pygame.K_SPACE: {"type": "play"},
        pygame.K_n: {"type": "step"},
        pygame.K_r: {"type": "reset"},
        pygame.K_g: {"type": "new_maze"},
        pygame.K_1: {"type": "set", "name": "algorithm", "value": "backtracking"},
        pygame.K_2: {"type": "set", "name": "algorithm", "value": "dijkstra"},
        pygame.K_3: {"type": "set", "name": "algorithm", "value": "qlearning"},
    }

    def __init__(self):
        self.pending = []
        self.last = None

    def key(self, ev) -> None:
        if ev.key in self.KEYS:
            self.pending.append(self.KEYS[ev.key])

    def pull(self) -> list:
        cmds, self.pending = self.pending, []
        return cmds

    def push(self, snapshot: dict) -> None:
        m = snapshot["metrics"]
        title = (f"Labirinto Playground [dev] · {snapshot['params']['algorithm']} · "
                 f"{snapshot['status']} · expandidas {m['visited']} · custo {m['cost'] or '-'}")
        if title != self.last:
            pygame.display.set_caption(title)
            self.last = title


async def main():
    pygame.init()
    pygame.display.set_caption("Labirinto Playground")  # no navegador, vira o título da aba
    screen = pygame.display.set_mode((760, 760))
    session = Session()
    board = BoardView(session)
    bridge = WebBridge() if IS_WEB else DesktopBridge()
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000

        for cmd in bridge.pull():
            if cmd.get("type") == "resize":
                # tamanho real do elemento na página x densidade de pixels
                size = (max(64, int(cmd["w"])), max(64, int(cmd["h"])))
                if size != screen.get_size():
                    screen = pygame.display.set_mode(size)
            else:
                session.command(cmd)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and not IS_WEB:
                bridge.key(ev)
            else:
                board.handle(ev)

        session.update(dt)
        board.draw(screen)
        pygame.display.flip()
        bridge.push(session.snapshot())
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
