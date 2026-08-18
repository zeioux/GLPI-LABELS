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
    if not os.path.exists(CONFIG_PATH):
        print("Pas de config.ini -> copier config.example.ini et remplir.")
        sys.exit(1)

    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding="utf-8")

    base_url = cfg.get("glpi", "base_url", fallback="").strip()
    prefix_lieu = cfg.get("glpi", "prefix_lieu", fallback="").strip()

    if not base_url:
        print("base_url manquant dans config.ini")
        sys.exit(1)

    return base_url, prefix_lieu
