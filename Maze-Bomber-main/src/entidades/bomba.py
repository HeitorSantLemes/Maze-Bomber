# bomba.py
import pygame
import os
from src.ui.config import TILE, HUD_H, IMG_DIR

class Bomba:
    def __init__(self, celula):
        self.celula = celula
        self.idade = 0.0
        self.solta = True
        
        # Carrega a imagem original utilizando o IMG_DIR da pasta assets
        caminho_img = os.path.join(IMG_DIR, "bomba.png")
        
        try:
            imagem_bomba = pygame.image.load(caminho_img).convert_alpha()
        except Exception as e:
            print(f"ERRO ao carregar a imagem da bomba em {caminho_img}: {e}")
            # Cria uma surface vazia de fallback caso ocorra algum erro de carregamento
            imagem_bomba = pygame.Surface((TILE, TILE))
            imagem_bomba.fill((230, 30, 30))
        
        # 1. Cria a versão de tamanho normal
        self.imagem_normal = pygame.transform.scale(imagem_bomba, (TILE, TILE))
        
        # 2. Cria uma versão 15% maior para dar o efeito de pulsar/tremer
        tamanho_grande = int(TILE * 1.15)
        self.imagem_grande = pygame.transform.scale(imagem_bomba, (tamanho_grande, tamanho_grande))
        
        # Calcula a diferença para manter a bomba grande centralizada no quadrado
        self.offset = (tamanho_grande - TILE) // 2

    def desenhar(self, tela):
        cx, cy = self.celula
        px = cx * TILE
        py = cy * TILE + HUD_H
        
        # A matemática da animação: 
        # A velocidade aumenta com o tempo (self.idade), fazendo a bomba pulsar 
        # cada vez mais freneticamente quando está quase a explodir!
        velocidade_pulsar = 5 + (self.idade * 3) 
        piscando = int(self.idade * velocidade_pulsar) % 2 == 0
        
        if piscando:
            # Desenha a versão maior (deslocada um pouco para trás para ficar no centro)
            tela.blit(self.imagem_grande, (px - self.offset, py - self.offset))
        else:
            # Desenha a versão normal
            tela.blit(self.imagem_normal, (px, py))