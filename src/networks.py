import networkx as nx
import numpy as np

def clean_degree_sequence(sequence):
    sequence = np.maximum(0, np.round(sequence)).astype(int)
    if sum(sequence) % 2 != 0:
        sequence[0] += 1
    return sequence

def generate_poisson_sequence(n, mean_degree=10):
    seq = np.random.poisson(lam=mean_degree, size=n)
    return clean_degree_sequence(seq)

def generate_negative_binomial_sequence(n, r=2, p=0.16):
    seq = np.random.negative_binomial(n=r, p=p, size=n)
    return clean_degree_sequence(seq)

def generate_power_law_sequence(n, gamma=2.5, min_degree=2, max_degree=500):
    seq_float = nx.utils.powerlaw_sequence(n, exponent=gamma)
    seq = np.floor(seq_float).astype(int)
    seq = np.clip(seq, min_degree, max_degree)
    return clean_degree_sequence(seq)

def build_network_from_sequence(sequence):
    multi_g = nx.configuration_model(sequence)
    g = nx.Graph(multi_g)
    g.remove_edges_from(nx.selfloop_edges(g))
    return g

def generate_network(network_type, n=10000, **kwargs):
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
        
    return build_network_from_sequence(sequence)