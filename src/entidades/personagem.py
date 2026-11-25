import os
import pygame
from src.ui.config import *
from src.ui.utils import *
from src.entidades.entidade import EntidadeGrade

TECLAS_DIRECAO = {
    pygame.K_UP: (0, -1),
    pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d: (1, 0),
}


class Jogador(EntidadeGrade):
    def __init__(self, celula):
        super().__init__(celula, DURACAO_PASSO_JOGADOR)
        self.vivo = True
        self.olhando = "direita"

        self.frame_atual = 0
        self.tempo_animacao = 0.0

        self.parado_dir = self._carregar_base("personagem_parado.png")
        self.parado_esq = (
            pygame.transform.flip(self.parado_dir, True, False)
            if self.parado_dir is not None
            else None
        )

        altura_ref = self.parado_dir.get_height() if self.parado_dir is not None else TILE

        nomes_andar = [
            "personagem_andando1.png",
            "personagem_andando2.png",
            "personagem_andando3.png",
            "personagem_andando4.png",
        ]

        self.frames_dir = []
        for nome in nomes_andar:
            sprite = self._carregar_frame_animacao(
                nome, altura_alvo=altura_ref, fallback=self.parado_dir
            )
            if sprite is not None:
                self.frames_dir.append(sprite)

        if not self.frames_dir and self.parado_dir is not None:
            self.frames_dir = [self.parado_dir]

        self.frames_esq = [
            pygame.transform.flip(img, True, False) for img in self.frames_dir
        ]

    def _recortar_conteudo(self, img):
        # Tenta recortar apenas a área visível (com alfa > 0)
        area = img.get_bounding_rect(min_alpha=1)
        if area.width > 0 and area.height > 0:
            return img.subsurface(area).copy()
        return img

    def _carregar_base(self, nome_arquivo, fallback=None):
        caminho = os.path.join(IMG_DIR, nome_arquivo)
        if os.path.exists(caminho):
            try:
                img = pygame.image.load(caminho).convert_alpha()
                recortada = self._recortar_conteudo(img)
                larg, alt = recortada.get_size()
                if larg > 0 and alt > 0:
                    escala = min(TILE / larg, TILE / alt)
                    nova_larg = max(1, int(round(larg * escala)))
                    nova_alt = max(1, int(round(alt * escala)))
                    return pygame.transform.smoothscale(recortada, (nova_larg, nova_alt))
            except Exception as e:
                print(f"Aviso ao carregar {nome_arquivo}: {e}")
        return fallback

    def _carregar_frame_animacao(self, nome_arquivo, altura_alvo, fallback=None):
        caminho = os.path.join(IMG_DIR, nome_arquivo)
        if os.path.exists(caminho):
            try:
                img = pygame.image.load(caminho).convert_alpha()
                recortada = self._recortar_conteudo(img)
                larg, alt = recortada.get_size()
                if larg > 0 and alt > 0 and altura_alvo > 0:
                    escala = altura_alvo / alt
                    nova_larg = max(1, int(round(larg * escala)))
                    nova_alt = max(1, int(round(alt * escala)))
                    return pygame.transform.smoothscale(recortada, (nova_larg, nova_alt))
            except Exception as e:
                print(f"Aviso ao carregar {nome_arquivo}: {e}")
        return fallback

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

            if self.frames_dir:
                self.tempo_animacao += dt
                if self.tempo_animacao > 0.15:
                    self.tempo_animacao = 0.0
                    self.frame_atual = (self.frame_atual + 1) % len(self.frames_dir)
        else:
            self.frame_atual = 0

            direcao_pedida = None
            for tecla, d in TECLAS_DIRECAO.items():
                if keys[tecla]:
                    direcao_pedida = d
                    break

            if direcao_pedida and self.pode_mover(*direcao_pedida, labirinto, bombas):
                dx, dy = direcao_pedida
                if dx < 0:
                    self.olhando = "esquerda"
                elif dx > 0:
                    self.olhando = "direita"

                self.iniciar_movimento(dx, dy)
                self.direcao = direcao_pedida

        for b in bombas:
            if b.celula != (self.cx, self.cy):
                b.solta = False

    def desenhar(self, tela):
        if not self.vivo:
            return

        px, py = self.posicao_pixel()
        py += HUD_H

        if self.em_movimento() and self.frames_dir:
            indice = self.frame_atual % len(self.frames_dir)
            if self.olhando == "esquerda":
                sprite = self.frames_esq[indice]
            else:
                sprite = self.frames_dir[indice]
        else:
            if self.olhando == "esquerda":
                sprite = self.parado_esq
            else:
                sprite = self.parado_dir

        if sprite is not None:
            rect = sprite.get_rect(center=(int(px), int(py)))
            tela.blit(sprite, rect)