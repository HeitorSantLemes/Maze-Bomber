# entidade.py
from src.ui.utils import centro_pixel

class EntidadeGrade:
    def __init__(self, celula, duracao):
        self.cx, self.cy = celula
        self.alvo = None
        self.progresso = 0.0
        self.duracao = duracao
        self.direcao = (0, 1)

    def em_movimento(self):
        return self.alvo is not None

    def posicao_pixel(self):
        cx, cy = centro_pixel(self.cx, self.cy)
        if self.alvo is None:
            return cx, cy
        ax, ay = centro_pixel(*self.alvo)
        return (cx + (ax - cx) * self.progresso, cy + (ay - cy) * self.progresso)

    def iniciar_movimento(self, dx, dy):
        self.alvo = (self.cx + dx, self.cy + dy)
        self.progresso = 0.0
        self.direcao = (dx, dy)

    def atualizar_deslizamento(self, dt):
        if self.alvo is None:
            return False
        self.progresso += dt / self.duracao
        if self.progresso >= 1.0:
            self.cx, self.cy = self.alvo
            self.alvo = None
            self.progresso = 0.0
            return True
        return False