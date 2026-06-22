# Relatório do Trabalho 2 - Busca com Adversário

## 1. Identificação
* **Nomes:** Aline Fraga da Silva(579723), Gabriel Ricci Pazinatto(578935) e Mariana Burzlaff Ercolani(579108)
* **Turma:** B

## 2. Bibliotecas Adicionais
* Nenhuma biblioteca externa adicional foi utilizada.

## 3. Tic-Tac-Toe Misere
### Resultados da Avaliação
(i) O minimax sempre ganha ou empata jogando contra o randomplayer?
**Resposta:** Sim. Como o minimax explora a árvore de jogo completa, ele nunca toma uma decisão subótima que leve à derrota se puder evitar. Ele vence na grande maioria das vezes (quando o aleatório comete um erro, o que acontece com frequência) e empata no pior dos casos.

(ii) O minimax sempre empata consigo mesmo?
**Resposta:** Sim. Como os dois agentes minimax jogam perfeitamente, o jogo sempre termina em empate.

(iii) O minimax não perde para você quando você usa a sua melhor estratégia?
**Resposta:** Sim. O minimax tem performance super-humana em jogos com árvores rasas, como é o caso do tttm, pois consegue prever todas as jogadas possíveis. No melhor dos casos, é possível obter um empate.

## 4. Othello
### Heurísticas Customizadas
O agente toma decisões combinando as seguintes cinco heurísticas:

* **Controle de Cantos:** Prioriza a captura dos cantos do tabuleiro, por serem posições que não podem ser retomadas pelo adversário futuramente.
* **Proximidade de Cantos:** Penaliza jogar nas casas adjacentes a cantos vazios, por serem mais sucetíveis a futuras capturas do oponente.
* **Mobilidade:** Busca balancear quantidade de jogadas válidas do agente Vs. Quantidade de jogadas válidas do oponente, visando ter sempre mais opções de movimento que o adversário.
* **Discos de Fronteira:** Penaliza posições adjacentes a discos do oponente, pois estas podem ser capturadas futuramente com mais facilidade.
* **Paridade de Peças:** Avalia a diferença entre a quantidade de peças do agente e as do oponente, focando em ter mais peças no tabuleiro, especialmente ao final do jogo.

### Critério de Parada
* **Descrição:** Utilizamos Iterative Deepening com limite de tempo. O algoritmo busca sequencialmente em profundidades cada vez maiores, e, quando o tempo se esgota, retorna o melhor movimento encontrado na última iteração.

### Resultados do Mini-Torneio
| Partida (Agente 1 x Agente 2) | Vencedor | Peças Agente 1 | Peças Agente 2 |
|---|---|---|---|
| Contagem X Valor Posicional | Contagem | 33 | 31 |
| Valor Posicional X Contagem | Valor Posicional | 33 | 31 |
| Contagem X Customizada | Customizada | 0 | 64 |
| Customizada X Contagem | Customizada | 55 | 9 |
| Valor Posicional X Customizada | Customizada | 11 | 52 |
| Customizada X Valor Posicional | Customizada | 34 | 30 |


**Análise:** A implementação mais bem-sucedida de todas foi a customizada. O seu sucesso se deve à combinação das múltiplas estratégias utilizadas. Ao contrário da contagem pura (que captura peças prematuramente e pode acabar encurralada) ou do valor posicional (que é muito estático), a heurística customizada restringe as opções do adversário e busca posições seguras, o que é fundamental para dominar o tabuleiro no Othello.

### Implementação Escolhida para o Torneio
* **Explicação:** Para o torneio final, optamos pelo agente com a heurística Customizada (combinando controle de cantos, proximidade de cantos, mobilidade, discos de fronteira e paridade de peças). A decisão foi fundamentada diretamente pelo desempenho amplamente superior no mini-torneio, em que esta configuração dominou as estratégias estáticas e gulosas. Aliado a isso, o agente emprega o Minimax com Poda Alfa-Beta e Iterative Deepening, garantindo uma busca adaptável que maximiza a profundidade alcançada sempre dentro do limite de tempo.

## 5. Extras (Opcional)


## 6. Utilização de Chatbots ou Agentes de IA
* **Declaração:** O Gemini (tanto chatbot, quanto agente) foi utilizado para uma pesquisa inicial de estratégias e heurísticas que poderiam ser implementadas para desenvolver o agente jogador de Othello, tendo algumas delas sido implementadas. Depois dos integrantes implementarem as heurísticas, o Gemini foi usado para gerar um simulador de torneio, a fim de selecionar as melhores combinações de estratégias.  Além disso, a ferramenta auxiliou na revisão do código e na escrita deste relatório. Todas as decisões finais e interpretações de resultados foram tomadas pelos integrantes do grupo.   

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
