"""Tela principal: parâmetros à esquerda, labirinto no centro, métricas à direita."""
import random

import pygame

from algorithms import ALGORITHMS
from algorithms.base import DONE, FAIL
from core.grid import EMPTY, MUD, WALL
from core.maze import generate_maze
from core.run_state import RunState

from . import theme as t
from .widgets import Button, Segmented, Slider, draw_text, wrap_text

VERSION = "v0.1 · Sprint 0"
W, H = 1280, 760
HEADER, LEFT, RIGHT, PAD = 56, 300, 270, 16

SIZES = list(range(11, 62, 2))          # dimensões ímpares (ver core/maze.py)
OPENNESS = list(range(0, 51, 5))        # % de paredes internas removidas
MUD_LEVELS = list(range(0, 41, 5))      # % de células com lama
SEEDS = list(range(1, 1000))
SPEEDS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]  # eventos por segundo

IDLE, RUNNING, PAUSED, FINISHED = "idle", "running", "paused", "finished"
STATUS_TEXT = {IDLE: "Pronto", RUNNING: "Executando...", PAUSED: "Pausado"}


class Playground:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.algorithm = "dijkstra"
        self.brush = WALL
        self.size, self.openness, self.mud, self.seed, self.speed = 21, 10, 15, 42, 20

        self.mode = IDLE
        self.gen = None
        self.run = RunState()
        self.accum = 0.0
        self.drag = None        # "start" | "goal" | tipo de célula sendo pintado

        self._build_widgets()
        self.regenerate()

    # ------------------------------------------------------------- widgets --
    def _build_widgets(self):
        x, w = PAD, LEFT - 2 * PAD
        algo_opts = [(k, a.name if a.available else f"{a.name}  (Sprint 3)", a.available)
                     for k, a in ALGORITHMS.items()]
        self.algo_select = Segmented((x, 92, w, 0), algo_opts, self.algorithm,
                                     self.set_algorithm, vertical=True)

        self.s_size = Slider((x, 252, w, 40), "Tamanho da grade", SIZES, self.size,
                             lambda v: self._param("size", v), fmt=lambda v: f"{v} x {v}")
        self.s_open = Slider((x, 298, w, 40), "Aberturas (ciclos)", OPENNESS, self.openness,
                             lambda v: self._param("openness", v), fmt=lambda v: f"{v}%")
        self.s_mud = Slider((x, 344, w, 40), "Lama (custo 5)", MUD_LEVELS, self.mud,
                            lambda v: self._param("mud", v), fmt=lambda v: f"{v}%")
        self.s_seed = Slider((x, 390, w, 40), "Semente", SEEDS, self.seed,
                             lambda v: self._param("seed", v))
        half = (w - 8) // 2
        self.b_new = Button((x, 438, half, 34), "Novo labirinto", self.new_maze)
        self.b_clear = Button((x + half + 8, 438, half, 34), "Grade vazia", self.clear_grid)

        self.brush_select = Segmented((x, 512, w, 0),
                                      [(WALL, "Parede", True), (MUD, "Lama", True), (EMPTY, "Borracha", True)],
                                      self.brush, self.set_brush, item_h=32)

        self.s_speed = Slider((x, 584, w, 40), "Velocidade", SPEEDS, self.speed,
                              self.set_speed, fmt=lambda v: f"{v} passos/s")
        self.b_play = Button((x, 632, w, 38), self._play_label, self.toggle_play, primary=True)
        self.b_step = Button((x, 678, half, 34), "Passo", self.step,
                             enabled=lambda: self.mode != FINISHED)
        self.b_reset = Button((x + half + 8, 678, half, 34), "Reiniciar", self.reset_run)

        self.widgets = [self.algo_select, self.s_size, self.s_open, self.s_mud, self.s_seed,
                        self.b_new, self.b_clear, self.brush_select, self.s_speed,
                        self.b_play, self.b_step, self.b_reset]

    def _play_label(self):
        return {RUNNING: "Pausar", PAUSED: "Continuar", FINISHED: "Executar de novo"}.get(self.mode, "Executar")

    # -------------------------------------------------------------- ações --
    def _param(self, name, value):
        setattr(self, name, value)
        self.regenerate()

    def set_algorithm(self, key):
        self.algorithm = key
        self.algo_select.selected = key
        self.reset_run()

    def set_brush(self, kind):
        self.brush = kind

    def set_speed(self, value):
        self.speed = value

    def regenerate(self):
        self.grid = generate_maze(self.size, self.size, self.seed,
                                  self.openness / 100, self.mud / 100)
        self._layout()
        self.reset_run()

    def new_maze(self):
        self.seed = random.choice(SEEDS)
        self.s_seed.set_value(self.seed)
        self.regenerate()

    def clear_grid(self):
        self.grid.fill(EMPTY)
        self.reset_run()

    def reset_run(self):
        self.mode, self.gen, self.run, self.accum = IDLE, None, RunState(), 0.0

    def _start(self):
        self.run = RunState()
        self.gen = ALGORITHMS[self.algorithm].run(self.grid)
        self.accum = 0.0

    def toggle_play(self):
        if self.mode in (IDLE, FINISHED):
            self._start()
            self.mode = RUNNING
        elif self.mode == RUNNING:
            self.mode = PAUSED
        else:
            self.mode = RUNNING

    def step(self):
        if self.mode == FINISHED:
            return
        if self.mode == IDLE:
            self._start()
        self.mode = PAUSED
        self._advance()

    def _advance(self) -> bool:
        """Consome um evento do algoritmo. Retorna False quando terminou."""
        try:
            ev = next(self.gen)
        except StopIteration:
            self.mode = FINISHED
            return False
        self.run.apply(ev)
        if ev.kind in (DONE, FAIL):
            self.mode = FINISHED
            return False
        return True

    # ------------------------------------------------------------ eventos --
    def _layout(self):
        area = pygame.Rect(LEFT + PAD, HEADER + PAD, W - LEFT - RIGHT - 2 * PAD, H - HEADER - 2 * PAD)
        self.cell = max(4, min(area.w // self.grid.cols, area.h // self.grid.rows))
        gw, gh = self.cell * self.grid.cols, self.cell * self.grid.rows
        self.board = pygame.Rect(area.x + (area.w - gw) // 2, area.y + (area.h - gh) // 2, gw, gh)

    def _cell_at(self, pos):
        if not self.board.collidepoint(pos):
            return None
        return ((pos[0] - self.board.x) // self.cell, (pos[1] - self.board.y) // self.cell)

    def _edit(self, cell):
        if cell is None:
            return
        if self.drag in ("start", "goal"):
            self.grid.move_endpoint(self.drag, cell)
        else:
            self.grid.set(cell, self.drag)
        self.reset_run()

    def handle(self, ev):
        if ev.type == pygame.QUIT:
            self.running = False
            return
        if ev.type == pygame.KEYDOWN:
            keys = {pygame.K_SPACE: self.toggle_play, pygame.K_n: self.step, pygame.K_RIGHT: self.step,
                    pygame.K_r: self.reset_run, pygame.K_g: self.new_maze}
            if ev.key in keys:
                keys[ev.key]()
            return
        for widget in self.widgets:
            if widget.handle(ev):
                return
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (1, 3):
            cell = self._cell_at(ev.pos)
            if cell is None:
                return
            if ev.button == 3:
                self.drag = EMPTY
            elif cell == self.grid.start:
                self.drag = "start"
            elif cell == self.grid.goal:
                self.drag = "goal"
            else:
                self.drag = self.brush
            self._edit(cell)
        elif ev.type == pygame.MOUSEMOTION and self.drag is not None:
            self._edit(self._cell_at(ev.pos))
        elif ev.type == pygame.MOUSEBUTTONUP:
            self.drag = None

    # ---------------------------------------------------------- execução --
    def update(self, dt):
        if self.mode != RUNNING:
            return
        self.accum += dt * self.speed
        n = min(int(self.accum), 5000)
        self.accum -= n
        for _ in range(n):
            if not self._advance():
                break

    def tick(self):
        dt = self.clock.tick(60) / 1000
        for ev in pygame.event.get():
            self.handle(ev)
        self.update(dt)
        self.draw()
        pygame.display.flip()

    # ------------------------------------------------------------ desenho --
    def draw(self):
        s = self.screen
        s.fill(t.BG)
        pygame.draw.rect(s, t.PANEL, (0, 0, W, HEADER))
        pygame.draw.line(s, t.BORDER, (0, HEADER - 1), (W, HEADER - 1))
        draw_text(s, "Labirinto Playground", 34, t.TEXT, (PAD, 12))
        draw_text(s, "Visualização interativa de Backtracking, Dijkstra e Q-Learning",
                  21, t.MUTED, (300, 22))
        draw_text(s, VERSION, 20, t.MUTED, (W - PAD, 22), "topright")

        pygame.draw.rect(s, t.PANEL, (0, HEADER, LEFT, H - HEADER))
        pygame.draw.line(s, t.BORDER, (LEFT - 1, HEADER), (LEFT - 1, H))
        pygame.draw.rect(s, t.PANEL, (W - RIGHT, HEADER, RIGHT, H - HEADER))
        pygame.draw.line(s, t.BORDER, (W - RIGHT, HEADER), (W - RIGHT, H))

        for label, y in (("ALGORITMO", 70), ("LABIRINTO", 228), ("PINCEL (clique e arraste)", 488),
                         ("EXECUÇÃO", 560)):
            draw_text(s, label, 18, t.MUTED, (PAD, y))
        for widget in self.widgets:
            widget.draw(s)
        draw_text(s, "Espaço executar · N passo · R reiniciar · G novo", 17, t.MUTED, (PAD, 726))
        draw_text(s, "Arraste os quadrados azul/vermelho para mover", 17, t.MUTED, (PAD, 742))

        self._draw_board(s)
        self._draw_sidebar(s)

    def _draw_board(self, s):
        g, cs, run = self.grid, self.cell, self.run
        pygame.draw.rect(s, t.GRID_LINE, self.board.inflate(2, 2))
        gap = 1 if cs >= 8 else 0
        show_dist = self.algorithm == "dijkstra" and cs >= 26
        for y in range(g.rows):
            for x in range(g.cols):
                cell = (x, y)
                kind = g.get(cell)
                rect = pygame.Rect(self.board.x + x * cs, self.board.y + y * cs, cs, cs)
                if kind == WALL:
                    pygame.draw.rect(s, t.CELL_WALL, rect)
                    continue
                state = run.cells.get(cell)
                inner = rect.inflate(-gap, -gap)
                if kind == MUD:
                    # lama visitada: anel marrom em volta da cor do estado
                    pygame.draw.rect(s, t.CELL_MUD, inner)
                    inner = inner.inflate(-max(4, cs // 3), -max(4, cs // 3))
                    color = t.STATE_COLORS[state] if state else t.CELL_MUD
                else:
                    color = t.STATE_COLORS[state] if state else t.CELL_EMPTY
                pygame.draw.rect(s, color, inner)
                if show_dist and cell in run.dist and state != "path":
                    draw_text(s, run.dist[cell], 17, t.TEXT, rect.center, "center")

        for cell, color in ((g.start, t.START), (g.goal, t.GOAL)):
            rect = pygame.Rect(self.board.x + cell[0] * cs, self.board.y + cell[1] * cs, cs, cs)
            pygame.draw.rect(s, color, rect.inflate(-gap, -gap), border_radius=max(2, cs // 5))
            pygame.draw.circle(s, t.WHITE, rect.center, max(2, cs // 5))
        if run.current is not None:
            x, y = run.current
            rect = pygame.Rect(self.board.x + x * cs, self.board.y + y * cs, cs, cs)
            pygame.draw.rect(s, t.CURRENT, rect, max(2, cs // 8))

    def _draw_sidebar(self, s):
        x0, w = W - RIGHT + PAD, RIGHT - 2 * PAD
        run = self.run
        draw_text(s, "MÉTRICAS", 18, t.MUTED, (x0, 70))

        if self.mode == FINISHED:
            status = "Caminho encontrado" if run.found else "Sem caminho"
        else:
            status = STATUS_TEXT[self.mode]
        if self.algorithm == "dijkstra":
            structure = ("Fila de prioridade", run.counts["frontier"])
        else:
            structure = ("Pilha (atual / máx.)", f"{run.depth} / {run.max_depth}")
        rows = [("Status", status),
                ("Eventos executados", run.steps),
                ("Células expandidas", run.visited),
                structure,
                ("Passos do caminho", run.result.get("moves", "-")),
                ("Custo do caminho", run.result.get("cost", "-"))]
        y = 94
        for label, value in rows:
            draw_text(s, label, 20, t.MUTED, (x0, y))
            draw_text(s, value, 20, t.TEXT, (x0 + w, y), "topright")
            y += 26

        draw_text(s, "LEGENDA", 18, t.MUTED, (x0, 268))
        legend = [(t.START, "Início"), (t.GOAL, "Objetivo"), (t.CELL_WALL, "Parede"),
                  (t.CELL_MUD, "Lama (custo 5)"), (t.STATE_COLORS["frontier"], "Fronteira"),
                  (t.STATE_COLORS["visited"], "Expandida"), (t.STATE_COLORS["dead"], "Retrocesso"),
                  (t.CURRENT, "Célula atual"), (t.STATE_COLORS["path"], "Caminho final")]
        for i, (color, label) in enumerate(legend):
            cx, cy = x0 + (i % 2) * (w // 2), 292 + (i // 2) * 24
            pygame.draw.rect(s, color, (cx, cy, 16, 16), border_radius=4)
            pygame.draw.rect(s, t.BORDER, (cx, cy, 16, 16), 1, border_radius=4)
            draw_text(s, label, 19, t.TEXT, (cx + 22, cy + 1))

        info = ALGORITHMS[self.algorithm]
        draw_text(s, f"SOBRE: {info.name.upper()}", 18, t.MUTED, (x0, 420))
        y = 444
        for line in wrap_text(info.description, 20, w):
            draw_text(s, line, 20, t.TEXT, (x0, y))
            y += 19
