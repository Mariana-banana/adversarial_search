# Relatório do Trabalho 2 — Busca com Adversário

## 1. Identificação
**Integrantes:** Aline Fraga da Silva (579723), Gabriel Ricci Pazinatto (578935), Mariana Burzlaff Ercolani (579108)

**Turma:** B

## 2. Bibliotecas adicionais
Nenhuma além das já requeridas pelo enunciado. A implementação usa apenas a biblioteca padrão
do Python (`math`, `time`, `typing`). Não é necessário instalar nada além do ambiente indicado
(Python 3.12, numpy/pandas/numba já presentes no ambiente do kit).

## 3. Tic-Tac-Toe Misère

Avaliação da poda alfa-beta. Partidas executadas via `server.py` do kit.

**(i) O minimax sempre ganha ou empata jogando contra o `randomplayer`?**

**Sim.** Em 40 partidas (20 de pretas + 20 de brancas), o minimax **não
perdeu nenhuma**. Foram 29 vitórias, 11 empates e 0 derrotas. De pretas teve 9 vitórias e 11
empates, já de brancas, totalizou 20 vitórias. Como o `randomplayer` joga aleatoriamente, a ausência de
derrotas em todas as partidas é forte evidência de jogo perfeito.

**(ii) O minimax sempre empata consigo mesmo?**

**Sim.** Minimax × Minimax termina em **empate** nas duas configurações de quem começa.
Como dois jogadores ótimos não conseguem forçar a derrota do outro no jogo da velha invertido, o
empate é o resultado esperado de jogo perfeito contra jogo perfeito.

**(iii) O minimax não perde para você quando você usa a sua melhor estratégia?**

[PREENCHER! Esperado: o agente joga perfeito, então no máximo
empata, não deve perder]

Importante destacar que os testes do kit passam integralmente: `test_pruning` 2/2, `test_minimax_tttm` 4/4, `test_othello_evaluations` 2/2. Total 8/8.

## 4. Othello

### 4.1. As três heurísticas
- **Contagem de peças (`evaluate_count`):** diferença entre o número de peças do jogador e do
  oponente. Heurística mais simples, considerada baseline.
- **Valor posicional (`evaluate_mask`):** soma o valor das casas ocupadas pelo jogador e subtrai o
  das casas do oponente, usando a máscara `EVAL_TEMPLATE` fornecida no kit (cantos valem muito, casas
  adjacentes a cantos têm valor negativo). A máscara não foi alterada durante a implementação.
- **Customizada (`evaluate_custom`):** combina **5 estratégias clássicas de Othello** com **pesos
  que variam conforme a fase do jogo** (abertura / meio / fim, definidas pela quantidade de casas
  vazias). Além disso, em estados **terminais** retorna o resultado real (vitória/derrota/empate)
  com valor extremo, em vez do palpite heurístico.

As 5 estratégias utilizadas na heurística customizada foram: controle de cantos, proximidade de cantos (casas X/C), mobilidade,
discos de fronteira e paridade de peças (dinâmica). Esse conjunto enxuto (sem as estratégias mais caras,
como estabilidade e paridade de regiões) deixa a avaliação mais rápida, permitindo ao aprofundamento
iterativo buscar mais fundo no mesmo tempo (ver seção 5 sobre a escolha do conjunto).

### 4.2. Explicação e fontes da heurística customizada
A customizada parte da ideia central do Othello: **não** maximizar peças cedo (isso aumenta a
fronteira e entrega mobilidade ao oponente), e sim **controlar cantos, evitar as casas adjacentes a
cantos (X/C), maximizar a mobilidade própria e minimizar os discos de fronteira**, deixando a
contagem de peças pesar só no fim.

Os pesos variam por fase (ex.: paridade de peças com peso baixo/negativo na abertura e alto no fim;
mobilidade e fronteira relevantes cedo; controle de cantos ao longo de todo o jogo).

**Fontes (usadas como base conceitual das heurísticas, documentadas no material de estudo do grupo):**
- Rosenbloom, P. (1982). *A world-championship-level Othello program (IAGO).*
- Lee, K.-F., & Mahajan, S. (1990). *The Development of a World Class Othello Program (BILL).*
- Buro, M. (1997). *Experiments with Multi-ProbCut and a New High-Quality Evaluation Function for
  Othello (Logistello).*
- Buro, M. (1999). *Toward Simple, Fast, and Robust Game-Tree Search.*

As heurísticas foram **combinadas e adaptadas** pelo grupo a partir dessas fontes (não copiadas de
uma única fonte). A escolha do conjunto de estratégias usado foi apoiada por um experimento interno
(ver seção 5).

### 4.3. Critério de parada
Todas as implementações usam **aprofundamento iterativo limitado por tempo**: a busca explora
profundidades crescentes (1, 2, 3, …) e devolve a melhor jogada da última profundidade concluída
antes do tempo acabar. Como o corte é por relógio de parede, **não ultrapassa o tempo** em nenhuma
máquina e aproveita toda a profundidade disponível.
- **Três heurísticas obrigatórias (mini-torneio do item "b"):** orçamento de **2,0 s por jogada**,
  bem abaixo do limite de 5 s.
- **Agente do torneio (`tournament_agent`):** orçamento de **4,5 s por jogada**, próximo do limite de
  5 s (deixando margem para o overhead do servidor), para jogar o mais forte possível na competição.

### 4.4. Resultados do mini-torneio
Seis partidas (cada par joga duas vezes, alternando quem começa). Executadas via `server.py`, com as
três heurísticas em aprofundamento iterativo a **2,0 s por jogada**.

| Pretas (B) | Brancas (W) | Peças B | Peças W | Vencedor |
|---|---|---|---|---|
| Contagem | Valor posicional | 27 | 37 | Valor posicional |
| Valor posicional | Contagem | 43 | 21 | Valor posicional |
| Contagem | Customizada | 4 | 60 | Customizada |
| Customizada | Contagem | 60 | 4 | Customizada |
| Valor posicional | Customizada | 13 | 51 | Customizada |
| Customizada | Valor posicional | 44 | 20 | Customizada |

**Vitórias:** Customizada = 4, Valor posicional = 2, Contagem = 0.
**Peças capturadas no total (desempate):** Customizada = 215, Valor posicional = 113, Contagem = 56.

**Implementação mais bem-sucedida: a Customizada** (venceu **todas as 4** partidas que disputou, nas
duas cores, e capturou de longe o maior número de peças — 215).

**Análise:**
- A **Customizada** dominou: ganhou de Contagem e de Valor posicional **jogando de pretas e de
  brancas** (inclusive 51×13 e 60×4 de brancas). Não sofreu da desvantagem de iniciar de brancas —
  efeito do conjunto enxuto de estratégias (mais rápido → busca mais funda via aprofundamento
  iterativo), que compensa a falta de iniciativa com profundidade.
- O **Valor posicional** ficou em segundo, vencendo a Contagem nas duas partidas — faz sentido, já
  que valorizar cantos/posições é muito superior a só contar peças no Othello.
- A **Contagem** não venceu nenhuma: maximizar o número de peças cedo é justamente o erro clássico do
  Othello (aumenta a fronteira e entrega mobilidade ao oponente).

### 4.5. Implementação escolhida para o torneio
O `tournament_agent` usa **minimax com poda alfa-beta + aprofundamento iterativo limitado por
tempo** (orçamento de 4,5 s), guiado pela **heurística customizada** (as 5 estratégias com pesos por
fase + tratamento de terminal). Não utiliza nenhuma das heurísticas básicas de forma pura, conforme exigido. O
aprofundamento iterativo garante que a jogada é sempre devolvida dentro do tempo (sem risco de
desclassificação) e que toda a profundidade disponível na máquina é aproveitada.

## 5. Extras (opcional)
- **Experimento de seleção de estratégias (método de projeto):** para decidir a composição da
  heurística customizada, o grupo implementou agentes com diferentes subconjuntos das 10 estratégias
  disponíveis e os colocou para competir entre si. Escolhemos o **conjunto enxuto de 5 estratégias**
  (controle de cantos, casas X/C, mobilidade, fronteira e paridade de peças): por ser uma avaliação
  mais leve, permite ao aprofundamento iterativo buscar mais fundo no mesmo tempo, e na prática esse
  conjunto venceu o mini-torneio do item "b" de forma decisiva (4×0), inclusive **superando a
  desvantagem de jogar de brancas**. *(Esses agentes auxiliares foram apenas ferramenta de
  experimentação e não fazem parte da entrega final.)*
- **Aprofundamento iterativo** no agente do torneio (técnica complementar ao alfa-beta clássico).
- **MCTS:** [PREENCHER]

## 6. Utilização de IA

O grupo utilizou ferramentas de IA (como Gemini, chatGPT e Claude Code) durante o desenvolvimento, da seguinte forma:
- **Pesquisa e projeto das heurísticas:** uso de IA para levantar e explicar heurísticas clássicas de Othello e suas fontes.
- **Comentários de código:** inserindo comentários explicativos no código para
  facilitar o entendimento do que foi desenvolvido entre os integrantes do grupo.
- **Revisão e correção de implementação:** Código revisado e corrigido com auxílio das ferramentas de IA.
- **Execução automatizada do torneio:** As partidas foram executados, em sua maioria, de forma automatizada com o auxílio das ferramentas de IA.
- **Elaboração do relatório:** O grupo utilizou ferramentas de IA para auxiliar a elaboração do relatório, principalmente na montagem de tabelas.

