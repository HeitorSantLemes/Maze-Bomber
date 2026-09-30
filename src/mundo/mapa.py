# mapa.py
import random
import pygame
from src.ui.config import *
from src.ui.utils import *

N = (GRID - 1) // 2

def _gerar_arvore():
    pai = {(0, 0): None}
    profundidade = {(0, 0): 0}
    pilha = [(0, 0)]
    while pilha:
        x, y = pilha[-1]
        candidatos = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= x + dx < N and 0 <= y + dy < N
                      and (x + dx, y + dy) not in pai]
        if candidatos:
            novo = random.choice(candidatos)
            pai[novo] = (x, y)
            profundidade[novo] = profundidade[(x, y)] + 1
            pilha.append(novo)
        else:
            pilha.pop()
    return pai, profundidade

def _para_grade(no):
    return 2 * no[0] + 1, 2 * no[1] + 1

def _passagem(a, b):
    return a[0] + b[0] + 1, a[1] + b[1] + 1

class Labirinto:
    def __init__(self):
        pai, profundidade = _gerar_arvore()

        no_saida = max(profundidade, key=profundidade.get)
        caminho = []
        no = no_saida
        while no is not None:
            caminho.append(no)
            no = pai[no]
        caminho_principal = set(caminho)

        self.grade = [[PAREDE] * GRID for _ in range(GRID)]
        for no in pai:
            gx, gy = _para_grade(no)
            self.grade[gy][gx] = PISO

        for no, p in pai.items():
            if p is None:
                continue
            gx, gy = _passagem(no, p)
            if no in caminho_principal:
                self.grade[gy][gx] = PISO
            else:
                self.grade[gy][gx] = BLOCO

        self.inicio = _para_grade((0, 0))
        self.saida = _para_grade(no_saida)
        self.grade[self.saida[1]][self.saida[0]] = BLOCO

        paredes_internas = [
            (x, y)
            for y in range(1, GRID - 1)
            for x in range(1, GRID - 1)
            if self.grade[y][x] == PAREDE
        ]
        
        random.shuffle(paredes_internas)
        qtd_viram_bloco = int(len(paredes_internas) * 0.3)
        for i in range(qtd_viram_bloco):
            x, y = paredes_internas[i]
            self.grade[y][x] = BLOCO

        self.bolinhas = set()
        self.bolinhas_escondidas = set()
        self.bombas_escondidas = set()

        for y in range(GRID):
            for x in range(GRID):
                if (x, y) == self.inicio:
                    continue 

                if self.grade[y][x] == PISO:
                    self.bolinhas.add((x, y))
                elif self.grade[y][x] == BLOCO:
                    self.bolinhas_escondidas.add((x, y))
                    if random.random() < CHANCE_BLOCO_ARMADILHA:
                        self.bombas_escondidas.add((x, y))

        self.total_bolinhas = len(self.bolinhas) + len(self.bolinhas_escondidas)
        self.bolinhas_coletadas = 0

        self.base_fantasmas = min(
            caminho, key=lambda n: abs(n[0] - N // 2) + abs(n[1] - N // 2))
        self.base_fantasmas = _para_grade(self.base_fantasmas)

    def dentro(self, cx, cy):
        return 0 <= cx < GRID and 0 <= cy < GRID

    def andavel(self, cx, cy):
        return self.dentro(cx, cy) and self.grade[cy][cx] == PISO

    def destruir_bloco(self, cx, cy):
        self.grade[cy][cx] = PISO
        self.bombas_escondidas.discard((cx, cy))

        if (cx, cy) in self.bolinhas_escondidas:
            self.bolinhas_escondidas.discard((cx, cy))
            self.bolinhas.add((cx, cy))

    def saida_ativa(self):
        return self.bolinhas_coletadas >= self.total_bolinhas

    def desenhar(self, tela):
        for y in range(GRID):
            for x in range(GRID):
                r = retangulo_celula(x, y).move(0, HUD_H)
                tipo = self.grade[y][x]
                if tipo == PAREDE:
                    pygame.draw.rect(tela, COR_PAREDE, r)
                    pygame.draw.rect(tela, COR_PAREDE_BORDA, r, 2)
                elif tipo == BLOCO:
                    pygame.draw.rect(tela, COR_BLOCO, r)
                    pygame.draw.rect(tela, COR_BLOCO_BORDA, r, 3)
                else:
                    pygame.draw.rect(tela, COR_PISO, r)
                    pygame.draw.rect(tela, COR_GRADE, r, 1)

        for (x, y) in self.bolinhas:
            cx, cy = centro_pixel(x, y)
            pygame.draw.circle(tela, COR_BOLINHA, (cx, cy + HUD_H), 4)

        if self.grade[self.saida[1]][self.saida[0]] != BLOCO:
            ex, ey = centro_pixel(*self.saida)
            ey += HUD_H
            if self.saida_ativa():
                pulso = 3 + int(2 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
                pygame.draw.circle(tela, COR_SAIDA_ATIVA, (ex, ey), 14 + pulso, 3)
                pygame.draw.circle(tela, COR_SAIDA_ATIVA, (ex, ey), 8)
            else:
                pygame.draw.circle(tela, COR_SAIDA_INATIVA, (ex, ey), 12, 2)