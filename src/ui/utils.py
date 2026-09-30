# utils.py
import pygame
from src.ui.config import TILE

def retangulo_celula(cx, cy):
    return pygame.Rect(cx * TILE, cy * TILE, TILE, TILE)

def centro_pixel(cx, cy):
    return (cx * TILE + TILE // 2, cy * TILE + TILE // 2)

def vizinhos(cx, cy):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yield cx + dx, cy + dy