# src/strategies.py

import pandas as pd
from .simulation import ABMSimulation

def run_baseline(graph, beta=0.04, recovery_time=6, initial_infected=5):
    """Exécute la simulation de référence sans aucune intervention informatique ou sanitaire."""
    sim = ABMSimulation(graph, beta=beta, recovery_time=recovery_time, initial_infected=initial_infected)
    history, transmissions = sim.run()
    
    # Indicateurs de performance
    total_infected = len(graph.nodes()) - history['S'][-1]
    cost = 0  # Aucun agent isolé
    
    return history, transmissions, {"Taille épidémie": total_infected, "Coût social (Isolés)": cost}

def run_confinement_uniforme(graph, reduction_factor=0.5, beta=0.04, recovery_time=6, initial_infected=5):
    """Exécute le scénario de distanciation sociale globale (réduction homogène du taux de contact)."""
    sim = ABMSimulation(graph, beta=beta, recovery_time=recovery_time, initial_infected=initial_infected)
    sim.apply_confinement_uniforme(reduction_factor)
    history, transmissions = sim.run()
    
    total_infected = len(graph.nodes()) - history['S'][-1]
    # Le coût social ici représente toute la population affectée par la baisse de contact
    cost = len(graph.nodes()) 
    
    return history, transmissions, {"Taille épidémie": total_infected, "Coût social (Isolés)": cost}

def run_confinement_cible(graph, top_percent=0.05, beta=0.04, recovery_time=6, initial_infected=5):
    """Exécute le scénario d'isolement préventif des hubs (les agents les plus connectés)."""
    sim = ABMSimulation(graph, beta=beta, recovery_time=recovery_time, initial_infected=initial_infected)
    sim.apply_confinement_cible(top_percent)
    history, transmissions = sim.run()
    
    total_infected = len(graph.nodes()) - history['S'][-1]
    cost = int(len(graph.nodes()) * top_percent)  # Uniquement les hubs mis en quarantaine
    
    return history, transmissions, {"Taille épidémie": total_infected, "Coût social (Isolés)": cost}

def run_traçage_contacts(graph, detection_prob=0.20, beta=0.04, recovery_time=6, initial_infected=5):
    """Exécute le scénario dynamique de test et d'isolement des cas index et de leurs voisins."""
    sim = ABMSimulation(graph, beta=beta, recovery_time=recovery_time, initial_infected=initial_infected)
    sim.activate_contact_tracing(detection_prob)
    history, transmissions = sim.run()
    
    total_infected = len(graph.nodes()) - history['S'][-1]
    # Nombre final d'agents qui ont fini dans l'état de quarantaine 'Q'
    cost = history['Q'][-1] 
    
    return history, transmissions, {"Taille épidémie": total_infected, "Coût social (Isolés)": cost}

def evaluer_trade_off(graph, beta=0.04, recovery_time=6, initial_infected=5):
    """
    Fonction maîtresse qui exécute l'ensemble des stratégies sur un même réseau 
    et compile un tableau comparatif pour optimiser le compromis efficacité/coût.
    """
    print("[Analyse] Lancement du benchmark des stratégies de contrôle...")
    
    # Exécution des 4 scénarios
    _, _, res_base = run_baseline(graph, beta, recovery_time, initial_infected)
    _, _, res_unif = run_confinement_uniforme(graph, 0.5, beta, recovery_time, initial_infected)
    _, _, res_cible = run_confinement_cible(graph, 0.05, beta, recovery_time, initial_infected)
    _, _, res_trace = run_traçage_contacts(graph, 0.20, beta, recovery_time, initial_infected)
    
    # Regroupement des résultats dans un DataFrame Pandas
    donnees = {
        "Pas d'intervention": res_base,
        "Confinement Uniforme (50%)": res_unif,
        "Confinement Ciblé (5% Hubs)": res_cible,
        "Traçage des Contacts (20%)": res_trace
    }
    
    df_tradeoff = pd.DataFrame(donnees).T
    # Calcul d'un score d'efficience simple : réduction des cas par agent confiné
    df_tradeoff["Cas évités"] = df_tradeoff.loc["Pas d'intervention", "Taille épidémie"] - df_tradeoff["Taille épidémie"]
    
    return df_tradeoff

# Bloc de test pour vérifier le bon fonctionnement du fichier
if __name__ == "__main__":
    import networkx as nx
    # Génération d'un petit graphe de test de 1000 nœuds
    g_test = nx.erdos_renyi_graph(n=1000, p=0.01)
    
    df_bilan = evaluer_trade_off(g_test)
    print("\n--- TABLEAU COMPARATIF DU TRADE-OFF ---")
    print(df_bilan)