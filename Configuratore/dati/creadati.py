from modelli.motore import Motore
from modelli.corsa import Corsa
from modelli.opzione import Opzione
from modelli.velocita import Velocita
from modelli.descrizione import Descrizione
from modelli.cuscinetto import Cuscinetto
from modelli.prodotto import Prodotto
from modelli.mandrino import Mandrino
from modelli.motorizzazione import Motorizzazione
from modelli.trasmissione import Trasmissione
from modelli.accessorio import Accessorio

def crea_accessorio(codice, descrizione, consegna, prezzo, tipologia):
    a = Accessorio()
    a.codice = codice
    a.descrizione = descrizione
    a.consegna = consegna
    a.prezzo = prezzo
    a.tipologia = tipologia
    return a

def crea_corsa(codice, descrizione):
    c = Corsa()
    c.codice = codice
    c.descrizione = descrizione
    return c

def crea_cuscinetto(codice, descrizione):
    c = Cuscinetto()
    c.codice = codice
    c.descrizione = descrizione
    return c

def crea_descrizione(codice, descrizione):
    d = Descrizione()
    d.codice = codice
    d.descrizione_base = descrizione
    return d

def crea_mandrino(codice, descrizione):
    m = Mandrino()
    m.codice = codice
    m.descrizione = descrizione
    return m

def crea_motore(codice, grandezza, grandezza_descr, potenza, poli, freno = ""):
    m = Motore()
    m.codice = codice
    m.grandezza = grandezza
    m.grandezza_descr = grandezza_descr
    m.potenza = potenza
    m.poli = poli
    m.freno = freno
    return m

def crea_opzione(codice, voce_ck, descrizione, comportamento, destinazione):
    o = Opzione()
    o.codice = codice
    o.voce_ck = voce_ck
    o.descrizione = descrizione
    o.comportamento = comportamento
    o.destinazione = destinazione
    return o

def crea_trasmissione(codice, descrizione):
     t = Trasmissione()
     t.codice = codice
     t.descrizione = descrizione
     return t

def crea_velocita(codice, descrizione):
     v = Velocita()
     v.codice = codice
     v.descrizione = descrizione
     return v

def crea_prodotto(catalogo, macrocat, codice, famiglia, corsa = "", mandrino = "", motorizzazione = "",cuscinetto = "",\
                  capacitaforatura = "", capacitamaschiatura = "", spinta = "", caricoassiale = "", concentricita = "", \
                  vite = "", cilpn = "", cilidr = "", maxtagliamot = "", opzioneextra = ""):
    
    p = Prodotto()

    p.tipo = macrocat
    p.codice = codice
    p.famiglia = catalogo.famiglie.get_famiglia(famiglia)

    if motorizzazione:
        for trittico in motorizzazione.split(";"):
            valoresingolo = trittico.split("|")
            terna = Motorizzazione()
            terna.velocita = catalogo.velocita.get_velocita(valoresingolo[0])
            terna.motore = catalogo.motori.get_motore(valoresingolo[1])
            terna.trasmissione = catalogo.trasmissioni.get_trasmissione(valoresingolo[2])
            p.aggiungi_motorizzazione(terna)
    
    if corsa:
        for x in corsa.split(";"):
            p.aggiungi_corsa(catalogo.corse.get_corsa(x))

    if mandrino:
        for x in mandrino.split(";"):
            p.aggiungi_mandrino(catalogo.mandrini.get_mandrino(x))

    if cuscinetto:
        for x in cuscinetto.split(";"):
            p.aggiungi_cuscinetto(catalogo.cuscinetti.get_cuscinetto(x))

    if opzioneextra:
        for x in opzioneextra.split(";"):
            p.aggiungi_opzione_extra(catalogo.opzioni.get_opzione(x))
    
    
    if capacitaforatura:
        p.capacita_foratura = capacitaforatura
    if capacitamaschiatura:
        p.capacita_maschiatura = capacitamaschiatura
    if spinta:
        p.spinta = spinta
    if caricoassiale:
        p.carico_assiale = caricoassiale
    if concentricita:
        p.concentricita = concentricita
    if vite:
        p.vite = vite
    if cilpn:
        p.cilindro_pneumatico = cilpn
    if cilidr:
        p.cilindro_idraulico = cilidr
    if maxtagliamot:
        p.max_taglia_motore = maxtagliamot
   
    return p