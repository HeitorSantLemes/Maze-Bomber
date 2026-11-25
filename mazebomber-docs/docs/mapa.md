---
sidebar_position: 4
title: Mapa
---

# 🗺️ Mapa

O mapa do **MazeBomber** é gerido pela classe `Labirinto` em uma grade `GRID x GRID`, combinando geração procedural por árvore geradora (DFS com pilha), caminho principal até a saída, blocos destrutíveis, itens escondidos e porta de saída com dois estados visuais.

---

## 🌳 Geração Procedural e Estrutura da Grade

- **Dimensões e árvore (`_gerar_arvore`):** calcula `N = (GRID - 1) // 2` e gera uma árvore a partir de `(0, 0)` registrando `pai` e `profundidade` de cada nó.
- **Caminho principal e saída:** escolhe o nó de maior profundidade como `no_saida`, reconstrói o caminho de volta até `(0, 0)` em `caminho_principal` e define `self.inicio` e `self.saida` via `_para_grade`.
- **Tipos de célula na grade:**
  - `PAREDE`: base inicial da grade e barreiras fixas.
  - `PISO`: nós visitados da árvore e passagens ao longo do `caminho_principal`.
  - `BLOCO`: passagens fora do `caminho_principal`, a célula inicial da `self.saida` e até `30%` (`0.3`) das `paredes_internas` sorteadas.
- **Base dos fantasmas (`self.base_fantasmas`):** seleciona o nó do caminho mais próximo do centro `(N // 2, N // 2)` em distância de Manhattan e converte para a grade.

---

## ⚪ Bolinhas, Blocos e Armadilhas

- **Bolinhas visíveis e escondidas:** células `PISO` (exceto `self.inicio`) recebem bolinhas em `self.bolinhas`, enquanto células `BLOCO` recebem bolinhas em `self.bolinhas_escondidas`. O total exigido é `self.total_bolinhas = len(self.bolinhas) + len(self.bolinhas_escondidas)`.
- **Bombas escondidas:** blocos também podem sortear uma bomba oculta em `self.bombas_escondidas` de acordo com `CHANCE_BLOCO_ARMADILHA`.
- **Destruição (`destruir_bloco`):** converte a célula `(cx, cy)` em `PISO`, remove eventuais bombas escondidas ali e transfere bolinhas de `self.bolinhas_escondidas` para `self.bolinhas`.
- **Liberação da saída (`saida_ativa`):** retorna verdadeiro quando `self.bolinhas_coletadas >= self.total_bolinhas`.

---

## 🚪 Renderização e Porta de Saída

- **Grade e bolinhas (`desenhar`):** desenha `PAREDE`, `BLOCO` e `PISO` deslocados por `HUD_H` no eixo `y`, além das bolinhas ativas com raio `4` na cor `COR_BOLINHA`.
- **Sprite da saída (`saida.png`):** carrega a imagem de `IMG_DIR`, divide ao meio na horizontal (`largura_porta = sprite_saida.get_width() // 2`) para separar a **porta apagada** (esquerda) e a **porta acesa** (direita), e escala ambas para `self.tamanho_saida = int(TILE * 1.25)`.
- **Estados na partida:** enquanto a célula da saída ainda for `BLOCO`, ela fica oculta; após ser descoberta, exibe a porta apagada até `saida_ativa()` ficar verdadeiro, quando passa a renderizar a porta acesa com efeito de pulsação (`pygame.time.get_ticks()`).

---

## ✨ Dicas de Exploração

- Abra rotas alternativas quebrando blocos que escondem bolinhas para completar o `total_bolinhas` mais rápido.
- Cuidado ao destruir blocos em sequência: além de liberar caminhos, eles podem revelar bolinhas ou bombas escondidas.
- Use a proximidade com a base central dos fantasmas e os corredores laterais para planejar fugas antes de acionar bombas.