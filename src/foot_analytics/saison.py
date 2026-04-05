"""
Module saison — Représentation d'une saison de Premier League.

La classe Saison regroupe plusieurs Equipe (agrégation) et fournit
des méthodes d'analyse à l'échelle de la ligue : classement,
meilleurs buteurs, meilleures attaques/défenses, etc.
"""

from __future__ import annotations
from typing import Iterator

from foot_analytics.equipe import Equipe
from foot_analytics.joueur import Joueur


class Saison:
    """
    Représente une saison complète de Premier League.

    Pattern : AGRÉGATION — Saison CONTIENT des Equipe.

    Attributes:
        annee: Identifiant de la saison (ex: '2023-2024')
    """

    def __init__(self, annee: str, equipes: list[Equipe] | None = None) -> None:
        if not annee or not annee.strip():
            raise ValueError("L'année de la saison ne peut pas être vide")

        self.annee = annee.strip()
        self._equipes: dict[str, Equipe] = {}

        if equipes:
            for equipe in equipes:
                self.ajouter_equipe(equipe)

    # ------------------------------------------------------------------ #
    #  Méthodes spéciales                                                 #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return f"Saison({self.annee!r}, {len(self)} équipes)"

    def __str__(self) -> str:
        return f"Premier League {self.annee} — {len(self)} équipes"

    def __len__(self) -> int:
        """Nombre d'équipes dans la saison."""
        return len(self._equipes)

    def __iter__(self) -> Iterator[Equipe]:
        """Itère sur les équipes."""
        return iter(self._equipes.values())

    def __contains__(self, nom_equipe: str) -> bool:
        """Teste si une équipe est dans la saison : 'Arsenal' in saison."""
        return nom_equipe in self._equipes

    # ------------------------------------------------------------------ #
    #  Gestion des équipes                                                #
    # ------------------------------------------------------------------ #

    def ajouter_equipe(self, equipe: Equipe) -> None:
        """Ajoute une équipe à la saison."""
        if not isinstance(equipe, Equipe):
            raise TypeError(f"Attendu une Equipe, reçu {type(equipe).__name__}")
        if equipe.nom in self._equipes:
            raise ValueError(f"{equipe.nom} est déjà dans la saison {self.annee}")
        self._equipes[equipe.nom] = equipe

    def get_equipe(self, nom: str) -> Equipe | None:
        """Récupère une équipe par son nom."""
        return self._equipes.get(nom)

    # ------------------------------------------------------------------ #
    #  Classement                                                         #
    # ------------------------------------------------------------------ #

    def classement(self) -> list[Equipe]:
        """
        Retourne le classement de la saison, trié par points décroissants.
        En cas d'égalité de points, la différence de buts départage.
        """
        return sorted(
            self._equipes.values(),
            key=lambda e: (e.points, e.difference_buts),
            reverse=True,
        )

    def afficher_classement(self) -> str:
        """Retourne le classement formaté sous forme de tableau lisible."""
        lignes = []
        header = (
            f"{'Pos':<4} {'Équipe':<22} {'MJ':>3} {'V':>3} {'N':>3} "
            f"{'D':>3} {'BP':>4} {'BC':>4} {'Diff':>5} {'Pts':>4}"
        )
        lignes.append(header)
        lignes.append("-" * len(header))

        for i, equipe in enumerate(self.classement(), start=1):
            ligne = (
                f"{i:<4} {equipe.nom:<22} {equipe.matchs_joues:>3} "
                f"{equipe.victoires:>3} {equipe.nuls:>3} {equipe.defaites:>3} "
                f"{equipe.buts_pour:>4} {equipe.buts_contre:>4} "
                f"{equipe.difference_buts:>+5} {equipe.points:>4}"
            )
            lignes.append(ligne)

        return "\n".join(lignes)

    # ------------------------------------------------------------------ #
    #  Analyses                                                           #
    # ------------------------------------------------------------------ #

    def meilleures_attaques(self, n: int = 5) -> list[Equipe]:
        """Retourne les n équipes ayant marqué le plus de buts."""
        return sorted(self._equipes.values(), key=lambda e: e.buts_pour, reverse=True)[:n]

    def meilleures_defenses(self, n: int = 5) -> list[Equipe]:
        """Retourne les n équipes ayant encaissé le moins de buts."""
        return sorted(self._equipes.values(), key=lambda e: e.buts_contre)[:n]

    def meilleurs_buteurs(self, n: int = 10) -> list[Joueur]:
        """Retourne les n meilleurs buteurs toutes équipes confondues."""
        tous_les_joueurs = [j for equipe in self for j in equipe]
        return sorted(tous_les_joueurs, key=lambda j: j.buts, reverse=True)[:n]

    def meilleurs_passeurs(self, n: int = 10) -> list[Joueur]:
        """Retourne les n meilleurs passeurs."""
        tous_les_joueurs = [j for equipe in self for j in equipe]
        return sorted(
            tous_les_joueurs, key=lambda j: j.passes_decisives, reverse=True
        )[:n]

    def meilleurs_contributions(self, n: int = 10) -> list[Joueur]:
        """Retourne les n joueurs avec le plus de G+A (buts + passes)."""
        tous_les_joueurs = [j for equipe in self for j in equipe]
        return sorted(
            tous_les_joueurs,
            key=lambda j: j.contributions_offensives,
            reverse=True,
        )[:n]

    def filtrer_joueurs_par_poste(self, poste: str) -> list[Joueur]:
        """Retourne tous les joueurs d'un poste donné dans la ligue."""
        if poste not in Joueur.POSTES_VALIDES:
            raise ValueError(
                f"Poste invalide : {poste!r}. "
                f"Postes acceptés : {Joueur.POSTES_VALIDES}"
            )
        return [j for equipe in self for j in equipe if j.poste == poste]
