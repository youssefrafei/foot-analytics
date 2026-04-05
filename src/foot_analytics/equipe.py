"""
Module equipe - Représentation d'une équipe de football.

La classe Equipe utilise le pattern d'AGRÉGATION : elle contient une
collection de Joueur, mais ceux-ci peuvent exister indépendamment.
Elle implémente les protocoles d'itération et de conteneur pour une
utilisation pythonique (len, for, in).
"""

from __future__ import annotations
from typing import Iterator

from foot_analytics.joueur import Joueur


class Equipe:
    """
    Représente une équipe de Premier League sur une saison.

    Pattern : AGRÉGATION - Equipe CONTIENT des Joueur.

    Attributes:
        nom: Nom du club
        matchs_joues: Nombre de matchs joués
        victoires: Nombre de victoires
        nuls: Nombre de matchs nuls
        defaites: Nombre de défaites
        buts_pour: Buts marqués par l'équipe
        buts_contre: Buts encaissés
        points: Total de points au classement
    """

    def __init__(
        self,
        nom: str,
        matchs_joues: int = 0,
        victoires: int = 0,
        nuls: int = 0,
        defaites: int = 0,
        buts_pour: int = 0,
        buts_contre: int = 0,
        points: int = 0,
    ) -> None:
        if not nom or not nom.strip():
            raise ValueError("Le nom de l'équipe ne peut pas être vide")

        self.nom = nom.strip()
        self.matchs_joues = matchs_joues
        self.victoires = victoires
        self.nuls = nuls
        self.defaites = defaites
        self.buts_pour = buts_pour
        self.buts_contre = buts_contre
        self.points = points
        self._joueurs: list[Joueur] = []

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    #  Méthodes spéciales                                                #
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

    def __repr__(self) -> str:
        return f"Equipe({self.nom!r}, {self.points}pts, {len(self._joueurs)} joueurs)"

    def __str__(self) -> str:
        return f"{self.nom} — {self.points} pts ({self.victoires}V {self.nuls}N {self.defaites}D)"

    def __len__(self) -> int:
        """Nombre de joueurs dans l'effectif."""
        return len(self._joueurs)

    def __iter__(self) -> Iterator[Joueur]:
        """Permet d'itérer sur les joueurs : for joueur in equipe."""
        return iter(self._joueurs)

    def __contains__(self, nom_joueur: str) -> bool:
        """Permet de tester : 'Haaland' in equipe."""
        return any(j.nom == nom_joueur for j in self._joueurs)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    #  Gestion de l'effectif                                              #
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

    def ajouter_joueur(self, joueur: Joueur) -> None:
        """Ajoute un joueur à l'effectif."""
        if not isinstance(joueur, Joueur):
            raise TypeError(f"Attendu un Joueur, reçu {type(joueur).__name__}")
        if joueur.nom in self:
            raise ValueError(f"{joueur.nom} est déjà dans l'effectif de {self.nom}")
        self._joueurs.append(joueur)

    def get_joueur(self, nom: str) -> Joueur | None:
        """Récupère un joueur par son nom. Retourne None si introuvable."""
        for joueur in self._joueurs:
            if joueur.nom == nom:
                return joueur
        return None

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    #  Propriétés : métriques collectives                                 #
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

    @property
    def difference_buts(self) -> int:
        """Différence de buts (buts pour − buts contre)."""
        return self.buts_pour - self.buts_contre

    @property
    def buts_par_match(self) -> float:
        """Moyenne de buts marqués par match."""
        if self.matchs_joues == 0:
            return 0.0
        return self.buts_pour / self.matchs_joues

    @property
    def buts_encaisses_par_match(self) -> float:
        """Moyenne de buts encaissés par match."""
        if self.matchs_joues == 0:
            return 0.0
        return self.buts_contre / self.matchs_joues

    @property
    def pourcentage_victoires(self) -> float:
        """Taux de victoires en pourcentage."""
        if self.matchs_joues == 0:
            return 0.0
        return (self.victoires / self.matchs_joues) * 100

    @property
    def points_par_match(self) -> float:
        """Moyenne de points par match."""
        if self.matchs_joues == 0:
            return 0.0
        return self.points / self.matchs_joues

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    #  Filtrage et classement de l'effectif                               #
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

    def joueurs_par_poste(self, poste: str) -> list[Joueur]:
        """Filtre les joueurs par poste."""
        if poste not in Joueur.POSTES_VALIDES:
            raise ValueError(
                f"Poste invalide : {poste!r}. "
                f"Postes acceptés : {Joueur.POSTES_VALIDES}"
            )
        return [j for j in self._joueurs if j.poste == poste]

    def meilleur_buteur(self) -> Joueur | None:
        """Retourne le meilleur buteur de l'équipe."""
        if not self._joueurs:
            return None
        return max(self._joueurs, key=lambda j: j.buts)

    def meilleur_passeur(self) -> Joueur | None:
        """Retourne le meilleur passeur de l'équipe."""
        if not self._joueurs:
            return None
        return max(self._joueurs, key=lambda j: j.passes_decisives)
