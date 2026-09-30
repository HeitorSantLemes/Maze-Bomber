# inimigo.py
import pygame
import random
from collections import deque
from src.ui.config import *
from src.ui.utils import *
from src.entidades.entidade import EntidadeGrade

class Fantasma(EntidadeGrade):
    def __init__(self, celula, cor, id_fantasma):
        super().__init__(celula, DURACAO_PASSO_FANTASMA)
        self.cor = cor
        self.id_fantasma = id_fantasma
        self.vivo = True
        self.respawn_em = 0.0

    def escolher_direcao(self, labirinto, jogador):
        opcoes = [(dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if labirinto.andavel(self.cx + dx, self.cy + dy)]
        if not opcoes:
            return None

        origem = (jogador.cx, jogador.cy)
        dist_ate_jogador = {origem: 0}
        fila = deque([origem])
        while fila:
            atual = fila.popleft()
            for viz in vizinhos(*atual):
                if viz not in dist_ate_jogador and labirinto.andavel(*viz):
                    dist_ate_jogador[viz] = dist_ate_jogador[atual] + 1
                    fila.append(viz)

        chances = [0.90, 0.35, 0.65] 
        chance_perseguir = chances[self.id_fantasma % len(chances)]

        if random.random() < chance_perseguir:
            random.shuffle(opcoes) 
            melhor = min(opcoes, key=lambda d: dist_ate_jogador.get(
                (self.cx + d[0], self.cy + d[1]), 999))
            return melhor
        return random.choice(opcoes)

    def atualizar(self, dt, labirinto, jogador):
        if self.em_movimento():
            self.atualizar_deslizamento(dt)
        else:
            d = self.escolher_direcao(labirinto, jogador)
            if d:
                self.iniciar_movimento(*d)

    def desenhar(self, tela):
        if not self.vivo:
            return
        px, py = self.posicao_pixel()
        py += HUD_H
        raio = 14
        pygame.draw.circle(tela, self.cor, (int(px), int(py) - 2), raio)
        pygame.draw.rect(tela, self.cor, (px - raio, py - 2, raio * 2, raio))
        for i in range(4):
            fx = px - raio + i * (raio / 2) + raio / 4
            pygame.draw.circle(tela, self.cor, (int(fx), int(py + raio - 2)), raio // 4)
        pygame.draw.circle(tela, (255, 255, 255), (int(px - 5), int(py - 4)), 4)
        pygame.draw.circle(tela, (255, 255, 255), (int(px + 5), int(py - 4)), 4)
        pygame.draw.circle(tela, (30, 30, 60), (int(px - 5), int(py - 4)), 2)
        pygame.draw.circle(tela, (30, 30, 60), (int(px + 5), int(py - 4)), 2)