"""Desenho do labirinto com Pygame e edição com o mouse.

É a ÚNICA parte da interface feita em Pygame. Parâmetros, botões, métricas e
legenda ficam no HTML (web/src/). O tabuleiro ocupa toda a superfície e se
adapta ao tamanho dela (que no navegador acompanha o tamanho real do
elemento na página, já multiplicado pela densidade de pixels da tela).
"""
import pygame

from algorithms.qlearning import ACTIONS, best_action
from core.grid import MUD, WALL

from . import theme as t


# tamanho mínimo da célula, em pixels de TELA (CSS), para os números Q serem legíveis
MIN_CELL_MAX_VALUE = 28   # um número por célula
MIN_CELL_ALL_VALUES = 42  # quatro números por célula


class BoardView:
    def __init__(self, session):
        self.session = session
        self.surface_size = (0, 0)
        self.cell = 1
        self.board = pygame.Rect(0, 0, 0, 0)
        self.dpr = 1.0            # densidade de pixels da tela (enviada pela página)
        self._text_cache = {}     # (texto, tamanho, cor, negrito) -> Surface

    def _layout(self, surface):
        grid = self.session.grid
        w, h = surface.get_size()
        pad = max(2, min(w, h) // 100)
        self.cell = max(2, min((w - 2 * pad) // grid.cols, (h - 2 * pad) // grid.rows))
        gw, gh = self.cell * grid.cols, self.cell * grid.rows
        self.board = pygame.Rect((w - gw) // 2, (h - gh) // 2, gw, gh)

    def cell_at(self, pos):
        if not self.board.collidepoint(pos):
            return None
        return ((pos[0] - self.board.x) // self.cell, (pos[1] - self.board.y) // self.cell)

    def _rect(self, cell):
        return pygame.Rect(self.board.x + cell[0] * self.cell, self.board.y + cell[1] * self.cell,
                           self.cell, self.cell)

    # -------------------------------------------------------------- mouse --
    def handle(self, ev) -> None:
        s = self.session
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (1, 3):
            s.edit_begin(self.cell_at(ev.pos), erase=ev.button == 3)
        elif ev.type == pygame.MOUSEMOTION:
            cell = self.cell_at(ev.pos)
            s.hover_at(cell)
            if s.drag is not None:
                s.edit_drag(cell)
        elif ev.type == pygame.MOUSEBUTTONUP:
            s.edit_end()
        elif ev.type == pygame.WINDOWLEAVE:
            s.hover_at(None)

    def _text(self, text, size, color, bold=False):
        """Texto renderizado com cache (os mesmos números se repetem a cada quadro)."""
        key = (text, size, color, bold)
        img = self._text_cache.get(key)
        if img is None:
            if len(self._text_cache) > 4000:
                self._text_cache.clear()
            img = self._text_cache[key] = t.font(size, bold).render(text, True, color)
        return img

    # ------------------------------------------------------------ desenho --
    def draw(self, surface) -> None:
        self._layout(surface)
        s = self.session
        grid, run, cs = s.grid, s.run, self.cell
        surface.fill(t.BOARD_BG)
        pygame.draw.rect(surface, t.GRID_LINE, self.board)

        gap = 1 if cs >= 10 else 0
        show_numbers = (s.params["show_numbers"] and s.params["algorithm"] == "dijkstra"
                        and cs >= 22)
        number_font = t.font(max(12, int(cs * 0.5)))

        # Q-Learning: valor de cada estado = max Q(s, .), normalizado para o mapa de calor
        q = run.q if s.params["algorithm"] == "qlearning" else None
        heat, arrows, labels = {}, [], []
        css_cell = cs / self.dpr
        s.q_fit = {"max": css_cell >= MIN_CELL_MAX_VALUE, "all": css_cell >= MIN_CELL_ALL_VALUES}
        mode = s.params["q_values"]
        if mode != "off" and not s.q_fit[mode]:
            mode = "off"          # números ilegíveis nesta grade: a página avisa e oferece o inspetor
        if q:
            values = {c: max(qs) for c, qs in q.items()}
            low, high = min(values.values()), max(values.values())
            span = (high - low) or 1.0
            heat = {c: (v - low) / span for c, v in values.items()}
            show_arrows = s.params["show_policy"] and cs >= 12

        for y in range(grid.rows):
            for x in range(grid.cols):
                cell = (x, y)
                kind = grid.get(cell)
                rect = self._rect(cell)
                if kind == WALL:
                    pygame.draw.rect(surface, t.CELL_WALL, rect)
                    continue
                state = run.cells.get(cell)
                inner = rect.inflate(-gap, -gap)
                if state:
                    fill = t.STATE_COLORS[state]
                elif cell in heat:
                    fill = t.mix(t.HEAT_LOW, t.HEAT_HIGH, heat[cell])
                else:
                    fill = None
                if kind == MUD:
                    # lama: anel cor de areia em volta da cor do estado
                    pygame.draw.rect(surface, t.CELL_MUD, inner)
                    # com números Q na célula, o anel de lama fica fino para não atrapalhar a leitura
                    ring = max(2, cs // (14 if mode != "off" and cell in heat else 5))
                    inner = inner.inflate(-2 * ring, -2 * ring)
                    color = fill or t.CELL_MUD
                else:
                    color = fill or t.CELL_EMPTY
                pygame.draw.rect(surface, color, inner, border_radius=max(0, cs // 8))
                if show_numbers and cell in run.dist and state != "path":
                    img = number_font.render(str(run.dist[cell]), True, t.TEXT)
                    surface.blit(img, img.get_rect(center=rect.center))
                if q and cell in q and cell != grid.goal:
                    qs = q[cell]
                    explored = max(qs) != min(qs)
                    light = heat[cell] > 0.55 or state == "path"
                    if show_arrows and explored and mode != "all":   # no modo "all" o sublinhado marca a melhor ação
                        arrows.append((rect.center, best_action(qs), light))
                    if mode != "off":
                        labels.append((rect, qs, light, explored))

        # com números no centro, a seta vira um triângulo pequeno junto à borda
        arrow_scale, arrow_offset = {"off": (1.0, 0.0), "max": (0.5, 0.36), "all": (1.0, 0.0)}[mode]
        for center, action, light in arrows:
            self._draw_arrow(surface, center, action, t.WHITE if light else t.ARROW_DARK,
                             arrow_scale, arrow_offset)
        for rect, qs, light, explored in labels:
            self._draw_q_values(surface, rect, qs, mode, t.WHITE if light else t.TEXT, explored)

        radius = max(2, cs // 4)
        for cell, color in ((grid.start, t.START), (grid.goal, t.GOAL)):
            rect = self._rect(cell).inflate(-gap, -gap)
            pygame.draw.rect(surface, color, rect, border_radius=radius)
            pygame.draw.circle(surface, t.WHITE, rect.center, max(2, cs // 6))
        if run.current is not None:
            if q is not None:
                # o agente do Q-Learning é um círculo que anda pelo labirinto
                center = self._rect(run.current).center
                pygame.draw.circle(surface, t.WHITE, center, max(3, int(cs * 0.36)))
                pygame.draw.circle(surface, t.AGENT, center, max(2, int(cs * 0.3)))
            else:
                pygame.draw.rect(surface, t.CURRENT, self._rect(run.current), max(2, cs // 7),
                                 border_radius=radius)

    def _draw_q_values(self, surface, rect, qs, mode, color, explored):
        """Valores da tabela Q da célula: o maior (centro) ou os 4 (um em cada borda)."""
        cs = self.cell
        if mode == "max":
            # fonte = metade da célula: "-12" ocupa ~48% da largura
            img = self._text(f"{max(qs):.0f}", max(10, int(cs * 0.5)), color)
            surface.blit(img, img.get_rect(center=rect.center))
            return
        # 4 valores em cruz: cima/baixo centralizados, esquerda/direita na linha do meio.
        # fonte = 0,36 da célula: "-12" ocupa ~34% da largura e cada linha ~24% da altura
        best = best_action(qs) if explored else None
        size = max(10, int(cs * 0.36))
        cx, cy = rect.center
        for a, (dx, dy) in enumerate(ACTIONS):
            img = self._text(f"{qs[a]:.0f}", size, color, bold=a == best)
            r = img.get_rect(center=(cx + dx * cs * 0.27, cy + dy * cs * 0.3))
            surface.blit(img, r)
            if a == best:   # sublinhado marca a melhor ação
                pygame.draw.line(surface, color, (r.left, r.bottom), (r.right - 1, r.bottom),
                                 max(1, int(self.dpr)))

    def _draw_arrow(self, surface, center, action, color, scale=1.0, offset=0.0):
        """Triângulo apontando para a melhor ação (cima, direita, baixo, esquerda)."""
        dx, dy = ACTIONS[action]
        size = self.cell * 0.28 * scale
        cx, cy = center[0] + dx * self.cell * offset, center[1] + dy * self.cell * offset
        tip = (cx + dx * size, cy + dy * size)
        base_x, base_y = cx - dx * size * 0.6, cy - dy * size * 0.6
        px, py = -dy * size * 0.6, dx * size * 0.6   # perpendicular
        pygame.draw.polygon(surface, color, [tip, (base_x + px, base_y + py), (base_x - px, base_y - py)])
