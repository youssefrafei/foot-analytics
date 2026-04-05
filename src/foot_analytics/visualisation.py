"""
Module visualisation — Graphiques d'analyse de la saison avec matplotlib.

Fournit des fonctions de visualisation : classement en barres, meilleures
attaques/défenses, top buteurs, et radar de comparaison de joueurs.
"""

from __future__ import annotations
import math

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from foot_analytics.saison import Saison
from foot_analytics.joueur import Joueur

# Backend non-interactif pour éviter les problèmes d'affichage
matplotlib.use("Agg")


def graphique_classement(saison: Saison, output: str = "classement.png") -> None:
    """
    Barplot horizontal du classement (points par équipe).

    Args:
        saison: Objet Saison à visualiser
        output: Chemin de sauvegarde de l'image
    """
    classement = saison.classement()
    noms = [e.nom for e in classement]
    points = [e.points for e in classement]

    # Inverser pour que le 1er soit en haut
    noms.reverse()
    points.reverse()

    fig, ax = plt.subplots(figsize=(10, 8))
    couleurs = plt.cm.RdYlGn(np.linspace(0, 1, len(noms)))
    ax.barh(noms, points, color=couleurs)
    ax.set_xlabel("Points")
    ax.set_title(f"Classement Premier League {saison.annee}")

    # Afficher la valeur sur chaque barre
    for i, v in enumerate(points):
        ax.text(v + 0.5, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"Graphique sauvegardé : {output}")


def graphique_attaque_defense(saison: Saison, output: str = "attaque_defense.png") -> None:
    """
    Nuage de points : buts marqués vs buts encaissés pour chaque équipe.

    Args:
        saison: Objet Saison à visualiser
        output: Chemin de sauvegarde
    """
    equipes = list(saison)
    bp = [e.buts_pour for e in equipes]
    bc = [e.buts_contre for e in equipes]
    pts = [e.points for e in equipes]

    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(bp, bc, c=pts, cmap="RdYlGn", s=120, edgecolors="black")
    plt.colorbar(scatter, ax=ax, label="Points")

    # Annoter chaque point avec le nom de l'équipe
    for equipe in equipes:
        ax.annotate(
            equipe.nom,
            (equipe.buts_pour, equipe.buts_contre),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=7,
        )

    ax.set_xlabel("Buts marqués")
    ax.set_ylabel("Buts encaissés")
    ax.set_title(f"Attaque vs Défense — Premier League {saison.annee}")

    # Zone idéale : beaucoup de buts marqués, peu encaissés (bas-droite)
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"Graphique sauvegardé : {output}")


def graphique_top_buteurs(saison: Saison, n: int = 15, output: str = "top_buteurs.png") -> None:
    """
    Barplot des n meilleurs buteurs de la saison.

    Args:
        saison: Objet Saison
        n: Nombre de joueurs à afficher
        output: Chemin de sauvegarde
    """
    buteurs = saison.meilleurs_buteurs(n)
    noms = [f"{j.nom} ({j.equipe})" for j in buteurs]
    buts = [j.buts for j in buteurs]

    # Inverser pour que le meilleur soit en haut
    noms.reverse()
    buts.reverse()

    fig, ax = plt.subplots(figsize=(10, 8))
    couleurs = plt.cm.Blues(np.linspace(0.3, 1.0, len(noms)))
    ax.barh(noms, buts, color=couleurs)
    ax.set_xlabel("Buts")
    ax.set_title(f"Top {n} Buteurs — Premier League {saison.annee}")

    for i, v in enumerate(buts):
        ax.text(v + 0.2, i, str(v), va="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"Graphique sauvegardé : {output}")


def radar_joueurs(
    joueurs: list[Joueur],
    output: str = "radar_comparaison.png",
) -> None:
    """
    Graphique radar comparant plusieurs joueurs sur des métriques clés.

    Les métriques sont normalisées entre 0 et 1 pour permettre la
    comparaison entre joueurs aux profils différents.

    Args:
        joueurs: Liste de joueurs à comparer (2 à 4 idéalement)
        output: Chemin de sauvegarde
    """
    if len(joueurs) < 2:
        raise ValueError("Il faut au moins 2 joueurs pour une comparaison radar")

    # Métriques à comparer
    categories = [
        "Buts/90",
        "Passes/90",
        "Efficacité tirs (%)",
        "Tirs cadrés",
        "Contributions/90",
        "Matchs joués",
    ]

    # Extraire les valeurs brutes de chaque joueur
    donnees_brutes: list[list[float]] = []
    for j in joueurs:
        donnees_brutes.append([
            j.buts_par_90,
            j.passes_par_90,
            j.efficacite_tirs,
            j.tirs_cadres,
            j.contributions_par_90,
            j.matchs_joues,
        ])

    # Normaliser chaque métrique entre 0 et 1 (par rapport au max du groupe)
    donnees_array = np.array(donnees_brutes)
    maxima = donnees_array.max(axis=0)
    # Éviter la division par zéro
    maxima[maxima == 0] = 1.0
    donnees_norm = donnees_array / maxima

    # Construction du radar
    n_categories = len(categories)
    angles = [n / n_categories * 2 * math.pi for n in range(n_categories)]
    angles += angles[:1]  # Fermer le polygone

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    couleurs = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    for i, joueur in enumerate(joueurs):
        valeurs = list(donnees_norm[i]) + [donnees_norm[i][0]]
        couleur = couleurs[i % len(couleurs)]
        ax.plot(angles, valeurs, "o-", linewidth=2, label=joueur.nom, color=couleur)
        ax.fill(angles, valeurs, alpha=0.15, color=couleur)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 1.1)
    ax.set_title("Comparaison de joueurs", fontsize=14, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Graphique sauvegardé : {output}")
