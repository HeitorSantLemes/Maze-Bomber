---
sidebar_position: 3
title: Inimigos
---

# 👻 Inimigos

Os inimigos do **MazeBomber** são representados pela classe `Fantasma` (que herda de `EntidadeGrade`), combinando movimentação em grade com deslizamento suave (`DURACAO_PASSO_FANTASMA`), cálculo de distância por busca em largura (BFS) até o jogador e perfis variados de perseguição.

---

## 🧠 IA e Movimentação

- **Direções válidas (`escolher_direcao`):** avalia os quatro vizinhos ortogonais (`(1, 0)`, `(-1, 0)`, `(0, 1)`, `(0, -1)`) e filtra apenas aqueles onde `labirinto.andavel(...)` retorna verdadeiro.
- **Mapa de distância (BFS):** parte da célula atual do jogador `(jogador.cx, jogador.cy)` usando `deque` e `vizinhos(...)` para mapear a distância de cada célula transitável até o jogador.
- **Perfis de perseguição (`id_fantasma`):** a chance de perseguir o alvo é selecionada pela tabela `[0.90, 0.35, 0.65]` com base em `id_fantasma % len(chances)`:
  - **Índice 0 (`90%`):** perseguição mais agressiva, priorizando a célula vizinha com menor distância no mapa BFS (com embaralhamento prévio das opções em caso de empate).
  - **Índice 1 (`35%`):** comportamento mais imprevisível e errático, escolhendo direções aleatórias com maior frequência.
  - **Índice 2 (`65%`):** perseguição intermediária, alternando entre avançar na rota mais curta e mudar de direção.
- **Atualização (`atualizar`):** enquanto `em_movimento()` for verdadeiro, executa `atualizar_deslizamento(dt)`; quando parado, solicita uma nova direção e chama `iniciar_movimento(*d)`.

---

## 🎨 Renderização e Estado

- **Controle de ciclo de vida:** cada fantasma possui `cor`, `id_fantasma`, `vivo = True` e `respawn_em = 0.0`. O método `desenhar(tela)` retorna imediatamente se `not self.vivo`.
- **Desenho geométrico (`desenhar`):** calcula a posição em pixels com `posicao_pixel()` e desloca `HUD_H` no eixo `y`. Usa `raio = 10` para compor a cabeça circular, o corpo retangular, quatro ondulações na base e os olhos (brancos com pupilas escuras) na cor `self.cor`.

---

## 💥 Perigo e Eliminação

- **Colisão com o jogador:** encostar em um fantasma ativo encerra a tentativa com derrota imediata.
- **Explosões e reaparecimento:** fantasmas atingidos pelas chamas das bombas são eliminados, contando com o controle de `vivo` e `respawn_em` para gerenciamento de estado na partida.

---

## ✨ Dicas para Enfrentá-los

- Evite corredores fechados quando um fantasma com alta chance de perseguição estiver por perto.
- Aproveite os momentos em que o fantasma escolhe rotas aleatórias para reposicionar-se ou abrir passagem com bombas.
- Planeje sua rota de fuga antes de detonar bombas próximas às rotas de patrulha.