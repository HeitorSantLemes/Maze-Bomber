# personagem.py
import pygame
import math
from src.ui.config import *
from src.ui.utils import *
from src.entidades.entidade import EntidadeGrade
TECLAS_DIRECAO = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
}

def _cos(graus):
    return math.cos(math.radians(graus))

def _sin(graus):
    return math.sin(math.radians(graus))

class Jogador(EntidadeGrade):
    def __init__(self, celula):
        super().__init__(celula, DURACAO_PASSO_JOGADOR)
        self.vivo = True
        self.fase_boca = 0.0

    def pode_mover(self, dx, dy, labirinto, bombas):
        nx, ny = self.cx + dx, self.cy + dy
        if not labirinto.andavel(nx, ny):
            return False
        for b in bombas:
            if b.celula == (nx, ny) and not b.solta:
                return False
        return True

    def atualizar(self, dt, keys, labirinto, bombas):
        self.fase_boca = (self.fase_boca + dt * 8) % (2 * 3.14159)
        if self.em_movimento():
            self.atualizar_deslizamento(dt)
        else:
            direcao_pedida = None
            for tecla, d in TECLAS_DIRECAO.items():
                if keys[tecla]:
                    direcao_pedida = d
                    break
            if direcao_pedida and self.pode_mover(*direcao_pedida, labirinto, bombas):
                self.iniciar_movimento(*direcao_pedida)
                self.direcao = direcao_pedida

        for b in bombas:
            if b.celula != (self.cx, self.cy):
                b.solta = False

    def desenhar(self, tela):
        px, py = self.posicao_pixel()
        py += HUD_H
        raio = 15
        pygame.draw.circle(tela, COR_JOGADOR_CORPO, (int(px), int(py) + 6), raio - 3)

        angulo_boca = 25 + 25 * abs(pygame.time.get_ticks() % 300 - 150) / 150
        dx, dy = self.direcao
        angulo_base = {(1, 0): 0, (-1, 0): 180, (0, -1): 270, (0, 1): 90}.get((dx, dy), 0)
        if self.vivo:
            pygame.draw.circle(tela, COR_JOGADOR_CABECA, (int(px), int(py)), raio)
            ponto1 = (px, py)
            ponto2 = (px + raio * 1.5 * _cos(angulo_base - angulo_boca),
                      py + raio * 1.5 * _sin(angulo_base - angulo_boca))
            ponto3 = (px + raio * 1.5 * _cos(angulo_base + angulo_boca),
                      py + raio * 1.5 * _sin(angulo_base + angulo_boca))
            pygame.draw.polygon(tela, COR_FUNDO, [ponto1, ponto2, ponto3])