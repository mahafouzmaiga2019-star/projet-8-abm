
```markdown
# Projet 8 : Modélisation Agent-Centrée (ABM) et Impact des Super-Propagateurs

Ce projet implémente un modèle à base d'agents (ABM) pour simuler la propagation d'une épidémie selon la dynamique SIR (Sain, Infecté, Rétabli) au sein d'une population de 10 000 individus. L'objectif est d'analyser l'impact de l'hétérogénéité des réseaux de contacts sur la diffusion du virus et d'évaluer le compromis (\*trade-off\*) entre l'efficacité sanitaire et le coût social de plusieurs politiques de contrôle.

## Structure du Projet

```text
├── src/
│   ├── \_\_init\_\_.py          # Centralisation et exposition des modules
│   ├── networks.py          # Génération des réseaux (Poisson, Binomiale Négative, Power-Law)
│   ├── simulation.py        # Moteur de l'ABM et suivi des transmissions secondaires
│   └── strategies.py        # Algorithmes des scénarios d'intervention (Phase 3)
├── notebooks/
│   └── analyse\_epideme.ipynb # Analyses graphiques, statistiques et courbes de Lorenz
├── main.py                  # Point d'entrée principal en ligne de commande
├── requirements.txt         # Liste des dépendances Python
└── README.md                # Documentation et synthèse des résultats

```

## Installation

1. **Clonez ce dépôt GitHub** sur votre machine :

```bash
git clone \[https://github.com/votre-utilisateur/nom-du-depot.git](https://github.com/votre-utilisateur/nom-du-depot.git)
cd nom-du-depot

```



2. **Installez les dépendances** requises avec pip :

```bash
pip install -r requirements.txt

```



## Utilisation

### Exécution en ligne de commande

Pour exécuter une simulation de référence sur le réseau le plus sensible (*Power-Law*) et afficher le tableau comparatif du compromis coût/bénéfice des stratégies directement dans votre terminal :

```bash
python main.py

```

### Analyse visuelle (Jupyter Notebook)

Pour explorer les courbes d'incidence temporelles, valider la loi de Pareto et consulter les interprétations physiques détaillées :

1. Démarrez Jupyter : `jupyter notebook`
2. Ouvrez et exécutez le fichier `notebooks/analyse\_epideme.ipynb`.

## Synthèse des Conclusions Scientifiques

### 1\. Topologie des réseaux (Phases 1 \& 2)

* **Réseau de Poisson (Homogène)** : La propagation est lente et prévisible. L'indice de dispersion des transmissions secondaires reste proche de l'unité ($I\_D \\approx 1$), traduisant une dynamique égalitaire sans événements majeurs de super-propagation.
* **Réseau Power-Law (Hétérogène)** : La dynamique est explosive avec un pic d'incidence aigu et précoce. L'analyse de la courbe de Lorenz valide la loi de Pareto : le top 20% des agents les plus connectés engendre environ 70% des cas secondaires ($I\_D \\gg 1$).

### 2\. Évaluation des politiques sanitaires (Phase 3)

* **Confinement uniforme** : Très inefficace. Restreindre les contacts de l'ensemble de la population paralyse 100% de la société pour un bénéfice sanitaire linéaire et non optimal.
* **Confinement ciblé (Top 5% Hubs)** : C'est la stratégie la plus efficiente. Isoler préventivement une infime minorité d'agents hautement connectés suffit à casser les chaînes de transmission dominantes et à éteindre l'épidémie au coût social le plus bas.
* **Traçage dynamique des contacts** : Cette approche stoppe efficacement l'épidémie mais génère un coût d'isolement élevé et difficilement contrôlable en raison des mises en quarantaine en cascade dès qu'un hub est détecté.

```

```

