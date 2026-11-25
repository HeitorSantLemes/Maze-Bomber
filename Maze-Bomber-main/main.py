import pygame
import sys
import random
import os

from src.ui.config import *
from src.ui.utils import *
from src.ui.audio import Audio
from src.mundo.mapa import Labirinto
from src.entidades.personagem import Jogador
from src.entidades.inimigo import Fantasma
from src.entidades.bomba import Bomba
from src.entidades.bomba_escondida import BombaEscondida


class Jogo:
    def __init__(self, tela, audio):
        self.tela = tela
        self.audio = audio
        self.fonte = pygame.font.SysFont(None, 26)
        self.fonte_grande = pygame.font.SysFont(None, 54)
        self.rodada = 1
        self.nova_rodada()
        self.estado = "menu"  # O jogo começa no menu principal

    def nova_rodada(self):
        self.labirinto = Labirinto()
        self.jogador = Jogador(self.labirinto.inicio)
        cores = COR_FANTASMA
        self.fantasmas = [Fantasma(self.labirinto.base_fantasmas, cores[i % len(cores)], i)
                         for i in range(QTD_FANTASMAS)]
        self.bombas = []
        
        # Cria as bombas escondidas debaixo de alguns blocos destrutíveis do labirinto
        self.dict_bombas_escondidas = {}
        for y, linha in enumerate(self.labirinto.grade):
            for x, tipo in enumerate(linha):
                if tipo == BLOCO:
                    # 25% de chance de ter uma bomba escondida neste bloco
                    if random.random() < 0.25:
                        self.dict_bombas_escondidas[(x, y)] = BombaEscondida((x, y))

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
                # Verifica se há uma bomba escondida embaixo deste bloco
                if (x, y) in self.dict_bombas_escondidas:
                    bomba_oculta = self.dict_bombas_escondidas.pop((x, y))
                    bomba_oculta.revelar()
                    self.bombas.append(bomba_oculta)
                    self.audio.tocar("bomba")

                self.labirinto.destruir_bloco(x, y)

    def atualizar(self, dt, keys, clique_mouse):
        # Verifica se o jogador clicou no botão dos menus/telas de fim de jogo
        if self.estado != "jogando":
            self.timer_fim -= dt
            if clique_mouse and hasattr(self, 'btn_acao') and self.btn_acao.collidepoint(pygame.mouse.get_pos()):
                if self.estado == "menu" or self.estado == "morreu":
                    self.nova_rodada()
                    self.estado = "jogando"
                elif self.estado == "venceu":
                    self.rodada += 1
                    self.nova_rodada()
                    self.estado = "jogando"
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

        # Desenho do Menu Inicial
        if self.estado == "menu":
            t1 = self.fonte_grande.render("MAZE BOMBER", True, (255, 215, 0))
            t2 = self.fonte.render("Colete todas as bolinhas e encontre a saída!", True, COR_TEXTO)
            tela.blit(t1, t1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60)))
            tela.blit(t2, t2.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20)))

            # Botão Iniciar
            self.btn_acao = pygame.Rect(LARGURA // 2 - 110, ALTURA // 2 + 30, 220, 50)
            mouse_pos = pygame.mouse.get_pos()
            hover = self.btn_acao.collidepoint(mouse_pos)
            cor_btn = (50, 190, 50) if hover else (40, 140, 40)

            pygame.draw.rect(tela, cor_btn, self.btn_acao, border_radius=10)
            pygame.draw.rect(tela, (255, 255, 255), self.btn_acao, 2, border_radius=10)

            t_btn = self.fonte.render("INICIAR JOGO", True, (255, 255, 255))
            tela.blit(t_btn, t_btn.get_rect(center=self.btn_acao.center))
            return

        # Desenho do Jogo Normal
        self.labirinto.desenhar(tela)

        for (x, y), tempo in self.explosoes.items():
            r = retangulo_celula(x, y).move(0, HUD_H)
            pygame.draw.rect(tela, COR_EXPLOSAO, r.inflate(-4, -4))
            pygame.draw.rect(tela, COR_EXPLOSAO_CENTRO, r.inflate(-16, -16))

        for b in self.bombas:
            b.desenhar(tela)

        for f in self.fantasmas:
            f.desenhar(tela)

        self.jogador.desenhar(tela)
        self._desenhar_hud()

        # Telas de Fim de Jogo (Derrota / Vitória)
        if self.estado == "morreu":
            self._desenhar_faixa("VOCÊ MORREU!", (255, 90, 90), "Tente novamente!", "TENTAR NOVAMENTE")
        elif self.estado == "venceu":
            self._desenhar_faixa("LABIRINTO CONCLUÍDO!", (110, 240, 140), "Prepare-se para a próxima fase!", "PRÓXIMA FASE")

    def _desenhar_hud(self):
        tela = self.tela
        texto = (f"Rodada {self.rodada}   "
                f"Bolinhas: {self.labirinto.bolinhas_coletadas}/{self.labirinto.total_bolinhas}   "
                f"Bombas: {len(self.bombas)}/{MAX_BOMBAS_ATIVAS}")
        tela.blit(self.fonte.render(texto, True, COR_TEXTO), (10, 12))

    def _desenhar_faixa(self, titulo, cor, subtitulo, texto_botao):
        véu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        véu.fill((0, 0, 0, 180))
        self.tela.blit(véu, (0, 0))
        
        t1 = self.fonte_grande.render(titulo, True, cor)
        t2 = self.fonte.render(subtitulo, True, COR_TEXTO)
        self.tela.blit(t1, t1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40)))
        self.tela.blit(t2, t2.get_rect(center=(LARGURA // 2, ALTURA // 2 + 5)))

        # Botão interativo centralizado na faixa
        self.btn_acao = pygame.Rect(LARGURA // 2 - 110, ALTURA // 2 + 45, 220, 45)
        mouse_pos = pygame.mouse.get_pos()
        hover = self.btn_acao.collidepoint(mouse_pos)
        cor_btn = (70, 130, 220) if hover else (40, 90, 180)

        pygame.draw.rect(self.tela, cor_btn, self.btn_acao, border_radius=8)
        pygame.draw.rect(self.tela, (255, 255, 255), self.btn_acao, 2, border_radius=8)

        t_btn = self.fonte.render(texto_botao, True, (255, 255, 255))
        self.tela.blit(t_btn, t_btn.get_rect(center=self.btn_acao.center))


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("MazeBomber")
    
    try:
        caminho_icone = os.path.join(IMG_DIR, "personagem_parado.png")
        if os.path.exists(caminho_icone):
            icone = pygame.image.load(caminho_icone)
            pygame.display.set_icon(icone)
    except Exception as e:
        print(f"Não foi possível carregar o ícone da janela: {e}")

    relogio = pygame.time.Clock()

    audio = Audio()
    jogo = Jogo(tela, audio)

    while True:
        dt = min(relogio.tick(FPS) / 1000.0, 0.05)

        clique_mouse = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_SPACE and jogo.estado == "jogando":
                    jogo.colocar_bomba()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clique esquerdo do mouse
                    clique_mouse = True

        jogo.atualizar(dt, pygame.key.get_pressed(), clique_mouse)
        jogo.desenhar()
        pygame.display.flip()

if __name__ == "__main__":
    main()