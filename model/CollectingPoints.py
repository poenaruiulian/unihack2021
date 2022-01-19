import json


class CollectingPoints:

    def __init__(self, _id, id, tip_colectare, adresa, companie, website, latitudine, longitudine):
        self.longitudine = longitudine
        self.latitudine = latitudine
        self.website = website
        self.companie = companie
        self.adresa = adresa
        self.tip_colectare = tip_colectare
        self.id = id
        self._id = _id

    def __repr__(self):
        return f'<CollectingPoints {self.id}>'

