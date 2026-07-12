# src/simulation.py

import networkx as nx
import numpy as np

class ABMSimulation:
    def __init__(self, graph, beta=0.04, recovery_time=6, initial_infected=5):
        """
        Initialise le moteur de simulation ABM.
        
        Parameters:
        -----------
        graph : nx.Graph (Le réseau de contacts généré)
        beta : float (Probabilité de transmission par contact infectieux, défaut=0.04)
        recovery_time : int (Durée de l'infection en jours, défaut=6)
        initial_infected : int (Nombre de patients zéros au jour 0)
        """
        self.graph = graph.copy()  # Copie pour ne pas altérer le graphe d'origine
        self.beta = beta
        self.recovery_time = recovery_time
        self.initial_infected = initial_infected
        
        # Dictionnaires d'état des agents
        # États possibles : 'S' (Sain), 'I' (Infecté), 'R' (Rétabli), 'Q' (Quarantaine/Isolé)
        self.states = {node: 'S' for node in self.graph.nodes()}
        self.days_infected = {node: 0 for node in self.graph.nodes()}
        
        # Suivi des transmissions pour la Phase 2 (Super-propagateurs)
        self.secondary_infections = {node: 0 for node in self.graph.nodes()}
        
        # Historique quotidien pour les courbes d'incidence
        self.history = {'S': [], 'I': [], 'R': [], 'Q': []}
        
        # Variables de contrôle pour la Phase 3
        self.contact_tracing_active = False
        self.detection_prob = 0.0
        
        self._seed_infection()

    def _seed_infection(self):
        """Sélectionne aléatoirement les patients zéros au jour 0."""
        nodes = list(self.graph.nodes())
        initial_nodes = np.random.choice(nodes, size=self.initial_infected, replace=False)
        for node in initial_nodes:
            self.states[node] = 'I'

    def apply_confinement_uniforme(self, reduction_factor=0.5):
        """Phase 3 : Confinement uniforme (Réduction globale de la probabilité de transmission)."""
        self.beta = self.beta * (1 - reduction_factor)
        print(f"[Contrôle] Confinement uniforme appliqué. bêta réduit à {self.beta:.4f}")

    def apply_confinement_cible(self, top_percent=0.05):
        """Phase 3 : Confinement ciblé (Isole préventivement les x% agents les plus connectés)."""
        # Trier les nœuds par degré décroissant (les Hubs)
        degrees = dict(self.graph.degree())
        sorted_hubs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        
        num_hubs_to_isolate = int(len(self.graph.nodes()) * top_percent)
        hubs_to_isolate = [node for node, deg in sorted_hubs[:num_hubs_to_isolate]]
        
        # Placer les hubs en quarantaine
        for node in hubs_to_isolate:
            if self.states[node] != 'R':  # Ne pas isoler si déjà immunisé
                self.states[node] = 'Q'
        print(f"[Contrôle] Confinement ciblé appliqué : {num_hubs_to_isolate} hubs isolés (Top {top_percent*100}%).")

    def activate_contact_tracing(self, detection_prob=0.20):
        """Phase 3 : Active la stratégie dynamique de test et traçage des contacts."""
        self.contact_tracing_active = True
        self.detection_prob = detection_prob
        print(f"[Contrôle] Traçage des contacts activé (Probabilité de détection quotidienne : {detection_prob*100}%).")

    def _run_contact_tracing(self):
        """Logique interne du traçage : isole un infecté détecté et ses voisins directs."""
        current_infected = [n for n, state in self.states.items() if state == 'I']
        nodes_to_isolate = set()
        
        for node in current_infected:
            # Chaque jour, l'agent infecté a une probabilité d'être détecté
            if np.random.rand() < self.detection_prob:
                nodes_to_isolate.add(node)  # Isoler le cas index
                # Isoler tous ses voisins sains ou infectés (mais pas rétablis)
                for neighbor in self.graph.neighbors(node):
                    if self.states[neighbor] in ['S', 'I']:
                        nodes_to_isolate.add(neighbor)
                        
        # Appliquer l'isolement en quarantaine 'Q'
        for node in nodes_to_isolate:
            self.states[node] = 'Q'

    def step(self):
        """Exécute un pas de temps (1 jour) de la simulation ABM."""
        # 1. Gestion dynamique du traçage des contacts (Phase 3)
        if self.contact_tracing_active:
            self._run_contact_tracing()

        # Listes temporaires pour stocker les changements d'état du jour
        newly_infected = []
        infectors = {}  # Pour attribuer correctement la source de l'infection
        
        # 2. Phase de propagation
        current_infected = [n for n, state in self.states.items() if state == 'I']
        
        for infector in current_infected:
            # L'agent infecté interagit avec ses voisins directs
            for neighbor in self.graph.neighbors(infector):
                # La transmission ne peut avoir lieu que si le voisin est sain ('S')
                if self.states[neighbor] == 'S':
                    if np.random.rand() < self.beta:
                        if neighbor not in newly_infected:
                            newly_infected.append(neighbor)
                            infectors[neighbor] = infector

        # Mettre à jour l'état des nouveaux infectés et enregistrer la transmission secondaire
        for victim, infector in infectors.items():
            self.states[victim] = 'I'
            self.secondary_infections[infector] += 1

        # 3. Phase de guérison (Mise à jour des durées d'infection)
        for node in current_infected:
            self.days_infected[node] += 1
            if self.days_infected[node] >= self.recovery_time:
                self.states[node] = 'R'

        # 4. Enregistrement des statistiques de la journée
        counts = {'S': 0, 'I': 0, 'R': 0, 'Q': 0}
        for state in self.states.values():
            counts[state] += 1
            
        for key in self.history.keys():
            self.history[key].append(counts[key])

    def run(self, max_days=100):
        """Lance la simulation jusqu'à extinction du virus ou atteinte de la limite de jours."""
        for day in range(max_days):
            self.step()
            # Si plus aucun agent n'est infecté, l'épidémie est terminée
            if self.history['I'][-1] == 0:
                break
        return self.history, self.secondary_infections


# Bloc de test rapide (exécutable directement pour valider la logique)
if __name__ == "__main__":
    from networks import generate_network
    
    # 1. Générer un petit réseau de test
    g_test = generate_network('poisson', n=1000, mean_degree=10)
    
    # 2. Lancer la simulation de base
    sim = ABMSimulation(g_test, beta=0.04, recovery_time=6, initial_infected=5)[cite: 5]
    history, transmissions = sim.run(max_days=50)
    
    print("\nSimulation terminée avec succès !")
    print(f"Nombre final d'agents sains (S) : {history['S'][-1]}")
    print(f"Nombre final d'agents guéris (R) : {history['R'][-1]}")
    print(f"Max de transmissions causées par un seul agent : {max(transmissions.values())}")