# audio.py
import pygame
import os
from src.ui.config import SOM_DIR

ARQUIVOS_SOM = {
    "bomba":            os.path.join(SOM_DIR, "colocar_bomba.wav"),
    "explosao":         os.path.join(SOM_DIR, "explosao.wav"),
    "bolinha":          os.path.join(SOM_DIR, "coletar_bolinha.wav"),
    "bomba_escondida":  os.path.join(SOM_DIR, "bomba_escondida.wav"),
    "fantasma_morre":   os.path.join(SOM_DIR, "fantasma_morre.wav"),
    "morte":            os.path.join(SOM_DIR, "morte.wav"),
    "vitoria":          os.path.join(SOM_DIR, "vitoria.wav"),
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
                try:
                    self.sons[nome] = pygame.mixer.Sound(caminho)
                except Exception as e:
                    print(f"Erro ao carregar o som {nome} em {caminho}: {e}")
            else:
                print(f"Aviso: Arquivo de som não encontrado: {caminho}")

    def tocar(self, nome):
        som = self.sons.get(nome)
        if som:
            som.play()