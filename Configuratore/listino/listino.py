from modelli.prodotto import Prodotto
from listino.prezzobasemandrino import PrezzoBaseMandrino
from listino.prezzobaseslitta import PrezzoBaseSlitta
from listino.prezzobaseunita import PrezzoBaseUnita
import pyodbc
from sqlalchemy import create_engine, event
import urllib
import datetime
import configparser
import os
import sys
from config_loader import D_HOST, D_DRIVER, D_NAME, D_USER, D_PASS, DB_CONFIG, risorsa_percorso

def _make_dict_cursor(connection, connection_record):
    def dict_row_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return dict(zip(fields, row))
    connection.row_factory = dict_row_factory

try:
    parametri = urllib.parse.quote_plus(DB_CONFIG)

    def connettore_diretto():
        certificato = "TrustServerCertificate=yes;" if "18" in D_DRIVER else ""
        
        stringa_dinamica = (
            f"Driver={{{D_DRIVER}}};"
            f"Server={D_HOST};"
            f"Database={D_NAME};"
            f"UID={D_USER};"
            f"PWD={D_PASS};"
            f"{certificato}"
        )
        return pyodbc.connect(stringa_dinamica)

    # Creiamo l'engine standard
    db_pool = create_engine(
        "mssql+pyodbc://",
        creator=connettore_diretto,
        pool_size=5,                     
        pool_reset_on_return='rollback'  
    )
    print("Connection Pool per SQL Server avviato con successo tramite connessione diretta!")

except Exception as err:
    print(f"Impossibile avviare il Connection Pool: {err}")
    db_pool = None

class Listino:
    def __init__(self):
        self.validita = datetime.date(2026, 9, 1)
        self.nome = ""
        self.prezzi_base_unita = {}
        self.prezzi_base_mandrini = {}
        self.prezzi_base_slitte = {}
        self.prezzi_mandrini = {}
        self.opzioni_escluse = {}
        self.prezzi_opzioni = {}
        
    def get_prezzo_base_unita(self, codice):
        return self.prezzi_base_unita.get(codice)

    def get_prezzo_base_mandrino(self, codice):
        return self.prezzi_base_mandrini.get(codice)

    def get_prezzo_base_slitta(self, codice):
        return self.prezzi_base_slitte.get(codice)

    def aggiungi_prezzo_base_unita(self, prodotto, corsa, prezzo, consegna):
        configurazione = PrezzoBaseUnita()
        configurazione.prodotto = prodotto
        configurazione.corsa = corsa
        configurazione.prezzo = prezzo
        configurazione.consegna = consegna
        chiave = f"{prodotto.codice} | {corsa.codice}"
        self.prezzi_base_unita[chiave] = configurazione

    def aggiungi_prezzo_base_mandrino(self, prodotto, cuscinetto, taglia, prezzo, consegna):
        configurazione = PrezzoBaseMandrino()
        configurazione.prodotto = prodotto
        configurazione.cuscinetto = cuscinetto
        configurazione.gr_motore = taglia
        configurazione.consegna = consegna
        configurazione.prezzo = prezzo
        chiave = f"{prodotto.codice} | {cuscinetto.codice} | {taglia}"
        self.prezzi_base_mandrini[chiave] = configurazione

    def aggiungi_prezzo_base_slitta(self, prodotto, corsa, prezzo, consegna):
        configurazione = PrezzoBaseSlitta()
        configurazione.prodotto = prodotto
        configurazione.corsa = corsa
        configurazione.prezzo = prezzo
        configurazione.consegna = consegna
        chiave = f"{prodotto.codice} | {corsa.codice}"
        self.prezzi_base_slitte[chiave] = configurazione

    def crea_prezzi_opzioni(self, prodotto, *valori):
        d = {}
        for coppia in valori:
            codice = coppia[0]
            prezzo = coppia[1]
            if codice in prodotto.opzioni_totali():
                d[codice] = prezzo
        return d

    def crea_prezzi_mandrini(self, prodotto, *valori):
        d = {}
        for coppia in valori:
            codice = coppia[0]
            prezzo = coppia[1]
            if codice in prodotto.mandrini:
                d[codice] = prezzo
        return d

    def popola_escludi_opzioni(self, prodotto, *valori):
        d = {}
        for op in valori:
            if op in prodotto.opzioni_totali():
                d[op] = True
        self.opzioni_escluse[prodotto.codice] = d

    def salta_opzione(self, prodotto, opzione):
        escluse_prodotto = self.opzioni_escluse.get(prodotto.codice)
        if not escluse_prodotto:
            return False
        return escluse_prodotto.get(opzione.codice, False)
    
    def carica(self, catalogo):

        if not db_pool:
            print("Errore: Il pool di connessioni non è attivo.")
            return
        
        self.prezzi_opzioni = {}
        self.prezzi_mandrini = {}

        with db_pool.raw_connection() as conn:
            with conn.cursor() as cursor:

                def fetch_as_dict(cur):
                    columns = [column[0] for column in cur.description]
                    return [dict(zip(columns, row)) for row in cur.fetchall()]
                
                # RIPRISTINATA LA QUERY CHE ERA STATA CANCELLATA
                cursor.execute("SELECT prodotto_codice, corsa_codice, prezzo, consegna FROM dbo.prezzi_base_unita")
                for row in fetch_as_dict(cursor):
                    p = catalogo.prodotti.get_prodotto(row['prodotto_codice'])
                    if p:
                        corsa = p.corse.get(row['corsa_codice'])
                        if corsa:
                            self.aggiungi_prezzo_base_unita(p, corsa, float(row['prezzo']), row['consegna'])

                cursor.execute("SELECT prodotto_codice, cuscinetto_codice, taglia, prezzo, consegna FROM dbo.prezzi_base_mandrini")
                for row in fetch_as_dict(cursor):
                    p = catalogo.prodotti.get_prodotto(row['prodotto_codice'])
                    if p:
                        cuscinetto = p.cuscinetti.get(row['cuscinetto_codice'])
                        if cuscinetto:
                            self.aggiungi_prezzo_base_mandrino(p, cuscinetto, row['taglia'], float(row['prezzo']), row['consegna'])

                cursor.execute("SELECT prodotto_codice, corsa_codice, prezzo, consegna FROM dbo.prezzi_base_slitte")
                for row in fetch_as_dict(cursor):
                    p = catalogo.prodotti.get_prodotto(row['prodotto_codice'])
                    if p:
                        corsa = p.corse.get(row['corsa_codice'])
                        if corsa:
                            self.aggiungi_prezzo_base_slitta(p, corsa, float(row['prezzo']), row['consegna'])

                cursor.execute("SELECT prodotto_codice, mandrino_codice, prezzo FROM dbo.prezzi_mandrini")
                for row in fetch_as_dict(cursor):
                    p = catalogo.prodotti.get_prodotto(row['prodotto_codice'])
                    if p:
                        if p.codice not in self.prezzi_mandrini:
                            self.prezzi_mandrini[p.codice] = {}
                        
                        codice_m = row['mandrino_codice']
                        if codice_m in p.mandrini:
                            self.prezzi_mandrini[p.codice][codice_m] = float(row['prezzo'])

                cursor.execute("SELECT prodotto_codice, opzione_codice, prezzo FROM dbo.prezzi_opzioni")
                for row in fetch_as_dict(cursor):
                    p = catalogo.prodotti.get_prodotto(row['prodotto_codice'])
                    if p:
                        if p.codice not in self.prezzi_opzioni:
                            self.prezzi_opzioni[p.codice] = {}
                        
                        codice_op = row['opzione_codice']
                        if codice_op in p.opzioni_totali():
                            self.prezzi_opzioni[p.codice][codice_op] = float(row['prezzo'])

                cursor.execute("SELECT prodotto_codice, opzione_codice FROM dbo.opzioni_escluse")
                for row in fetch_as_dict(cursor):
                    p = catalogo.prodotti.get_prodotto(row['prodotto_codice'])
                    if p:
                        if p.codice not in self.opzioni_escluse:
                            self.opzioni_escluse[p.codice] = {}
                        
                        codice_op = row['opzione_codice']
                        if codice_op in p.opzioni_totali():
                            self.opzioni_escluse[p.codice][codice_op] = True
