
class Peli(object):
    def __init__(self, id):
        self.id = id

class Peliarvostelu(object):
    def __init__(self):
        self

class Kappale(object):
    def __init__(self, id, otsikko, teksti):
        self.id = id
        self.otsikko = otsikko
        self.teksti = teksti
    
    def __repr__(self):
        return "Kappale {} {}".format(self.id, self.otsikko)

class Kuva(object):
    def __init__(self, id):
        self.id = id

