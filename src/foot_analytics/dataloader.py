"""
Module dataloader - Chargement des données depuis des fichiers CSV.

Le DataLoader lit les fichiers CSV (équipes et joueurs) à l'aide de pandas,
instancie les classes Joueur et Equipe, et les relie entre elles. Il rattache
automatiquement chaque Joueur à son Equipe correspondante et assemble le
tout dans un objet Saison.
"""

from __future__ import annotations
from pathlib import Path

import pandas as pd

from foot_analytics.joueur import Joueur
from foot_analytics.equipe import Equipe
from foot_analytics.saison import Saison


class DataLoader:
    """
    Charge et transforme les données CSV en objets Python.

    Attributes:
        data_dir: Chemin vers le dossier contenant les CSV
    """

    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Dossier introuvable : {self.data_dir}")

    def __repr__(self) -> str:
        return f"DataLoader({str(self.data_dir)!r})"

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    #  Chargement brut des CSV                                            #
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

    def charger_csv(self, nom_fichier: str) -> pd.DataFrame:
        """
        Lit un fichier CSV et retourne un DataFrame.

        Args:
            nom_fichier: Nom du fichier (ex: 'equipes.csv')

        Returns:
            DataFrame pandas contenant les données

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
        """
        chemin = self.data_dir / nom_fichier
        if not chemin.exists():
            raise FileNotFoundError(f"Fichier introuvable : {chemin}")
        return pd.read_csv(chemin)

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    #  Construction des objets                                            #
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

    def charger_equipes(self, nom_fichier: str = "equipes.csv") -> dict[str, Equipe]:
        """
        Charge les équipes depuis un CSV et retourne un dictionnaire {nom: Equipe}.
        """
        df = self.charger_csv(nom_fichier)

        colonnes_attendues = {
            "nom", "matchs_joues", "victoires", "nuls",
            "defaites", "buts_pour", "buts_contre", "points",
        }
        colonnes_manquantes = colonnes_attendues - set(df.columns)
        if colonnes_manquantes:
            raise ValueError(f"Colonnes manquantes dans {nom_fichier} : {colonnes_manquantes}")

        equipes: dict[str, Equipe] = {}
        for _, row in df.iterrows():
            equipe = Equipe(
                nom=row["nom"],
                matchs_joues=int(row["matchs_joues"]),
                victoires=int(row["victoires"]),
                nuls=int(row["nuls"]),
                defaites=int(row["defaites"]),
                buts_pour=int(row["buts_pour"]),
                buts_contre=int(row["buts_contre"]),
                points=int(row["points"]),
            )
            equipes[equipe.nom] = equipe

        return equipes

    def charger_joueurs(
        self,
        equipes: dict[str, Equipe],
        nom_fichier: str = "joueurs.csv",
    ) -> list[Joueur]:
        """
        Charge les joueurs depuis un CSV, les crée et les rattache à leur équipe.

        Args:
            equipes: Dictionnaire des équipes déjà chargées
            nom_fichier: Nom du fichier CSV

        Returns:
            Liste de tous les joueurs créés
        """
        df = self.charger_csv(nom_fichier)

        colonnes_attendues = {
            "nom", "equipe", "poste", "matchs_joues", "minutes_jouees",
            "buts", "passes_decisives", "tirs", "tirs_cadres",
            "cartons_jaunes", "cartons_rouges",
        }
        colonnes_manquantes = colonnes_attendues - set(df.columns)
        if colonnes_manquantes:
            raise ValueError(f"Colonnes manquantes dans {nom_fichier} : {colonnes_manquantes}")

        joueurs: list[Joueur] = []
        for _, row in df.iterrows():
            joueur = Joueur(
                nom=row["nom"],
                equipe=row["equipe"],
                poste=row["poste"],
                matchs_joues=int(row["matchs_joues"]),
                minutes_jouees=int(row["minutes_jouees"]),
                buts=int(row["buts"]),
                passes_decisives=int(row["passes_decisives"]),
                tirs=int(row["tirs"]),
                tirs_cadres=int(row["tirs_cadres"]),
                cartons_jaunes=int(row["cartons_jaunes"]),
                cartons_rouges=int(row["cartons_rouges"]),
            )
            joueurs.append(joueur)

            # Rattacher le joueur à son équipe si elle existe
            if joueur.equipe in equipes:
                try:
                    equipes[joueur.equipe].ajouter_joueur(joueur)
                except ValueError:
                    # Joueur déjà présent (doublon dans le CSV)
                    pass

        return joueurs

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
    #  Méthode principale : charger une saison complète                   #
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #

    def charger_saison(
        self,
        annee: str,
        fichier_equipes: str = "equipes.csv",
        fichier_joueurs: str = "joueurs.csv",
    ) -> Saison:
        """
        Charge une saison complète : équipes + joueurs rattachés.

        Args:
            annee: Identifiant de la saison (ex: '2023-2024')
            fichier_equipes: Nom du CSV des équipes
            fichier_joueurs: Nom du CSV des joueurs

        Returns:
            Objet Saison prêt à être analysé
        """
        equipes = self.charger_equipes(fichier_equipes)
        self.charger_joueurs(equipes, fichier_joueurs)

        saison = Saison(annee, equipes=list(equipes.values()))
        return saison
