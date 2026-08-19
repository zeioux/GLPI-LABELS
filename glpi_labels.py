import configparser
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd
import qrcode
from fpdf import FPDF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.ini")


def load_config():
    # fail fast, pas de retry ni de valeurs par défaut, si config absente tant pis 
    if not os.path.exists(CONFIG_PATH):
        print("Pas de config.ini -> copier config.example.ini et remplir.")
        sys.exit(1)

    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding="utf-8")

    # strip anti-espace foireux en fin de ligne dans le ini
    base_url = cfg.get("glpi", "base_url", fallback="").strip()
    prefix_lieu = cfg.get("glpi", "prefix_lieu", fallback="").strip()

    if not base_url:
        print("base_url manquant dans config.ini")
        sys.exit(1)

    return base_url, prefix_lieu

# Avery L6140, 4x10, mm (dims de la fiche produit)
COLS, ROWS = 4, 10
LABEL_W, LABEL_H = 45.7, 25.4
GAP_X = 2.7
STEP_X, STEP_Y = LABEL_W + GAP_X, LABEL_H
X_START, Y_START = 9.5, 21.0

QR_SIZE = 18
QR_MARGIN_LEFT, QR_MARGIN_Y = 2.0, 2.9
TEXT_ZONE_X, TEXT_ZONE_W = 22.0, 23.0

def clean_location(valeur, prefix=""):
    # format GLPI: Site > Bâtiment > Salle
    # force str sinon pandas file un NaN/float et ça pete
    valeur = str(valeur).strip()

    # cases vides export CSV, ZZZ_ pour que ça tombe en dernier dans un tri alpha
    if pd.isna(valeur) or valeur in ("nan", ""):
        return "ZZZ_Inconnu", ""
    
    # enlève le préfixe si présent 
    if prefix and valeur.startswith(prefix):
        valeur = valeur.replace(prefix, "", 1).strip()

    # dept = 1er niveau, sous_dept = 2e si y'en a un, apres le reste pas besoin
    morceaux = valeur.split(" > ")
    dept = morceaux[0].strip()
    sous_dept = morceaux[1].strip() if len(morceaux) > 1 else ""
    return dept, sous_dept

def clear_user(valeur): 
    valeur = str(valeur).strip()
    if pd.isna(valeur) or valeur in ("nan", ""): 
        return "Sans Utilisateur" 
    # vire le '(123)' que GLPI colle après le no
    return re.sub(r"\s+\(d+\)$", "", valeur)

def choisir_csv():
    # popup file picker, root caché sinon on se tape une fenêtre vide en plus
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Sélectionner le fichier CSV exporté de GLPI",
        filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")],
    )