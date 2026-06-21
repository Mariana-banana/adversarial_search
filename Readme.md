# Relatório do Trabalho 2 - Busca com Adversário

## 1. Identificação
* **Nomes:** Aline Fraga da Silva(579723), Gabriel Ricci Pazinatto(578935) e Mariana Burzlaff Ercolani(579108)
* **Turma:** B

## 2. Bibliotecas Adicionais
* [Liste bibliotecas extras utilizadas ou informe que não foram utilizadas além das requeridas]

## 3. Tic-Tac-Toe Misere
### Resultados da Avaliação
(i) O minimax sempre ganha ou empata jogando contra o randomplayer?
**Resposta:** [Sim/Não - Relate o que ocorreu]

(ii) O minimax sempre empata consigo mesmo?
**Resposta:** [Sim/Não - Relate o que ocorreu]

(iii) O minimax não perde para você quando você usa a sua melhor estratégia?
**Resposta:** [Sim/Não - Relate o que ocorreu]

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
| agent_1 X agent_2 | agent_2 | 9 | 55 |
| agent_1 X agent_3 | agent_1 | 55 | 9 |
| agent_1 X agent_4 | agent_4 | 16 | 48 |
| agent_1 X agent_5 | agent_5 | 16 | 48 |
| agent_2 X agent_1 | agent_1 | 15 | 49 |
| agent_2 X agent_3 | agent_2 | 55 | 9 |
| agent_2 X agent_4 | agent_2 | 35 | 29 |
| agent_2 X agent_5 | agent_2 | 42 | 22 |
| agent_3 X agent_1 | agent_1 | 1 | 63 |
| agent_3 X agent_2 | agent_3 | 55 | 9 |
| agent_3 X agent_4 | agent_4 | 30 | 34 |
| agent_3 X agent_5 | agent_3 | 33 | 31 |
| agent_4 X agent_1 | agent_1 | 2 | 60 |
| agent_4 X agent_2 | agent_4 | 52 | 12 |
| agent_4 X agent_3 | agent_3 | 21 | 43 |
| agent_4 X agent_5 | agent_5 | 22 | 42 |
| agent_5 X agent_1 | agent_5 | 40 | 24 |
| agent_5 X agent_2 | agent_5 | 34 | 30 |
| agent_5 X agent_3 | agent_5 | 46 | 18 |
| agent_5 X agent_4 | agent_5 | 38 | 26 |

**Análise:** A implementação mais bem-sucedida de todas foi a **agent_5** (6 vitórias). Como previsto, a combinação completa das 10 estratégias e a transição dinâmica de heurísticas (Evaporação/Mobilidade no início, Estabilidade e Paridade no final) provou ser superior e consistentemente forte contra os demais agentes, vencendo todas as partidas em que jogou com as pretas e perdendo apenas quando jogou de brancas (devido à desvantagem natural do jogador branco e da simetria forçada do tempo baixo).

### Implementação Escolhida para o Torneio
* **Explicação:** Utilizaremos o **agent_5** (código base replicado para o `tournament_agent.py`), pois ele utiliza todas as 10 heurísticas descritas de maneira dinâmica baseada nas fases do jogo, maximizando as métricas de estabilidade e mobilidade enquanto evita armadilhas em padrões de borda. Juntamente ao Aprofundamento Iterativo, ele explora a árvore ao limite do tempo garantindo decisões de altíssima qualidade.

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