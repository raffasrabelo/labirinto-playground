"""Componentes de interface desenhados com Pygame (botão, slider, seletor).

O Pygame não tem widgets prontos; estes são mínimos e sem dependências
externas para continuarem funcionando no navegador (WebAssembly).
"""
import pygame

from . import theme as t


def draw_text(surf, text, size, color, pos, anchor="topleft"):
    img = t.font(size).render(str(text), True, color)
    rect = img.get_rect(**{anchor: pos})
    surf.blit(img, rect)
    return rect


def wrap_text(text, size, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = f"{line} {word}".strip()
        if t.font(size).size(test)[0] <= width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


class Button:
    def __init__(self, rect, label, on_click, primary=False, enabled=None):
        self.rect = pygame.Rect(rect)
        self.label = label                  # texto ou função que retorna texto
        self.on_click = on_click
        self.primary = primary
        self.enabled = enabled or (lambda: True)

    def handle(self, ev) -> bool:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 \
                and self.rect.collidepoint(ev.pos) and self.enabled():
            self.on_click()
            return True
        return False

    def draw(self, surf):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if not self.enabled():
            bg, fg, border = t.BG, t.DISABLED, t.BORDER
        elif self.primary:
            bg = t.ACCENT_HOVER if hover else t.ACCENT
            fg, border = t.WHITE, bg
        else:
            bg, fg, border = (t.HOVER if hover else t.PANEL), t.TEXT, t.BORDER
        pygame.draw.rect(surf, bg, self.rect, border_radius=8)
        pygame.draw.rect(surf, border, self.rect, 1, border_radius=8)
        label = self.label() if callable(self.label) else self.label
        draw_text(surf, label, 22, fg, self.rect.center, "center")


class Slider:
    """Slider de valores discretos: rótulo + valor na 1ª linha, trilho abaixo."""

    def __init__(self, rect, label, values, value, on_change, fmt=str):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.values = list(values)
        self.index = self.values.index(value)
        self.on_change = on_change
        self.fmt = fmt
        self.dragging = False

    @property
    def value(self):
        return self.values[self.index]

    def set_value(self, value, notify=False):
        self._set_index(self.values.index(value), notify)

    def _track(self):
        return pygame.Rect(self.rect.x + 8, self.rect.y + 28, self.rect.w - 16, 4)

    def _set_index(self, index, notify=True):
        index = max(0, min(len(self.values) - 1, index))
        if index != self.index:
            self.index = index
            if notify:
                self.on_change(self.value)

    def _index_at(self, x):
        track = self._track()
        ratio = (x - track.x) / track.w
        return round(ratio * (len(self.values) - 1))

    def handle(self, ev) -> bool:
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and self.rect.collidepoint(ev.pos):
            self.dragging = True
            self._set_index(self._index_at(ev.pos[0]))
            return True
        if ev.type == pygame.MOUSEMOTION and self.dragging:
            self._set_index(self._index_at(ev.pos[0]))
            return True
        if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.dragging:
            self.dragging = False
            return True
        return False

    def draw(self, surf):
        draw_text(surf, self.label, 21, t.TEXT, (self.rect.x, self.rect.y))
        draw_text(surf, self.fmt(self.value), 21, t.ACCENT, (self.rect.right, self.rect.y), "topright")
        track = self._track()
        pygame.draw.rect(surf, t.BORDER, track, border_radius=2)
        ratio = self.index / max(1, len(self.values) - 1)
        knob_x = track.x + round(ratio * track.w)
        pygame.draw.rect(surf, t.ACCENT, (track.x, track.y, knob_x - track.x, track.h), border_radius=2)
        pygame.draw.circle(surf, t.WHITE, (knob_x, track.centery), 8)
        pygame.draw.circle(surf, t.ACCENT, (knob_x, track.centery), 8, 2)


class Segmented:
    """Grupo de opções mutuamente exclusivas. options = [(chave, rótulo, habilitado)]."""

    def __init__(self, rect, options, selected, on_change, vertical=False, item_h=34, gap=6):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.selected = selected
        self.on_change = on_change
        self.vertical = vertical
        self.item_h = item_h
        self.gap = gap

    def _rects(self):
        n = len(self.options)
        if self.vertical:
            return [pygame.Rect(self.rect.x, self.rect.y + i * (self.item_h + self.gap),
                                self.rect.w, self.item_h) for i in range(n)]
        w = (self.rect.w - self.gap * (n - 1)) / n
        return [pygame.Rect(round(self.rect.x + i * (w + self.gap)), self.rect.y,
                            round(w), self.item_h) for i in range(n)]

    def handle(self, ev) -> bool:
        if ev.type != pygame.MOUSEBUTTONDOWN or ev.button != 1:
            return False
        for (key, _, enabled), rect in zip(self.options, self._rects()):
            if rect.collidepoint(ev.pos):
                if enabled and key != self.selected:
                    self.selected = key
                    self.on_change(key)
                return True
        return False

    def draw(self, surf):
        mouse = pygame.mouse.get_pos()
        for (key, label, enabled), rect in zip(self.options, self._rects()):
            if key == self.selected:
                bg, fg, border = t.ACCENT_SOFT, t.ACCENT, t.ACCENT
            elif not enabled:
                bg, fg, border = t.BG, t.DISABLED, t.BORDER
            else:
                bg = t.HOVER if rect.collidepoint(mouse) else t.PANEL
                fg, border = t.TEXT, t.BORDER
            pygame.draw.rect(surf, bg, rect, border_radius=8)
            pygame.draw.rect(surf, border, rect, 1, border_radius=8)
            if self.vertical:
                draw_text(surf, label, 22, fg, (rect.x + 12, rect.centery), "midleft")
            else:
                draw_text(surf, label, 21, fg, rect.center, "center")
