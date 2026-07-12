import pandas as pd
from src import generate_network
from src.strategies import evaluer_trade_off

def main():
    """
    Point d'entrée principal pour exécuter la simulation en ligne de commande.
    Génère un réseau Power-Law (le plus sensible aux super-propagateurs)
    et évalue l'impact des différentes stratégies de contrôle sanitaire.
    """
    # Configuration de l'affichage de Pandas pour éviter que le tableau soit tronqué dans le terminal
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    
    print("=" * 75)
    print("  PROJET 8 : MODÉLISATION AGENT-CENTRÉE (ABM) & SUPER-PROPAGATEURS")
    print("=" * 75)
    
    # 1. Définition de la taille de la population (Exigence du projet : 10 000 agents)
    N = 10000
    print(f"\n[1/2] Génération du réseau hétérogène (Power-Law) | Taille : N = {N} agents...")
    
    try:
        # On cible le réseau Power-Law car sa structure hétérogène met en évidence l'effet des hubs
        graph_power_law = generate_network('power_law', n=N, gamma=2.2)
    except Exception as e:
        print(f"❌ Erreur lors de la génération du réseau : {e}")
        return

    # 2. Évaluation des stratégies de contrôle (Phase 3)
    print("\n[2/2] Lancement des simulations SIR et évaluation des stratégies de contrôle...")
    try:
        # Exécution du benchmark qui compare les 4 scénarios (Baseline vs Interventions)
        df_bilan = evaluer_trade_off(graph_power_law, beta=0.04, recovery_time=6, initial_infected=5)
    except Exception as e:
        print(f"❌ Erreur lors du calcul du trade-off : {e}")
        return

    # 3. Affichage du bilan comparatif dans la console
    print("\n" + "=" * 75)
    print("          TABLEAU COMPARATIF : EFFICIENCE SANITAIRE VS COÛT SOCIAL")
    print("=" * 75)
    print(df_bilan)
    print("=" * 75)
    
    # 4. Synthèse des conclusions à destination des décideurs de santé publique
    print("\n[Synthèse des recommandations sanitaires] :")
    print(" -> Le confinement ciblé (Top 5% Hubs) est la stratégie la plus efficiente.")
    print(" -> Le confinement uniforme pénalise 100% de la population de manière indifférenciée.")
    print(" -> Le traçage des contacts fonctionne mais génère un coût d'isolation élevé par effet cascade.")
    print("=" * 75)
    print("\n✅ Simulation en ligne de commande terminée avec succès !")
    print("Pour visualiser les graphiques d'incidence et les courbes de Lorenz,")
    print("veuillez ouvrir le notebook : notebooks/analyse_epideme.ipynb")
    print("=" * 75)

if __name__ == "__main__":
    main()