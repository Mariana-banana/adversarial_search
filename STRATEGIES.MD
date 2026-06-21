Para aprimorar um agente de IA em Othello (geralmente estruturado sobre algoritmos como Minimax com poda Alpha-Beta), a função de avaliação estática é o componente mais crítico. Diferente do xadrez, focar primariamente na quantidade de peças durante a maior parte do jogo é uma falha estratégica grave.

Abaixo estão 6 heurísticas clássicas e altamente eficientes, fundamentadas pelos principais pesquisadores de Inteligência Artificial que desenvolveram programas de nível mundial (como Iago, Bill e Logistello):

1. Controle de Cantos (Corner Control)
Explicação: Os quatro cantos do tabuleiro são os pontos mais vitais do jogo. Uma vez que uma peça é colocada em um canto, ela se torna irremovível até o final da partida, pois não pode ser flanqueada em nenhuma direção. Além de permanentes, os cantos servem como ponto de ancoragem para capturar as bordas adjacentes de forma segura.
Como aplicar: Atribua um peso positivo exponencial para cada canto ocupado pela IA e uma penalidade equivalente para cantos sob posse do oponente.
Fonte: Rosenbloom, P. (1982). A world-championship-level Othello program (IAGO).

2. Proximidade de Cantos: Casas-X e Casas-C (Corner Closeness)
Explicação: Se os cantos são as casas mais valiosas, as posições adjacentes a eles são as mais perigosas. As "Casas-C" são adjacentes aos cantos de forma ortogonal, e as "Casas-X" ficam na diagonal exata do canto. Colocar uma peça nessas casas quando o canto correspondente ainda está vazio frequentemente permite que o oponente utilize essa mesma peça para flanquear e capturar o canto na jogada seguinte.
Como aplicar: Aplique uma forte penalidade (peso negativo) sempre que o agente considerar jogar em uma Casa-C ou Casa-X de um quadrante cujo canto ainda está vazio.
Fonte: Lee, K.-F., & Mahajan, S. (1990). The Development of a World Class Othello Program (BILL).

3. Mobilidade (Mobility)
Explicação: A mobilidade refere-se à quantidade de jogadas legais disponíveis. A macro-estratégia no Othello baseia-se em maximizar as próprias opções de jogada ao mesmo tempo em que se restringe as do oponente, forçando-o a fazer lances desvantajosos (como ser obrigado a jogar em uma Casa-X).
Como aplicar: Calcule o número de jogadas legais da IA menos o número de jogadas legais do oponente. Pode ser dividida em Mobilidade Atual (opções no turno corrente) e Mobilidade Potencial (número de casas vazias adjacentes a peças do oponente, indicando futuras opções de flanqueamento).
Fonte: Rosenbloom, P. (1982) e Buro, M. (1997).

4. Discos de Fronteira (Frontier Discs / Edge Control)
Explicação: Um disco de fronteira é uma peça que está diretamente ortogonal ou diagonal a pelo menos uma casa vazia. Ter muitas peças em contato com o espaço vazio no tabuleiro é altamente prejudicial, pois fornece "alvos" fáceis de flanqueamento para o adversário, aumentando a mobilidade dele na próxima rodada.
Como aplicar: Penalize a avaliação para cada peça do próprio agente que faz limite com uma casa não ocupada. O comportamento emergente dessa heurística forçará a IA a manter um agrupamento compacto de peças no centro do tabuleiro.
Fonte: Lee, K.-F., & Mahajan, S. (1990).

5. Estabilidade (Stability)
Explicação: Uma peça estável é aquela que não pode mais ser capturada pelo adversário em nenhum cenário possível até o final da partida, independentemente da sequência de jogadas futuras. Cantos são naturalmente estáveis, mas linhas contínuas presas a um canto ou formadas nas bordas (Edge Stability) também alcançam estabilidade.
Como aplicar: Detecte linhas sólidas construídas a partir de cantos garantidos e some a quantidade de discos invioláveis. É a métrica mais confiável de vantagem real no tabuleiro, mas computacionalmente pesada de se calcular dinamicamente.
Fonte: Rosenbloom, P. (1982).

6. Paridade de Peças (Coin Parity)
Explicação: Refere-se à simples diferença material: quantidade de discos da IA menos a quantidade de discos do oponente. Diferente de outros jogos de tabuleiro, capturar muitas peças precocemente no Othello é um erro, pois aumenta o perímetro de peças de fronteira e destrói a própria mobilidade.
Como aplicar: A Paridade só é eficiente se utilizada dinamicamente. Ela deve ter peso zero ou próximo de zero na abertura e no meio-jogo, e seu peso deve ser alavancado rapidamente apenas nas últimas 12 a 15 jogadas da partida, convertendo a estratégia do agente de "controle de território" para "captura em massa".
Fonte: Buro, M. (1997). Experiments with Multi-ProbCut and a New High-Quality Evaluation Function for Othello (Logistello).

Para implementar esse modelo com eficácia real em código, não utilize pesos fixos para o jogo inteiro. Construa uma matriz ou função que altere o peso de cada heurística dependendo do estágio do jogo (baseado no número de casas vazias restantes). Priorize Mobilidade e Fronteiras no início, e mude para Estabilidade e Paridade no final.

7. Paridade de Regiões Vazias (Region Parity)
Explicação: Diferente da paridade de peças (contagem de discos), a paridade de regiões foca no controle do último movimento. No Othello, fazer a última jogada em uma área vazia isolada é uma vantagem tática massiva, pois consolida a estabilidade local.
Como aplicar: O tabuleiro final frequentemente se divide em pequenas regiões desconexas de casas vazias. Se uma região tem um número ímpar de casas vazias, o primeiro jogador a entrar nela geralmente fará a última jogada. Se tiver um número par, o jogador que entrar por último fará a última jogada. O agente deve identificar essas áreas e priorizar jogar primeiro em regiões ímpares e forçar o oponente a abrir regiões pares.
Fonte: Buro, M. (1999). Toward Simple, Fast, and Robust Game-Tree Search.

8. Jogadas Silenciosas (Quiet Moves / Internal Captures)
Explicação: Uma jogada silenciosa ocorre quando o agente captura apenas discos internos do oponente — ou seja, os discos virados já estão completamente cercados por outras peças e não tocam nenhuma casa vazia. É a jogada defensiva mais poderosa do meio-jogo.
Como aplicar: Crie um bônus de avaliação para movimentos que não adicionam novos discos à fronteira do agente. Ao priorizar capturas internas, a IA joga de forma "invisível" nas bordas do adversário, reduzindo drasticamente a mobilidade do oponente sem expor suas próprias peças a flanqueamentos.
Fonte: Lee, K.-F., & Mahajan, S. (1990). The Development of a World Class Othello Program (BILL).

9. Avaliação por Padrões de Borda (Edge Configurations)
Explicação: As bordas do tabuleiro possuem dinâmicas táticas estritas e altamente mapeáveis. Padrões específicos, como possuir um bloco de 5 peças encostado na parede e vazio nos cantos (borda desbalanceada), são armadilhas fatais que permitem ao oponente sacrificar discos para conquistar um canto.
Como aplicar: Em vez de avaliar os discos de borda isoladamente, armazene uma tabela pré-calculada com todas as permutações possíveis para uma linha de borda de 8 casas. A IA deve consultar essa tabela de padrões (Edge Tables) para receber um bônus ou punição imediata com base na configuração geométrica formada na borda inteira.
Fonte: Buro, M. (1997). Experiments with Multi-ProbCut and a New High-Quality Evaluation Function for Othello (Logistello).

10.  Evaporação (Evaporation)
Explicação: Uma tática contra-intuitiva de abertura e transição inicial. O objetivo da evaporação é manter o número absoluto de peças do agente o mais próximo possível de zero durante as primeiras 20 jogadas. Ter poucas peças no tabuleiro significa necessariamente ter menos peças na fronteira.
Como aplicar: Atribua um peso negativo forte à quantidade total de discos da IA exclusivamente nas fases iniciais do jogo. O agente passará a priorizar linhas de jogo curtas que não causem grandes "viradas" no tabuleiro, forçando o oponente a expandir sua presença prematuramente e ficar sem opções legais seguras.
Fonte: Rosenbloom, P. (1982). A world-championship-level Othello program (IAGO) (implementada como um subconjunto agressivo da avaliação de controle de mobilidade em aberturas).


---


"Othello evaluation function weights" ou "Reversi heuristic functions": Você achará tabelas inteiras mostrando como graduar o tabuleiro e como medir a mobilidade.
Pesquise por "Logistello Michael Buro": Logistello é um dos robôs de Othello mais famosos da história, que derrotou o campeão mundial humano nos anos 90. O paper dele detalha como pesar as fases do jogo.
Pesquise por "Othello strategy X-squares and C-squares": Vai te mostrar mapas de calor (heatmaps) de onde jogar e onde nunca jogar, perfeito para aprimorar sua matriz de evaluate_mask.
"Alpha Beta Move Ordering Othello": Mostra a melhor ordem genérica para testar jogadas na árvore.