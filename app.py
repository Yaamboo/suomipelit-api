from flask import abort, Flask, jsonify
import sqlite3
import re
from Suomipelit.jsonencoder import OmaEncoder
from Suomipelit.models import Peli, Peliarvostelu, Kappale, Kuva

app = Flask(__name__)
app.json_encoder = OmaEncoder

@app.route("/api/pelit")
def pelit():
    return jsonify(lataa_pelit())

def lataa_pelit():
    connection = sqlite3.connect("suomipelit.db")
    connection.row_factory = sqlite3.Row

    c = connection.cursor()
    pelit = []
    for pelirivi in c.execute("SELECT * FROM pelit order by id asc LIMIT 0,5"):
        peli = muodostaPeli(pelirivi, c)
        pelit.append(peli)

    # print(kappaleet)
    return pelit

@app.route("/api/pelit/<id>")
def peli(id):
    #id voi olla vain numeroita
    clean_id = int(id)
    peli = lataa_peli(clean_id)
    if peli is not None:
        return jsonify(peli)
    abort(404)

def lataa_peli(id):
    connection = sqlite3.connect("suomipelit.db")
    connection.row_factory = sqlite3.Row
    c = connection.cursor()

    c.execute("select * from pelit where id = ?", (id,))
    peli = c.fetchone()
    if peli is not None: 
        return muodostaPeli(peli, connection)
    return None

def muodostaPeli(pelirivi, connection):
    peli = Peli(pelirivi["id"])
    peli.nimi = pelirivi["nimi"]
    peli.tekija = pelirivi["tekija"]
    peli.url = pelirivi["url"]
    peli.kuvaus = pelirivi["kuvaus"]
    peli.vaatimukset = pelirivi["vaatimukset"]

    pelikuva = Kuva(pelirivi["id"])
    pelikuva.asemointi = None
    pelikuva.kuvateksti = None
    if pelirivi["kuva_iso"] != None and len(pelirivi["kuva_iso"]) > 0:
        pelikuva.tiedosto = pelirivi["kuva_iso"] 
    else: 
        pelikuva.tiedosto = pelirivi["kuva"]

    peli.kuva = pelikuva


    if pelirivi["uusittu"] == 1:
        arvostelu = Peliarvostelu()

        arvostelu.julkaistu = pelirivi["paivays"]
        arvostelu.kirjoittaja = pelirivi["user"]

        kappaleet = []

        for rivi in connection.cursor().execute("SELECT * FROM kappale where artikkeli_id = ? and kaytto='PELI' order by artikkeli_id asc, sivu asc, jarjestys", (pelirivi["id"],)):
            kappale = Kappale(rivi["id"], rivi["otsikko"], rivi["teksti"])
            kappale.artikkeliId = rivi["artikkeli_id"]
            kappale.sivu = rivi["sivu"]

            if len(rivi["kuva"]) > 0:
                kuva = Kuva(rivi["id"])
                if rivi["kuva_iso"] != None and len(rivi["kuva_iso"]) > 0:
                    kuva.tiedosto = rivi["kuva_iso"]
                else: 
                    kuva.tiedosto = rivi["kuva"]
                kuva.asemointi = rivi["asemointi"]
                kuva.kuvateksti = rivi["kuvateksti"]
            else:
                kuva = None

            kappale.kuva = kuva
            kappaleet.append(kappale)

        arvostelu.kappaleet = kappaleet

        peli.arvostelu = arvostelu
    else:
        peli.arvostelu = None
    return peli


