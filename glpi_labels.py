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
    # stop direct si le fichier de conf manque
    if not os.path.exists(CONFIG_PATH):
        print("Pas de config.ini -> copier config.example.ini et remplir.")
        sys.exit(1)

    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding="utf-8")

    # fallback string vide + strip pour évite de crash sur un espace en fin de ligne
    base_url = cfg.get("glpi", "base_url", fallback="").strip()
    prefix_lieu = cfg.get("glpi", "prefix_lieu", fallback="").strip()

    # L'URL GLPI est indispensable dpnc on bloque si elle est vide
    if not base_url:
        print("base_url manquant dans config.ini")
        sys.exit(1)

    return base_url, prefix_lieu

# Avery L6140 - 4x10, en mm
COLS, ROWS = 4, 10
LABEL_W, LABEL_H = 45.7, 25.4
GAP_X = 2.7
STEP_X, STEP_Y = LABEL_W + GAP_X, LABEL_H
X_START, Y_START = 9.5, 21.0

QR_SIZE = 18
QR_MARGIN_LEFT, QR_MARGIN_Y = 2.0, 2.9
TEXT_ZONE_X, TEXT_ZONE_W = 22.0, 23.0