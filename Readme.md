# Relatório do Trabalho 2 - Busca com Adversário

## 1. Identificação
* **Nomes:** Aline Fraga da Silva(579723), Gabriel Ricci Pazinatto(578935) e Mariana Burzlaff Ercolani(579108)
* **Turma:** B

## 2. Bibliotecas Adicionais
* [Liste bibliotecas extras utilizadas ou informe que não foram utilizadas além das requeridas]

## 3. Tic-Tac-Toe Misere
### Resultados da Avaliação
(i) O minimax sempre ganha ou empata jogando contra o randomplayer?
**Resposta:** Sim. Como o espaço de estados do Tic-Tac-Toe Misere é extremamente reduzido, o minimax com profundidade ilimitada (`-1`) resolve o jogo perfeitamente. Contra o randomplayer, que escolhe jogadas aleatórias, o minimax aproveita todas as oportunidades e sempre vence ou empata, nunca sendo derrotado.

(ii) O minimax sempre empata consigo mesmo?
**Resposta:** Sim. O Tic-Tac-Toe Misere é um jogo matematicamente resolvido em que, sob jogada perfeita de ambos os lados, o resultado teórico é o empate. Como dois agentes minimax sempre jogam de forma ideal, o confronto minimax vs minimax sempre resulta em empate.

(iii) O minimax não perde para você quando você usa a sua melhor estratégia?
**Resposta:** Sim. Pela optimalidade matemática do algoritmo e busca exaustiva até estados terminais, qualquer sequência de lances tentada por um jogador humano será defendida perfeitamente pela IA, impedindo derrotas.

## 4. Othello
### Heurísticas Customizadas
Construímos 5 agentes (`agent_1` até `agent_5`), combinando as 10 heurísticas propostas no `STRATEGIES.MD`. 
* **agent_1**: Controle de Cantos, Proximidade de Cantos, Mobilidade, Discos de Fronteira, Paridade de Peças.
* **agent_2**: Controle de Cantos, Proximidade de Cantos, Mobilidade, Estabilidade e Jogadas Silenciosas.
* **agent_3**: Controle de Cantos, Proximidade de Cantos, Discos de Fronteira, Paridade de Regiões, Evaporação.
* **agent_4**: Controle de Cantos, Proximidade de Cantos, Estabilidade, Paridade de Peças, Padrões de Borda.
* **agent_5 (Tournament Agent)**: Combina as 10 heurísticas dinamicamente com base na fase do jogo (Abertura, Meio-Jogo, Fim de Jogo).
* **Fontes:** As implementações foram baseadas no arquivo `STRATEGIES.MD`, utilizando as metodologias de Iago (Rosenbloom), Bill (Lee & Mahajan) e Logistello (Buro).

### Critério de Parada
* **Descrição:** Utilizamos **Aprofundamento Iterativo (Iterative Deepening)** com limite de tempo. O algoritmo busca sequencialmente em profundidades cada vez maiores (1, 2, 3...) até que o tempo limite da jogada se esgote, momento em que retorna o melhor movimento encontrado na última iteração completa. Para facilitar a troca, basta passar um valor fixo no parâmetro `max_depth` (se diferente de -1, ele rodará até essa profundidade fixa sem timer).

### Resultados do Mini-Torneio
| Partida (B x W) | Vencedor | Peças B | Peças W |
|---|---|---|---|
| agent_2 X agent_4 | agent_4 | 0 | 28 |
| agent_3 X agent_5 | agent_5 | 15 | 49 |
| agent_1 X agent_3 | agent_3 | 31 | 33 |
| agent_3 X agent_2 | agent_2 | 26 | 38 |
| agent_3 X agent_1 | agent_1 | 25 | 39 |
| agent_1 X agent_2 | agent_1 | 47 | 17 |
| agent_1 X agent_4 | agent_1 | 56 | 8 |
| agent_2 X agent_3 | agent_3 | 26 | 38 |
| agent_3 X agent_4 | agent_3 | 42 | 22 |
| agent_4 X agent_5 | agent_5 | 22 | 42 |
| agent_4 X agent_2 | agent_2 | 16 | 48 |
| agent_4 X agent_3 | agent_3 | 14 | 50 |
| agent_1 X agent_5 | agent_1 | 55 | 9 |
| agent_4 X agent_1 | agent_1 | 30 | 34 |
| agent_2 X agent_1 | agent_1 | 28 | 36 |
| agent_2 X agent_5 | agent_5 | 29 | 35 |
| agent_5 X agent_1 | agent_1 | 15 | 49 |
| agent_5 X agent_3 | agent_5 | 58 | 5 |
| agent_5 X agent_2 | agent_2 | 1 | 63 |
| agent_5 X agent_4 | agent_5 | 63 | 1 |

**Análise:** A implementação mais bem-sucedida de todas foi a **agent_1** (7 vitórias). Embora o `agent_5` possua um conjunto completo de 10 heurísticas estruturadas, o `agent_1` foi superior na prática devido a dois fatores cruciais:
1. **Relação Profundidade-Velocidade:** Como o `agent_1` possui uma função de avaliação mais leve (apenas 5 heurísticas básicas, sem BFS ou laços complexos na borda), ele consegue avaliar nós muito mais rapidamente. Com isso, no aprofundamento iterativo dentro de 4.5s, ele atinge profundidades maiores (1 a 2 níveis extras), o que é mais valioso em Othello do que avaliações mais complexas porém rasas.
2. **Harmonia Estratégica:** `agent_5` sofreu de conflitos entre a evaporação e a coin-parity na fase de abertura (como na derrota de 1-63 contra o `agent_2`), forçando uma exclusão de peças própria tão agressiva que permitiu ao adversário monopolizar a mobilidade e encurralá-lo.

### Implementação Escolhida para o Torneio
* **Explicação:** Utilizaremos o **agent_1** adaptado como base do `tournament_agent.py` (ou `agent_5` devidamente simplificado em termos de custo computacional). A versão escolhida rodará com Aprofundamento Iterativo com tempo limite de 4.5s e sem geração de subprocessos ou threads ativas após a decisão, respeitando todas as restrições de tempo, de memória (RAM) e integridade do torneio.

## 5. Extras (Opcional)
* **Melhorias:** [Descreva implementação de MCTS ou de melhorias pro Minimax, se houver, citando fontes.]

## 6. Utilização de Chatbots ou Agentes de IA
* **Declaração:** [Descreva detalhadamente se utilizou IAs (como ChatGPT, Gemini, Copilot) e como foram utilizadas no desenvolvimento.]

---

# INSTRUÇÕES ORIGINAIS DO KIT (Guia)
O kit contém os seguintes arquivos (todos os `__init__.py` estao omitidos):

```text
kit_games
├── server.py              <-- servidor de jogos
├── server_tui.py          <-- servidor com melhor visualização (somente para othello)
├── test_mcts.py                <-- teste (muito basico) do seu MCTS
├── test_minimax_tttm.py        <-- teste da poda alfa-beta no tic-tac-toe misere
├── test_othello_evaluations.py <-- teste das funcoes de avaliacao do othello p/ a poda alfa-beta
├── test_pruning.py             <-- teste da poda alfa-beta em um jogo simplificado
└── advsearch
    ├── othello
    |   ├── board.py       <-- encapsula o tabuleiro do othello
    |   └── gamestate.py   <-- encapsula um estado do othello (config. do tabuleiro e cor que joga)
    ├── tttm
    |   ├── board.py       <-- encapsula o tabuleiro do tic-tac-toe misere
    |   └── gamestate.py   <-- encapsula um estado do tic-tac-toe-misere (config. do tabuleiro e cor que joga)
    ├── randomplayer
    |   └── agent.py       <-- agente que joga aleatoriamente
    ├── humanplayer        
    |   └── agent.py       <-- agente para um humano jogar 
    ├── timer.py           <-- funcoes auxiliares de temporizacao
    └── your_agent         <-- renomeie este diretorio c/ o nome do seu agente 
      ├── mcts.py         <-- implemente o algoritmo MCTS aqui
      ├── minimax.py      <-- implemente a poda alfa-beta aqui
      ├── othello_minimax_count.py  <-- chame seu minimax com a heuristica de contagem 
      ├── othello_minimax_mask.py   <-- chame seu minimax com a heuristica posicional 
      ├── othello_minimax_custom.py <-- chame seu minimax com uma heuristica customizada
      ├── tournament_agent.py       <-- agente que vai jogar o torneio de othello 
      ├── tttm_minimax.py           <-- chame seu minimax sem limite de profundidade aqui
      └── [vc pode adicionar outros arquivos e subdiretorios aqui]
```

## Instruções
Para iniciar uma partida, digite no terminal:
`python server.py game player1 player 2 [-h] [-d delay] [-p pace]  [-o output-file] [-l log-history]`
(Mais detalhes no arquivo original e PDF).