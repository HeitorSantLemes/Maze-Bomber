# main.py
import pygame
import sys

from src.ui.config import *
from src.ui.utils import *
from src.ui.audio import Audio
from src.mundo.mapa import Labirinto
from src.entidades.personagem import Jogador
from src.entidades.inimigo import Fantasma
from src.entidades.bomba import Bomba

class Jogo:
    def __init__(self, tela, audio):
        self.tela = tela
        self.audio = audio
        self.fonte = pygame.font.SysFont(None, 26)
        self.fonte_grande = pygame.font.SysFont(None, 54)
        self.rodada = 1
        self.nova_rodada()

    def nova_rodada(self):
        self.labirinto = Labirinto()
        self.jogador = Jogador(self.labirinto.inicio)
        cores = COR_FANTASMA
        self.fantasmas = [Fantasma(self.labirinto.base_fantasmas, cores[i % len(cores)], i)
                          for i in range(QTD_FANTASMAS)]
        self.bombas = []
        self.explosoes = {}          
        self.estado = "jogando"      
        self.timer_fim = 0.0

    def colocar_bomba(self):
        if self.estado != "jogando":
            return
        celula = (self.jogador.cx, self.jogador.cy)
        if any(b.celula == celula for b in self.bombas):
            return
        if len(self.bombas) >= MAX_BOMBAS_ATIVAS:
            return
        self.bombas.append(Bomba(celula))
        self.audio.tocar("bomba")

    def explodir(self, bomba):
        if bomba not in self.bombas:
            return
        self.bombas.remove(bomba)
        self.audio.tocar("explosao")
        cx, cy = bomba.celula
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = cx + dx, cy + dy
            if not self.labirinto.dentro(x, y):
                continue
            if self.labirinto.grade[y][x] == PAREDE:
                continue          
            self.explosoes[(x, y)] = TEMPO_EXPLOSAO

            for outra in list(self.bombas):
                if outra.celula == (x, y):
                    outra.idade = TEMPO_PAVIO

            if self.labirinto.grade[y][x] == BLOCO:
                tinha_bomba = (x, y) in self.labirinto.bombas_escondidas
                self.labirinto.destruir_bloco(x, y)
                if tinha_bomba:
                    self.audio.tocar("bomba_escondida")
                    self.explodir(Bomba((x, y)))

    def atualizar(self, dt, keys):
        if self.estado != "jogando":
            self.timer_fim -= dt
            if self.timer_fim <= 0:
                self.nova_rodada()
            return

        self.jogador.atualizar(dt, keys, self.labirinto, self.bombas)

        for b in self.bombas:
            b.idade += dt
        prontas = [b for b in self.bombas if b.idade >= TEMPO_PAVIO]
        for b in prontas:
            self.explodir(b)

        for cel in list(self.explosoes):
            self.explosoes[cel] -= dt
            if self.explosoes[cel] <= 0:
                del self.explosoes[cel]

        for f in self.fantasmas:
            if f.vivo:
                f.atualizar(dt, self.labirinto, self.jogador)
            else:
                f.respawn_em -= dt
                if f.respawn_em <= 0 and (f.cx, f.cy) != (self.jogador.cx, self.jogador.cy):
                    f.vivo = True

        pos_jogador = (self.jogador.cx, self.jogador.cy)
        if pos_jogador in self.labirinto.bolinhas:
            self.labirinto.bolinhas.discard(pos_jogador)
            self.labirinto.bolinhas_coletadas += 1
            self.audio.tocar("bolinha")

        for f in self.fantasmas:
            if f.vivo and (f.cx, f.cy) in self.explosoes:
                f.vivo = False
                f.respawn_em = TEMPO_RESPAWN_FANTASMA
                f.cx, f.cy = self.labirinto.base_fantasmas
                self.audio.tocar("fantasma_morre")

        if pos_jogador in self.explosoes or any(
                f.vivo and (f.cx, f.cy) == pos_jogador for f in self.fantasmas):
            self.estado = "morreu"
            self.timer_fim = TEMPO_TELA_FIM
            self.audio.tocar("morte")
            return

        if self.labirinto.saida_ativa() and pos_jogador == self.labirinto.saida:
            self.estado = "venceu"
            self.timer_fim = TEMPO_TELA_FIM
            self.rodada += 1
            self.audio.tocar("vitoria")

    def desenhar(self):
        tela = self.tela
        tela.fill(COR_FUNDO)
        self.labirinto.desenhar(tela)

        for (x, y), tempo in self.explosoes.items():
            r = retangulo_celula(x, y).move(0, HUD_H)
            pygame.draw.rect(tela, COR_EXPLOSAO, r.inflate(-4, -4))
            pygame.draw.rect(tela, COR_EXPLOSAO_CENTRO, r.inflate(-16, -16))

        # --- AQUI ESTÁ A CORREÇÃO: Puxa o desenho da bomba direto da classe dela ---
        for b in self.bombas:
            b.desenhar(tela)

        for f in self.fantasmas:
            f.desenhar(tela)

        self.jogador.desenhar(tela)
        self._desenhar_hud()

        if self.estado == "morreu":
            self._desenhar_faixa("VOCÊ MORREU!", (255, 90, 90), "Reiniciando o labirinto...")
        elif self.estado == "venceu":
            self._desenhar_faixa("LABIRINTO CONCLUÍDO!", (110, 240, 140),
                                 "Gerando um novo labirinto...")

    def _desenhar_hud(self):
        tela = self.tela
        texto = (f"Rodada {self.rodada}   "
                f"Bolinhas: {self.labirinto.bolinhas_coletadas}/{self.labirinto.total_bolinhas}   "
                f"Bombas: {len(self.bombas)}/{MAX_BOMBAS_ATIVAS}")
        tela.blit(self.fonte.render(texto, True, COR_TEXTO), (10, 12))

    def _desenhar_faixa(self, titulo, cor, subtitulo):
        véu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        véu.fill((0, 0, 0, 160))
        self.tela.blit(véu, (0, 0))
        t1 = self.fonte_grande.render(titulo, True, cor)
        t2 = self.fonte.render(subtitulo, True, COR_TEXTO)
        self.tela.blit(t1, t1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 16)))
        self.tela.blit(t2, t2.get_rect(center=(LARGURA // 2, ALTURA // 2 + 28)))

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("MazeBomber")
    relogio = pygame.time.Clock()

    audio = Audio()
    jogo = Jogo(tela, audio)

    while True:
        dt = min(relogio.tick(FPS) / 1000.0, 0.05)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_SPACE:
                    jogo.colocar_bomba()

        jogo.atualizar(dt, pygame.key.get_pressed())
        jogo.desenhar()
        pygame.display.flip()

if __name__ == "__main__":
    main()