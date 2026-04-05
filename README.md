# Foot Analytics — Analyse de la Premier League

Outil d'analyse de statistiques de la Premier League (saison 2023-2024), développé dans le cadre du cours de Python L3 Économie Appliquée.

## Structure du projet

```
foot_analytics/
├── data/                          # Données CSV
│   ├── equipes.csv                # Stats des 20 équipes
│   └── joueurs.csv                # Stats individuelles des joueurs
├── src/
│   └── foot_analytics/
│       ├── __init__.py            # Package init
│       ├── joueur.py              # Classe Joueur
│       ├── equipe.py              # Classe Equipe (agrégation de Joueur)
│       ├── saison.py              # Classe Saison (agrégation d'Equipe)
│       ├── dataloader.py          # Chargement des CSV avec pandas
│       └── visualisation.py       # Graphiques matplotlib
├── main.py                        # Script de démonstration
├── pyproject.toml                 # Configuration du projet
└── README.md
```

## Architecture

Le projet repose sur trois classes organisées par composition et agrégation :

```
Saison (2023-2024)
├── Equipe: Manchester City (28V 7N 3D, 91 pts)
│   ├── Joueur: Erling Haaland (Attaquant, 27 buts)
│   ├── Joueur: Phil Foden (Milieu, 19 buts)
│   └── ...
├── Equipe: Arsenal (28V 5N 5D, 89 pts)
│   ├── Joueur: Bukayo Saka (Milieu, 16 buts)
│   └── ...
└── ...
```

- **Joueur** : brique de base, stocke les stats individuelles et calcule des métriques par 90 minutes
- **Equipe** : agrège des Joueur, fournit les stats collectives et le filtrage par poste
- **Saison** : agrège des Equipe, permet le classement et les analyses transversales
- **DataLoader** : lit les CSV avec pandas et instancie les objets

## Concepts Python mobilisés

- Programmation orientée objet : classes, composition, agrégation
- Méthodes spéciales : `__repr__`, `__str__`, `__len__`, `__iter__`, `__contains__`
- Décorateur `@property` pour les attributs calculés
- Type hints
- Gestion des exceptions (`ValueError`, `TypeError`, `FileNotFoundError`)
- Collections : listes, dictionnaires, compréhensions
- Manipulation de données avec pandas
- Visualisation avec matplotlib

## Installation

```bash
# Cloner le repo
git clone https://github.com/<username>/foot-analytics.git
cd foot-analytics

# Créer un environnement virtuel et installer
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

pip install -e .
```

## Utilisation

```bash
python main.py
```

Le script affiche dans le terminal :
- Le classement complet de la saison
- Les meilleures attaques et défenses
- Le top 10 des buteurs et des contributeurs (G+A)
- Le détail d'une équipe (Arsenal)

Et génère dans le dossier `output/` :
- `classement.png` : barplot du classement
- `attaque_defense.png` : nuage de points attaque vs défense
- `top_buteurs.png` : barplot des meilleurs buteurs
- `radar_comparaison.png` : radar comparant Haaland, Salah, Palmer et Watkins
