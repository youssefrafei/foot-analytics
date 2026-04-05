"""
foot_analytics - Outil d'analyse de statistiques de Premier League.

Ce package fournit des classes pour charger, manipuler et visualiser
les données d'une saison de Premier League.
"""

from foot_analytics.joueur import Joueur
from foot_analytics.equipe import Equipe
from foot_analytics.saison import Saison
from foot_analytics.dataloader import DataLoader

__all__ = ["Joueur", "Equipe", "Saison", "DataLoader"]
