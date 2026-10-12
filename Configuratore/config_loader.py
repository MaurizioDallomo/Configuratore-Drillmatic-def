import os
import sys
import configparser

def risorsa_percorso(relative_path):
    """ Ottiene il percorso del config.ini all'esterno dell'exe di PyInstaller """
    # Se il programma è compilato con PyInstaller, sys.executable ci dà il percorso dell'exe
    if hasattr(sys, '_MEIPASS'):
        # Prende la cartella in cui si trova fisicamente il file .exe lanciato
        base_path = os.path.dirname(sys.executable)
    else:
        # Se siamo in sviluppo (main.py), usa la cartella corrente
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# Inizializzazione variabili
D_HOST = None
D_NAME = None
D_USER = None
D_PASS = None

percorso_config = risorsa_percorso("config.ini")
config = configparser.ConfigParser()

if os.path.exists(percorso_config):
    config.read(percorso_config, encoding='utf-8')
    try:
        D_HOST = config["DATABASE"]["host"]
        D_NAME = config["DATABASE"]["nome_db"]
        D_USER = config["DATABASE"]["utente"]
        D_PASS = config["DATABASE"]["password"]
    except KeyError as e:
        print(f"Errore: Manca la chiave {e} nel file config.ini!")
        sys.exit(1)
else:
    print(f"Errore critico: Il file config.ini non è stato trovato in: {percorso_config}")
    sys.exit(1)

# Stringa di configurazione globale
DB_CONFIG = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={D_HOST};"
    f"Database={D_NAME};"
    f"UID={D_USER};"
    f"PWD={D_PASS};"
    "TrustServerCertificate=yes;"
)