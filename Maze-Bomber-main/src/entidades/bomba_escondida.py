# bomba_escondida.py
import pygame
import os
import math
from src.ui.config import HUD_H, IMG_DIR
from src.ui.utils import retangulo_celula

class BombaEscondida:
    _imagem = None

    def __init__(self, celula):
        self.celula = celula
        self.idade = 0.0
        self.revelada = False

        if BombaEscondida._imagem is None:
            # Carrega diretamente da nova pasta centralizada assets/imagens usando o IMG_DIR
            caminho_img = os.path.join(IMG_DIR, "bomba_escondida.png")

            try:
                if os.path.exists(caminho_img):
                    BombaEscondida._imagem = pygame.image.load(caminho_img).convert_alpha()
                else:
                    print(f"Aviso: Imagem da bomba escondida não encontrada em {caminho_img}")
                    BombaEscondida._imagem = None
            except Exception as e:
                print(f"ERRO ao carregar a imagem da bomba: {e}")
                BombaEscondida._imagem = None

    def revelar(self):
        """Chamado quando o bloco destrutível acima é destruído."""
        self.revelada = True

    def desenhar(self, tela):
        """Desenha a imagem da bomba escondida com efeito de pulsação (crescendo e diminuindo)."""
        if self.revelada:
            x, y = self.celula
            r = retangulo_celula(x, y).move(0, HUD_H)

            if BombaEscondida._imagem is not None:
                # Efeito de pulsação usando seno baseado no tempo em milissegundos
                tempo = pygame.time.get_ticks()
                fator_escala = 1.0 + 0.15 * math.sin(tempo * 0.01) 
                
                nova_largura = int(r.width * fator_escala)
                nova_altura = int(r.height * fator_escala)

                img_redimensionada = pygame.transform.scale(BombaEscondida._imagem, (nova_largura, nova_altura))
                
                # Centraliza a imagem redimensionada na célula para ela pulsar a partir do centro
                ret_img = img_redimensionada.get_rect(center=r.center)
                tela.blit(img_redimensionada, ret_img.topleft)
            else:
                # Fallback caso não haja imagem
                pygame.draw.circle(tela, (255, 120, 0), r.center, r.width // 3)