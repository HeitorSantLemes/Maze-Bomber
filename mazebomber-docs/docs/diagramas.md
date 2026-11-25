---
sidebar_position: 5
title: Diagramas
---

# 📊 Diagramas

Esta página reúne os diagramas UML do **MazeBomber** para documentar a arquitetura orientada a objetos, a relação de herança entre entidades e o ciclo de execução de cada partida[cite: 5, 6, 7].

---

## 🔄 Diagrama de Sequência (Ciclo da Partida)

<img src="/img/diagrama_sequencia.png" alt="MazeBomber - Diagrama de Sequência (ciclo da partida)" width="760" />

- **Loop principal e estado ativo (`estado == "jogando"`):** `Loop principal` chama `atualizar(dt, keys)` em `Jogo`, que coordena o movimento do `Jogador` (verificando células/caminhos no `Labirinto`), a colocação de `Bomba` (respeitando estado, célula e limite, com som `tocar("bomba")` via `Audio`), a atualização das bombas ativas e explosões (`explodir(bomba)`, `dentro(x, y)`, `destruir_bloco(x, y)` e `tocar("explosao")`), e a movimentação dos `Fantasma` vivos[cite: 5].
- **Colisões, vitória e derrota:** após verificar bolinhas e saída no `Labirinto`, o fluxo avalia colisões de fantasmas com explosões (`marcar morto e definir respawn` e `tocar("fantasma_morre")`), colisões do jogador com fantasma ou explosão (`estado = "morreu"` e `tocar("morte")`) e chegada à saída ativa (`estado = "venceu"`, `rodada += 1` e `tocar("vitoria")`)[cite: 5].
- **Reinício e renderização:** quando a partida termina e o temporizador acaba, `nova_rodada()` recria `Labirinto`, `Jogador` e os `Fantasma` configurados; ao final de cada ciclo, `desenhar()` atualiza na tela `Labirinto`, `Bomba`, `Fantasma` e `Jogador`[cite: 5].

---

## 📐 Diagrama de Classes

<img src="/img/diagrama.png" alt="Diagrama de Classes - MazeBomber" width="760" />

- **Classe central `Jogo`:** gerencia `tela`, `audio`, `fonte`, `fonte_grande`, `rodada`, `estado`, `timer_fim`, `labirinto` (`1`), `jogador` (`1`), `fantasmas` (`0..*`), `bombas` (`0..*`) e `explosoes`, concentrando `nova_rodada()`, `colocar_bomba()`, `explodir(bomba)`, `atualizar(dt, keys)`, `desenhar()`, `_desenhar_hud()` e `_desenhar_faixa(...)`[cite: 6].
- **Classe abstrata `EntidadeGrade`:** define `cx`, `cy`, `alvo`, `progresso`, `duracao` e `direcao` junto aos métodos `em_movimento()`, `posicao_pixel()`, `iniciar_movimento(dx, dy)` e `atualizar_deslizamento(dt)`, servindo de base para `Jogador` e `Fantasma`[cite: 6].
- **Entidades e cenário:** `Jogador` (`vivo`, `frames`, `frame_atual`, `tempo_animacao`, `imagem_parado`), `Fantasma` (`cor`, `id_fantasma`, `vivo`, `respawn_em`, `escolher_direcao(...)`), `Bomba` (`celula`, `idade`, `solta`, `imagem_normal`, `imagem_grande`, `offset`) e `Labirinto` (`grade`, `inicio`, `saida`, `bolinhas`, `bolinhas_escondidas`, `bombas_escondidas`, `total_bolinhas`, `bolinhas_coletadas`, `base_fantasmas`, `andavel(...)`, `destruir_bloco(...)`, `saida_ativa()`)[cite: 6].

---

## 🧬 Diagrama de Classes e Herança

<img src="/img/diagrama_classes_heranca.png" alt="Diagrama de Classes e Herança - MazeBomber" width="760" />

- **Herança compartilhada:** `EntidadeGrade` concentra os atributos e métodos de grade e deslizamento compartilhados por `Jogador` e `Fantasma`[cite: 7].
- **Associações e dependências:** `Jogo` gerencia `Bomba` (`0..3`), `Fantasma` (`3`), `Jogador` (`1`) e `Labirinto` (`1`), além de acionar `Audio.tocar(nome)`[cite: 7]. `Fantasma` consulta caminhos em `Labirinto` e persegue `Jogador`, enquanto `Jogador` consulta movimento em `Labirinto`[cite: 7].