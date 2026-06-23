# Relatório do Trabalho 2 — Busca com Adversário

## 1. Identificação
**Integrantes:** Aline Fraga da Silva (579723), Gabriel Ricci Pazinatto (578935), Mariana Burzlaff Ercolani (579108)

**Turma:** B

## 2. Bibliotecas adicionais
Nenhuma biblioteca adicional foi utilizada, além das bibliotecas padrões do Python.

## 3. Tic-Tac-Toe Misère

**(i) O minimax sempre ganha ou empata jogando contra o `randomplayer`?**

Sim. Em 40 partidas (20 de pretas + 20 de brancas), o minimax não
perdeu nenhuma. Foram 29 vitórias, 11 empates e 0 derrotas. De pretas teve 9 vitórias e 11
empates, já de brancas, totalizou 20 vitórias. Como o `randomplayer` joga aleatoriamente, a ausência de
derrotas em todas as partidas é forte evidência de jogo perfeito.

**(ii) O minimax sempre empata consigo mesmo?**

Sim. Minimax × Minimax termina em empate nas duas configurações de quem começa.
Como dois jogadores ótimos não conseguem forçar a derrota do outro no jogo da velha invertido, o
empate é o resultado esperado de jogo perfeito contra jogo perfeito.

**(iii) O minimax não perde para você quando você usa a sua melhor estratégia?**

Sim. Jogando como humano tentando aplicar a melhor estratégia possível para forçar uma vitória, o máximo que se consegue é um empate. Como o Minimax explora a árvore de busca do TTTS inteira, ele nunca comete erros táticos, garantindo matematicamente que nunca perderá.

Além disso, os testes do kit passam integralmente: `test_pruning` 2/2, `test_minimax_tttm` 4/4, `test_othello_evaluations` 2/2. Total 8/8.

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



### 4.2. Explicação e fontes da heurística customizada

As 5 estratégias utilizadas na heurística customizada foram: controle de cantos, proximidade de cantos (casas X/C), mobilidade, discos de fronteira e paridade de peças, descritas brevemente abaixo:

* **Controle de Cantos:** Prioriza a captura dos cantos do tabuleiro, por serem posições que não podem ser retomadas pelo adversário futuramente.
* **Proximidade de Cantos:** Penaliza jogar nas casas adjacentes a cantos vazios, por serem mais sucetíveis a futuras capturas do oponente.
* **Mobilidade:** Busca balancear quantidade de jogadas válidas do agente Vs. Quantidade de jogadas válidas do oponente, visando ter sempre mais opções de movimento que o adversário.
* **Discos de Fronteira:** Penaliza posições adjacentes a discos do oponente, pois estas podem ser capturadas futuramente com mais facilidade.
* **Paridade de Peças:** Avalia a diferença entre a quantidade de peças do agente e as do oponente, focando em ter mais peças no tabuleiro, especialmente ao final do jogo.

Os pesos variam por fase (ex.: paridade de peças com peso baixo/negativo na abertura e alto no fim;
mobilidade e fronteira relevantes cedo; controle de cantos ao longo de todo o jogo).

**Fontes:**
- Rosenbloom, P. (1982). *A world-championship-level Othello program (IAGO).*
- Lee, K.-F., & Mahajan, S. (1990). *The Development of a World Class Othello Program (BILL).*
- Buro, M. (1997). *Experiments with Multi-ProbCut and a New High-Quality Evaluation Function for
  Othello (Logistello).*
- Buro, M. (1999). *Toward Opening Book Learning*

### 4.3. Critério de parada
Todas as implementações usam **aprofundamento iterativo limitado por tempo**: a busca explora
profundidades crescentes (1, 2, 3, …) e devolve a melhor jogada da última profundidade concluída
antes do tempo acabar. Assim, é possível buscar até a maior profundidade possível independentemente da máquina onde o agente está rodando.
- **Três heurísticas obrigatórias:** orçamento de 2,0 s por jogada.
- **Agente do torneio (`tournament_agent`):** orçamento de 4,5 s por jogada, próximo do limite de 5 s.

### 4.4. Resultados do mini-torneio
Seis partidas (cada par joga duas vezes, alternando quem começa). Executadas via `server.py`, com as
três heurísticas em aprofundamento iterativo a 2,0 s por jogada.

| Pretas (B) | Brancas (W) | Peças B | Peças W | Vencedor |
|---|---|---|---|---|
| Contagem | Valor posicional | 26 | 43 | Valor posicional |
| Valor posicional | Contagem | 52 | 17 | Valor posicional |
| Contagem | Customizada | 29 | 40 | Customizada |
| Customizada | Contagem | 55 | 14 | Customizada |
| Valor posicional | Customizada | 9 | 60 | Customizada |
| Customizada | Valor posicional | 50 | 19 | Customizada |

**Vitórias:** Customizada = 4, Valor posicional = 2, Contagem = 0.
**Peças capturadas no total (desempate):** Customizada = 205, Valor posicional = 123, Contagem = 86.

**Implementação mais bem-sucedida: a Customizada**: venceu todas as 4 partidas que disputou, nas
duas cores, e capturou de longe o maior número de peças.

**Análise:**
- A **Customizada** venceu de Contagem e de Valor posicional jogando de pretas e de
  brancas. Não sofreu da desvantagem de iniciar de brancas, efeito do conjunto eficiente de estragégias.
- O **Valor posicional** venceu a Contagem nas duas partidas, mas perdeu para a Customizada nas duas.
- A **Contagem** não venceu nenhuma partida, por focar somente na quantidade de peças.

### 4.5. Implementação escolhida para o torneio
O `tournament_agent` usa minimax com poda alfa-beta + aprofundamento iterativo limitado por
tempo (orçamento de 4,5 s), guiado pela heurística customizada. Não utiliza nenhuma das heurísticas básicas de forma pura. O Iterative Deepening garante que a jogada é sempre devolvida dentro do tempo.

## 5. Extras (opcional)
- **Experimento de seleção de estratégias:** para decidir a composição da heurística customizada, o grupo implementou agentes com diferentes subconjuntos das 10 estratégias disponíveis e os colocou para competir entre si. Escolhemos o conjunto 5 estratégias
  (controle de cantos, casas X/C, mobilidade, fronteira e paridade de peças): por ser uma avaliação
  mais leve, permite ao aprofundamento iterativo buscar mais fundo no mesmo tempo, e na prática esse
  conjunto venceu o mini-torneio do item "b".
- **Aprofundamento iterativo** no agente do torneio (técnica complementar ao alfa-beta clássico).
- **MCTS:** Implementamos a Monte Carlo Tree Search (`mcts.py`) seguindo o modelo de 4 etapas (Selection com UCB1, Expansion, Simulation e Backpropagation). Adicionamos uma inteligência primária na fase de Simulação (*Rollout pseudo-aleatório*): o agente evita escolher casas X e C (adjacentes às quinas) durante o rollout, a menos que seja obrigado. Isso reduziu drasticamente o número de simulações "suicidas" que prejudicavam a avaliação do MCTS puro, tornando-o um oponente muito mais formidável dentro dos mesmos 4.5 segundos.

## 6. Utilização de IA

O grupo utilizou ferramentas de IA (como Gemini, chatGPT e Claude Code) durante o desenvolvimento, da seguinte forma:
- **Experimento de seleção de estratégias:**: O código utilizado para executar torneios entre agentes com diferentes combinações e números de estratégias foi desenvolvido principalmente com uso do agente do Gemini. Todas as heurísticas utilizdas na versão final do trabalho foram revisadas pela ferramenta, mas desenvolvidas pelos membros do grupo.
- **Pesquisa e projeto das heurísticas:** uso de IA para levantar e explicar heurísticas clássicas de Othello e suas fontes.
- **Comentários de código:** inserindo comentários explicativos no código para
  facilitar o entendimento do que foi desenvolvido entre os integrantes do grupo.
- **Revisão e correção de implementação:** Código revisado e corrigido com auxílio das ferramentas de IA.
- **Execução automatizada do torneio:** As partidas foram executados, em sua maioria, de forma automatizada com o auxílio das ferramentas de IA.
- **Elaboração do relatório:** O grupo utilizou ferramentas de IA para auxiliar a elaboração do relatório, principalmente na montagem de tabelas.

