import subprocess
import itertools
import xml.etree.ElementTree as ET
import os
import concurrent.futures

def run_match(pair):
    black, white = pair
    print(f"Starting match: {black} (B) vs {white} (W)")
    output_file = f"results_{black}_{white}.xml"
    history_file = f"history_{black}_{white}.txt"
    
    cmd = [
        "python3", "server.py", "othello", 
        f"advsearch/your_agent/{black}.py", 
        f"advsearch/your_agent/{white}.py", 
        "-d", "5.0", 
        "-o", output_file,
        "-l", history_file
    ]
    
    # Run the server silently
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Parse the output
    if os.path.exists(output_file):
        tree = ET.parse(output_file)
        root = tree.getroot()
        
        p_black = root.find("./player[@color='B']")
        p_white = root.find("./player[@color='W']")
        
        score_b = int(p_black.get("score"))
        score_w = int(p_white.get("score"))
        
        if score_b > score_w:
            winner = black
        elif score_w > score_b:
            winner = white
        else:
            winner = "Draw"
            
        print(f"Result: {winner} won! ({score_b} - {score_w}) [Match: {black} vs {white}]")
        # os.remove(output_file) # Optional cleanup
        return {
            "black": black,
            "white": white,
            "winner": winner,
            "score_black": score_b,
            "score_white": score_w
        }
    else:
        print(f"Failed to find results for {black} vs {white}")
        return None

def run_tournament():
    agents = [
        "agent_1",
        "agent_2",
        "agent_3",
        "agent_4",
        "agent_5"
    ]
    
    pairs = list(itertools.permutations(agents, 2))
    
    results = []
    
    os.environ['OTHELLO_TIME_LIMIT'] = '4.9'
    
    # Run matches in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        futures = {executor.submit(run_match, pair): pair for pair in pairs}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                results.append(res)

    print("\n\n### Resultados do Torneio")
    print("| Partida (B x W) | Vencedor | Peças B | Peças W |")
    print("|---|---|---|---|")
    for r in results:
        print(f"| {r['black']} X {r['white']} | {r['winner']} | {r['score_black']} | {r['score_white']} |")
        
    # Determine the absolute best agent
    wins = {a: 0 for a in agents}
    for r in results:
        if r['winner'] in wins:
            wins[r['winner']] += 1
            
    print("\n### Vitórias por Agente")
    for agent, win_count in sorted(wins.items(), key=lambda x: x[1], reverse=True):
        print(f"- {agent}: {win_count}")
        
    best_agent = max(wins, key=wins.get)
    print(f"\n**Análise:** A implementação mais bem-sucedida de todas foi a `{best_agent}`, com {wins[best_agent]} vitórias.")

if __name__ == "__main__":
    run_tournament()
