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

class Jogador(EntidadeGrade):
    def __init__(self, celula):
        super().__init__(celula, DURACAO_PASSO_JOGADOR)
        self.vivo = True
        
        # --- NOVO: Sistema de Imagens e Animação ---
        self.frames = []
        self.frame_atual = 0
        self.tempo_animacao = 0  # Controla a velocidade de troca dos passos
        
        # 1. Carrega a imagem com os 4 personagens (assumindo que o fundo já está transparente)
        sprite_sheet = pygame.image.load("imagens/personagem_andando.png").convert_alpha()
        
        # 2. Descobre o tamanho de cada personagem fatiando a largura total por 4
        largura_frame = sprite_sheet.get_width() // 4
        altura_frame = sprite_sheet.get_height()
        
        # 3. Recorta cada um dos 4 bonecos e salva na lista
        for i in range(4):
            area_recorte = pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame)
            frame_recortado = sprite_sheet.subsurface(area_recorte)
            
            # Ajusta para caber certinho no quadrado do labirinto (TILE)
            frame_pronto = pygame.transform.scale(frame_recortado, (TILE, TILE))
            self.frames.append(frame_pronto)
            
        # 4. Carrega e ajusta a imagem do personagem parado
        imagem_parado_original = pygame.image.load("imagens/personagem_parado.png").convert_alpha()
        self.imagem_parado = pygame.transform.scale(imagem_parado_original, (TILE, TILE))
            
    def pode_mover(self, dx, dy, labirinto, bombas):
        nx, ny = self.cx + dx, self.cy + dy
        if not labirinto.andavel(nx, ny):
            return False
        for b in bombas:
            if b.celula == (nx, ny) and not b.solta:
                return False
        return True

    def atualizar(self, dt, keys, labirinto, bombas):
        if self.em_movimento():
            self.atualizar_deslizamento(dt)
            
            # --- NOVO: Toca a animação APENAS se estiver se movendo ---
            self.tempo_animacao += dt
            if self.tempo_animacao > 0.15:  # Quanto menor o número, mais rápido ele mexe as pernas
                self.tempo_animacao = 0
                self.frame_atual = (self.frame_atual + 1) % 4
        else:
            # Se ele parar, volta para a pose 0 (parado)
            self.frame_atual = 0 
            
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
        # Descobre a posição exata (pixels) em que ele está deslizando agora
        px, py = self.posicao_pixel()
        py += HUD_H  # Ajusta para não ficar embaixo da barra de cima (HUD)
        
        if self.vivo:
            # Verifica se está a deslizar para o próximo bloco
            if self.em_movimento():
                # Desenha a imagem atual da animação de andar
                tela.blit(self.frames[self.frame_atual], (int(px - TILE/2), int(py - TILE/2)))
            else:
                # Desenha a imagem estática dele parado
                tela.blit(self.imagem_parado, (int(px - TILE/2), int(py - TILE/2)))