# audio.py
import pygame
import os

ARQUIVOS_SOM = {
    "bomba":          "sons/colocar_bomba.wav",
    "explosao":       "sons/explosao.wav",
    "bolinha":        "sons/coletar_bolinha.wav",
    "bomba_escondida":"sons/bomba_escondida.wav",
    "fantasma_morre": "sons/fantasma_morre.wav",
    "morte":          "sons/morte.wav",
    "vitoria":        "sons/vitoria.wav",
}

class Audio:
    def __init__(self):
        self.sons = {}
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Áudio indisponível: o jogo vai rodar sem som.")
            return
        
        for nome, caminho in ARQUIVOS_SOM.items():
            if os.path.exists(caminho):
                self.sons[nome] = pygame.mixer.Sound(caminho)

    def tocar(self, nome):
        som = self.sons.get(nome)
        if som:
            som.play()