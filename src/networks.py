import networkx as nx
import numpy as np

def clean_degree_sequence(sequence):
    """
    Nettoie et valide une séquence de degrés pour le Configuration Model.
    - Convertit les valeurs en entiers positifs.
    - S'assure que la somme des degrés est paire (obligatoire pour lier les nœuds deux à deux).
    """
    # Évite les valeurs négatives, arrondit et convertit en entiers
    sequence = np.maximum(0, np.round(sequence)).astype(int)
    
    # Si la somme totale des degrés est impaire, on ajoute 1 au premier élément pour la rendre paire
    if sum(sequence) % 2 != 0:
        sequence[0] += 1
        
    return sequence

def generate_poisson_sequence(n, mean_degree=10):
    """
    Génère une séquence de degrés suivant une loi de Poisson.
    Représente un réseau homogène (faible variance autour de la moyenne).
    """
    seq = np.random.poisson(lam=mean_degree, size=n)
    return clean_degree_sequence(seq)

def generate_negative_binomial_sequence(n, r=2, p=0.16):
    """
    Génère une séquence de degrés suivant une loi binomiale négative.
    Représente un réseau surdispersé (variance modérée).
    """
    seq = np.random.negative_binomial(n=r, p=p, size=n)
    return clean_degree_sequence(seq)

def generate_power_law_sequence(n, gamma=2.5, min_degree=2, max_degree=500):
    """
    Génère une séquence de degrés suivant une loi de puissance (Power-Law).
    Représente un réseau sans échelle fortement hétérogène (présence de super-propagateurs).
    """
    # Génère des valeurs flottantes suivant une loi de puissance via NetworkX
    seq_float = nx.utils.powerlaw_sequence(n, exponent=gamma)
    
    # Tronque à l'entier inférieur
    seq = np.floor(seq_float).astype(int)
    
    # Limite les degrés entre un minimum et un maximum pour éviter des hubs infinis ou des agents isolés
    seq = np.clip(seq, min_degree, max_degree)
    
    return clean_degree_sequence(seq)

def build_network_from_sequence(sequence):
    """
    Construit un graphe simple à partir d'une séquence de degrés via le Configuration Model.
    Élimine les multi-arêtes (liens doubles) et les boucles sur soi-même générées par le modèle.
    """
    # 1. Génération du multi-graphe brut (autorise les liens doubles et boucles)
    multi_g = nx.configuration_model(sequence)
    
    # 2. Conversion en graphe simple (supprime automatiquement les arêtes doubles)
    g = nx.Graph(multi_g)
    
    # 3. Suppression manuelle des boucles sur soi-même (un agent ne se connecte pas à lui-même)
    g.remove_edges_from(nx.selfloop_edges(g))
    
    return g

def generate_network(network_type, n=10000, **kwargs):
    """
    Fonction principale (Wrapper) pour générer le réseau selon la topologie souhaitée.
    
    Paramètres:
    -----------
    network_type : str ('poisson', 'negative_binomial', 'power_law')
    n : int (Nombre d'agents, par défaut 10 000)
    **kwargs : Paramètres spécifiques aux distributions (ex: mean_degree, gamma...)
    """
    if network_type == 'poisson':
        mean_degree = kwargs.get('mean_degree', 10)
        sequence = generate_poisson_sequence(n, mean_degree)
        
    elif network_type == 'negative_binomial':
        r = kwargs.get('r', 2)
        p = kwargs.get('p', 0.16)
        sequence = generate_negative_binomial_sequence(n, r, p)
        
    elif network_type == 'power_law':
        gamma = kwargs.get('gamma', 2.5)
        min_degree = kwargs.get('min_degree', 2)
        max_degree = kwargs.get('max_degree', 500)
        sequence = generate_power_law_sequence(n, gamma, min_degree, max_degree)
        
    else:
        raise ValueError(f"Type de réseau inconnu : {network_type}")
        
    # Construit et retourne le graphe simple nettoyé
    return build_network_from_sequence(sequence)