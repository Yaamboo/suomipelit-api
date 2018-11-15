# pylint: disable=E0202

from flask.json import JSONEncoder
from Suomipelit.models import Peli, Peliarvostelu, Kappale, Kuva

class OmaEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Peli):
            return {
                'id': obj.id,
                'nimi': obj.nimi,
                'tekija': obj.tekija,
                'url': obj.url,
                'kuvaus': obj.kuvaus,
                'arvostelu': obj.arvostelu,
                'kuva': obj.kuva,
                'vaatimukset': obj.vaatimukset,
            }
        if isinstance(obj, Peliarvostelu):
            return {
                'kirjoittaja': obj.kirjoittaja,
                'julkaistu': obj.julkaistu,
                'kappaleet': obj.kappaleet,
            }
        if isinstance(obj, Kappale):
            return {
                'id': obj.id,
                'artikkeli': obj.artikkeliId,
                'sivu': obj.sivu,
                'otsikko': obj.otsikko,
                'teksti': obj.teksti,
                'kuva': obj.kuva
            }
        if isinstance(obj, Kuva):
            return {
                'id': obj.id,
                'tiedosto': obj.tiedosto,
                'asemointi': obj.asemointi,
                'kuvateksti': obj.kuvateksti
            }
        return super(OmaEncoder, self).default(obj)
