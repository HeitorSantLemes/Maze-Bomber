---
sidebar_position: 2
title: Personagem
---

#  Personagem

<img src="/img/personagem_parado.png" alt="Personagem do MazeBomber" width="128" />

O jogador é representado pela classe `Jogador` (que herda de `EntidadeGrade`), combinando deslocamento em grade com deslizamento suave entre células, animação de caminhada e interação direta com o labirinto e as bombas.

---

## 🎮 Movimentação e Controles

- **Direções (`TECLAS_DIRECAO`):** o movimento funciona por grade (`dx`, `dy`) usando **setas do teclado** (`↑`, `↓`, `←`, `→`) ou **`W`**, **`A`**, **`S`**, **`D`**.
- **Deslizamento suave e direção:** ao iniciar um passo (`iniciar_movimento`), o personagem desliza durante `DURACAO_PASSO_JOGADOR` e atualiza `olhando` (`"esquerda"` ou `"direita"`) quando há movimento horizontal (`dx < 0` ou `dx > 0`).
- **Verificação de passagem (`pode_mover`):** checa se a célula destino `(nx, ny)` é transitável no `labirinto` (`labirinto.andavel(nx, ny)`) e se não está bloqueada por alguma bomba que já tenha sido liberada (`not b.solta`).
- **Saída da célula da bomba:** enquanto o jogador continua na mesma célula `(self.cx, self.cy)` onde acabou de plantar uma bomba, `b.solta` continua ativa para não travar a saída dele; assim que ele sai da célula, `b.solta` passa a ser `False`.

---

## 🎞️ Sprites e Animação

- **Estado parado:** carrega `personagem_parado.png`, recorta a área visível com transparência (`get_bounding_rect(min_alpha=1)`), redimensiona proporcionalmente ao tamanho do `TILE` e gera a versão espelhada para a esquerda (`pygame.transform.flip`).
- **Animação de caminhada:** carrega os 4 frames (`personagem_andando1.png` a `personagem_andando4.png`) ajustando a altura à referência do sprite parado, alternando os quadros a cada `0.15s` enquanto `em_movimento()` estiver ativo.
- **Renderização (`desenhar`):** só desenha se `self.vivo` for verdadeiro, somando `HUD_H` ao eixo `y` para compensar a barra superior do HUD.

---

## 💣 Bombas e Condições de Derrota

- **Colocação:** a **Barra de Espaço** posiciona uma bomba (respeitando o limite de **3 bombas ativas** simultaneamente).
- **Derrota imediata:** encostar em fantasmas ou ser atingido por explosões (próprias, de outras bombas ou de bombas armadilhas em cadeia) encerra a tentativa com morte instantânea.

---

## ✨ Dicas de Jogabilidade

- Garanta sempre uma célula livre para recuar antes de soltar uma bomba em corredores estreitos.
- Evite ficar preso entre um fantasma e um bloco recém-destruído.
- Use **bombas armadilhas** à distância para provocar reações em cadeia com segurança.