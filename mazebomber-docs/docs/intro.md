---
sidebar_position: 1
title: Visão Geral do MazeBomber
---

# 💣 MazeBomber

**MazeBomber** é um jogo desenvolvido em Python (usando a biblioteca **Pygame**) que mistura as mecânicas clássicas de dois grandes sucessos: **Pac-Man** e **Bomberman**.

O jogador precisa navegar por um labirinto, explodir blocos, coletar pontos e fugir de fantasmas, utilizando estratégia e agilidade para encontrar a saída escondida e vencer a rodada.

---

## 🎮 Como Jogar

### Objetivos
1. **Coletar todas as bolinhas:** elas estão espalhadas pelo chão livre e escondidas debaixo de blocos destrutíveis.
2. **Encontrar a Saída:** a saída está escondida embaixo de um dos blocos do mapa. Ela só é ativada quando todas as bolinhas do mapa forem coletadas.
3. **Sobreviver:** encostar nos fantasmas ou ser pego por uma explosão (até mesmo a da sua própria bomba) resulta em morte instantânea!

### Controles
* **Setas do Teclado ou `W`, `A`, `S`, `D`:** movimentar o personagem.
* **Barra de Espaço:** colocar uma bomba.
* **`ESC`:** sair do jogo.

### Mecânicas Especiais
* Você tem um suprimento infinito de bombas, mas só pode ter **3 ativas ao mesmo tempo**.
* Alguns blocos escondem **Bombas Armadilhas**. Se a explosão da sua bomba atingir esse bloco, a bomba escondida detona junto, criando uma reação em cadeia!

---

## 🚀 Como Executar o Jogo

A forma mais fácil de iniciar o **MazeBomber** é:

1. Localize o arquivo chamado `jogar` (`jogar.bat`) na pasta do jogo.
2. Dê dois cliques sobre ele.
3. Aguarde a inicialização e o jogo será aberto automaticamente.

Pronto! Não é necessário abrir o terminal nem executar comandos manualmente para iniciar o jogo por esse método.

---

## ⚙️ Pré-requisitos e Instalação

Para rodar este jogo, você precisará do **Python 3** instalado no seu computador, além da biblioteca **Pygame**.

1. Instale a dependência do Pygame abrindo o terminal (ou prompt de comando) e digitando:

```bash
pip install pygame