# src/__init__.py

# Importations relatives pour exposer directement les fonctions et classes clés
from .networks import generate_network
from .simulation import ABMSimulation
from .strategies import (
    evaluer_trade_off, 
    run_baseline, 
    run_confinement_uniforme, 
    run_confinement_cible, 
    run_traçage_contacts
)

# Définition des éléments exportés publiquement
__all__ = [
    "generate_network",
    "ABMSimulation",
    "evaluer_trade_off",
    "run_baseline",
    "run_confinement_uniforme",
    "run_confinement_cible",
    "run_traçage_contacts"
]