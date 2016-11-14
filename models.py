from google.appengine.ext import ndb


class PosameznoSporocilo(ndb.Model):
    ime = ndb.StringProperty()
    email = ndb.StringProperty()
    sporocilo = ndb.StringProperty()
    izbrisan = ndb.BooleanProperty(default=False)
    datum = ndb.DateTimeProperty(auto_now_add=True)