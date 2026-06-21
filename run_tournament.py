import subprocess
import itertools
import xml.etree.ElementTree as ET
import os

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
    
    os.environ['OTHELLO_TIME_LIMIT'] = '0.4'
    
    for black, white in pairs:
        print(f"Running match: {black} (B) vs {white} (W)")
        output_file = f"results_{black}_{white}.xml"
        
        cmd = [
            "python", "server.py", "othello", 
            f"advsearch/your_agent/{black}.py", 
            f"advsearch/your_agent/{white}.py", 
            "-d", "0.5", # Fast delay for tournament speed
            "-o", output_file
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
                
            results.append({
                "black": black,
                "white": white,
                "winner": winner,
                "score_black": score_b,
                "score_white": score_w
            })
            
            print(f"Result: {winner} won! ({score_b} - {score_w})")
            # os.remove(output_file) # Optional cleanup
        else:
            print(f"Failed to find results for {black} vs {white}")

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
            
    best_agent = max(wins, key=wins.get)
    print(f"\n**Análise:** A implementação mais bem-sucedida de todas foi a `{best_agent}`, com {wins[best_agent]} vitórias.")

if __name__ == "__main__":
    run_tournament()
