"""
Script principal — Démonstration des fonctionnalités de foot_analytics.

Ce script charge les données de la saison 2023-2024 de Premier League,
affiche des analyses dans le terminal et génère des visualisations.
"""

from pathlib import Path

from foot_analytics.dataloader import DataLoader
from foot_analytics.visualisation import (
    graphique_classement,
    graphique_attaque_defense,
    graphique_top_buteurs,
    radar_joueurs,
)


def main() -> None:
    # ------------------------------------------------------------------ #
    #  1. Chargement des données                                         #
    # ------------------------------------------------------------------ #
    data_dir = Path(__file__).parent / "data"
    loader = DataLoader(data_dir)
    saison = loader.charger_saison("2023-2024")
    print(f"Saison chargée : {saison}\n")

    # ------------------------------------------------------------------ #
    #  2. Classement                                                      #
    # ------------------------------------------------------------------ #
    print("=" * 70)
    print("CLASSEMENT")
    print("=" * 70)
    print(saison.afficher_classement())
    print()

    # ------------------------------------------------------------------ #
    #  3. Meilleures attaques et défenses                                #
    # ------------------------------------------------------------------ #
    print("=" * 70)
    print("TOP 5 MEILLEURES ATTAQUES")
    print("=" * 70)
    for equipe in saison.meilleures_attaques(5):
        print(f"  {equipe.nom:<22} {equipe.buts_pour} buts ({equipe.buts_par_match:.2f}/match)")

    print()
    print("=" * 70)
    print("TOP 5 MEILLEURES DÉFENSES")
    print("=" * 70)
    for equipe in saison.meilleures_defenses(5):
        print(f"  {equipe.nom:<22} {equipe.buts_contre} buts encaissés ({equipe.buts_encaisses_par_match:.2f}/match)")
    print()

    # ------------------------------------------------------------------ #
    #  4. Meilleurs buteurs                                               #
    # ------------------------------------------------------------------ #
    print("=" * 70)
    print("TOP 10 BUTEURS")
    print("=" * 70)
    for i, joueur in enumerate(saison.meilleurs_buteurs(10), start=1):
        mpb = joueur.minutes_par_but
        mpb_str = f"{mpb:.0f} min/but" if mpb is not None else "—"
        print(f"  {i:>2}. {joueur.nom:<22} {joueur.equipe:<20} {joueur.buts:>2} buts  ({mpb_str})")
    print()

    # ------------------------------------------------------------------ #
    #  5. Top contributions offensives (G+A)                             #
    # ------------------------------------------------------------------ #
    print("=" * 70)
    print("TOP 10 CONTRIBUTIONS (G+A)")
    print("=" * 70)
    for i, joueur in enumerate(saison.meilleurs_contributions(10), start=1):
        print(
            f"  {i:>2}. {joueur.nom:<22} {joueur.equipe:<20} "
            f"{joueur.buts:>2}G + {joueur.passes_decisives:>2}A = {joueur.contributions_offensives:>2}"
        )
    print()

    # ------------------------------------------------------------------ #
    #  6. Détail d'une équipe                                            #
    # ------------------------------------------------------------------ #
    arsenal = saison.get_equipe("Arsenal")
    if arsenal:
        print("=" * 70)
        print(f"FOCUS : {arsenal.nom}")
        print("=" * 70)
        print(f"  Points par match   : {arsenal.points_par_match:.2f}")
        print(f"  % de victoires     : {arsenal.pourcentage_victoires:.1f}%")
        print(f"  Différence de buts : {arsenal.difference_buts:+d}")
        print(f"  Effectif chargé    : {len(arsenal)} joueurs")

        buteur = arsenal.meilleur_buteur()
        passeur = arsenal.meilleur_passeur()
        if buteur:
            print(f"  Meilleur buteur    : {buteur.nom} ({buteur.buts} buts)")
        if passeur:
            print(f"  Meilleur passeur   : {passeur.nom} ({passeur.passes_decisives} passes)")
        print()

    # ------------------------------------------------------------------ #
    #  7. Visualisations                                                  #
    # ------------------------------------------------------------------ #
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("Génération des graphiques...")
    graphique_classement(saison, str(output_dir / "classement.png"))
    graphique_attaque_defense(saison, str(output_dir / "attaque_defense.png"))
    graphique_top_buteurs(saison, n=15, output=str(output_dir / "top_buteurs.png"))

    # Radar de comparaison : Haaland vs Salah vs Palmer vs Watkins
    joueurs_radar = []
    noms_cibles = ["Erling Haaland", "Mohamed Salah", "Cole Palmer", "Ollie Watkins"]
    for equipe in saison:
        for joueur in equipe:
            if joueur.nom in noms_cibles:
                joueurs_radar.append(joueur)

    if len(joueurs_radar) >= 2:
        radar_joueurs(joueurs_radar, str(output_dir / "radar_comparaison.png"))

    print("\nTerminé !")


if __name__ == "__main__":
    main()
