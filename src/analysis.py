"""
analysis.py

Fonctions d'analyse statistique pour le Projet 8 :
Modélisation Agent-Centrée (ABM) pour l'étude des super-propagateurs.

"""

import numpy as np
import pandas as pd

from .simulation import ABMSimulation


# R0 EFFECTIF


def compute_effective_r0(transmissions):
    """
    Calcule le nombre de reproduction effectif (R0).

    Parameters
    ----------
    transmissions : dict
        Dictionnaire {agent_id: nombre de transmissions secondaires}

    Returns
    -------
    float
    """

    values = np.array(list(transmissions.values()), dtype=float)

    if values.size == 0:
        return 0.0

    return values.mean()



# INDICE DE DISPERSION


def compute_dispersion_index(transmissions):
    """
    Calcule l'indice de dispersion.

        ID = variance / moyenne
    """

    values = np.array(list(transmissions.values()), dtype=float)

    if values.size == 0:
        return 0.0

    mean = values.mean()

    if mean == 0:
        return 0.0

    return values.var() / mean



# PERCENTILE RESPONSABLE DE X% DES TRANSMISSIONS


def compute_pareto_percentile(transmissions, target_share=0.80):
    """
    Détermine le plus petit percentile d'agents responsable
    de target_share des infections.

    Parameters
    ----------
    transmissions : dict

    target_share : float
        Part cumulée des infections (par défaut 80%)

    Returns
    -------
    percentile : float
        Pourcentage minimal d'agents

    share : float
        Part réellement atteinte (%)
    """

    values = np.array(list(transmissions.values()), dtype=float)

    if values.sum() == 0:
        return 0.0, 0.0

    values = np.sort(values)[::-1]

    cumulative = np.cumsum(values)

    cumulative /= cumulative[-1]

    idx = np.argmax(cumulative >= target_share)

    percentile = (idx + 1) / len(values) * 100

    share = cumulative[idx] * 100

    return percentile, share


# PROBABILITE D'EXTINCTION


def compute_extinction_probability(
    graph,
    beta=0.04,
    recovery_time=6,
    initial_infected=5,
    max_days=100,
    extinction_threshold=50,
    n_simulations=100
):
    """
    Estime la probabilité d'extinction précoce
    de l'épidémie.

    Une simulation est considérée comme éteinte
    si moins de extinction_threshold individus
    ont été infectés.
    """

    extinct = 0

    for _ in range(n_simulations):

        sim = ABMSimulation(
            graph=graph,
            beta=beta,
            recovery_time=recovery_time,
            initial_infected=initial_infected
        )

        history, _ = sim.run(max_days=max_days)

        total_cases = history["R"][-1]

        if total_cases < extinction_threshold:
            extinct += 1

    return extinct / n_simulations



# TABLEAU DE SYNTHESE


def summarize_network(transmissions):
    """
    Résumé statistique d'un réseau.

    Returns
    -------
    pandas.Series
    """

    r0 = compute_effective_r0(transmissions)

    dispersion = compute_dispersion_index(transmissions)

    percentile80, _ = compute_pareto_percentile(
        transmissions,
        target_share=0.80
    )

    record = max(transmissions.values()) if transmissions else 0

    return pd.Series({

        "R0 effectif": round(r0, 3),

        "Indice de dispersion": round(dispersion, 3),

        "Transmission maximale": record,

        "Percentile responsable de 80% des infections (%)":
            round(percentile80, 2)

    })



# COMPARAISON DE PLUSIEURS RESEAUX


def compare_networks(transmissions_dict):
    """
    Produit un tableau comparatif des différents réseaux.

    Parameters
    ----------
    transmissions_dict : dict

        {
            "Poisson": transmissions,
            "Power-Law": transmissions,
            ...
        }

    Returns
    -------
    pandas.DataFrame
    """

    results = {}

    for name, transmissions in transmissions_dict.items():

        results[name] = summarize_network(transmissions)

    return pd.DataFrame(results).T