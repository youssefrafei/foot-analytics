"""
Module joueur — Représentation d'un joueur de football et de ses statistiques.

Ce module constitue la brique de base du projet. La classe Joueur encapsule
les statistiques individuelles d'un joueur sur une saison et expose des
métriques dérivées via des propriétés (@property).
"""

from __future__ import annotations


class Joueur:
    """
    Représente un joueur de football avec ses statistiques sur une saison.

    Attributes:
        nom: Nom complet du joueur
        equipe: Nom du club
        poste: Position sur le terrain (Gardien, Defenseur, Milieu, Attaquant)
        matchs_joues: Nombre de matchs disputés
        minutes_jouees: Minutes totales jouées
        buts: Nombre de buts marqués
        passes_decisives: Nombre de passes décisives
        tirs: Nombre total de tirs
        tirs_cadres: Nombre de tirs cadrés
        cartons_jaunes: Nombre de cartons jaunes
        cartons_rouges: Nombre de cartons rouges
    """

    POSTES_VALIDES: list[str] = ["Gardien", "Defenseur", "Milieu", "Attaquant"]

    def __init__(
        self,
        nom: str,
        equipe: str,
        poste: str,
        matchs_joues: int = 0,
        minutes_jouees: int = 0,
        buts: int = 0,
        passes_decisives: int = 0,
        tirs: int = 0,
        tirs_cadres: int = 0,
        cartons_jaunes: int = 0,
        cartons_rouges: int = 0,
    ) -> None:
        # --- Validation des entrées ---
        if not nom or not nom.strip():
            raise ValueError("Le nom du joueur ne peut pas être vide")
        if not equipe or not equipe.strip():
            raise ValueError("Le nom de l'équipe ne peut pas être vide")
        if poste not in self.POSTES_VALIDES:
            raise ValueError(
                f"Poste invalide : {poste!r}. "
                f"Postes acceptés : {self.POSTES_VALIDES}"
            )
        if minutes_jouees < 0 or matchs_joues < 0:
            raise ValueError("Les minutes et matchs ne peuvent pas être négatifs")
        if buts < 0 or passes_decisives < 0:
            raise ValueError("Les buts et passes ne peuvent pas être négatifs")

        self.nom = nom.strip()
        self.equipe = equipe.strip()
        self.poste = poste
        self.matchs_joues = matchs_joues
        self.minutes_jouees = minutes_jouees
        self.buts = buts
        self.passes_decisives = passes_decisives
        self.tirs = tirs
        self.tirs_cadres = tirs_cadres
        self.cartons_jaunes = cartons_jaunes
        self.cartons_rouges = cartons_rouges

    def __repr__(self) -> str:
        """Représentation technique (debug/développement)."""
        return (
            f"Joueur({self.nom!r}, {self.equipe!r}, {self.poste!r}, "
            f"{self.buts}G {self.passes_decisives}A)"
        )

    def __str__(self) -> str:
        """Représentation lisible (utilisateur)."""
        return f"{self.nom} ({self.equipe}) — {self.poste}"

    # ------------------------------------------------------------------ #
    #  Propriétés : métriques dérivées calculées à la demande             #
    # ------------------------------------------------------------------ #

    @property
    def buts_par_90(self) -> float:
        """Nombre de buts rapporté à 90 minutes de jeu."""
        if self.minutes_jouees == 0:
            return 0.0
        return (self.buts / self.minutes_jouees) * 90

    @property
    def passes_par_90(self) -> float:
        """Nombre de passes décisives rapporté à 90 minutes."""
        if self.minutes_jouees == 0:
            return 0.0
        return (self.passes_decisives / self.minutes_jouees) * 90

    @property
    def contributions_offensives(self) -> int:
        """Buts + passes décisives (G+A)."""
        return self.buts + self.passes_decisives

    @property
    def contributions_par_90(self) -> float:
        """(Buts + passes) rapportés à 90 minutes."""
        if self.minutes_jouees == 0:
            return 0.0
        return (self.contributions_offensives / self.minutes_jouees) * 90

    @property
    def efficacite_tirs(self) -> float:
        """Pourcentage de tirs cadrés par rapport au total de tirs."""
        if self.tirs == 0:
            return 0.0
        return (self.tirs_cadres / self.tirs) * 100

    @property
    def taux_conversion(self) -> float:
        """Pourcentage de tirs convertis en buts."""
        if self.tirs == 0:
            return 0.0
        return (self.buts / self.tirs) * 100

    @property
    def minutes_par_but(self) -> float | None:
        """Minutes jouées par but marqué. None si aucun but."""
        if self.buts == 0:
            return None
        return self.minutes_jouees / self.buts
