#!/usr/bin/env python
import os
import jinja2
import webapp2
from time import gmtime, strftime
from models import PosameznoSporocilo


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class VnosSporocilaHandler(BaseHandler):
    def get(self):
        params = {}
        return self.render_template("vnos_sporocila.html", params=params)

    def post(self):
        if len(self.request.get("ime")) == 0:
            ime = "Neznanec"
        else:
            ime = self.request.get("ime")

        if len(self.request.get("email")) == 0:
            email = "Neznan Email"
        else:
            email = self.request.get("email")

        sporocilo = self.request.get("sporocilo")

        posamezno_sporocilo = PosameznoSporocilo(ime=ime, email=email, sporocilo=sporocilo)
        posamezno_sporocilo.put()

        datum_cas = strftime("%a, %d %b %Y %H:%M:%S", gmtime())

        params = {"ime": ime, "email": email, "sporocilo": sporocilo, "cas": datum_cas}
        return self.render_template("vnos_sporocila.html", params=params)

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = PosameznoSporocilo.query(PosameznoSporocilo.izbrisan == False).fetch()
        params = {"seznam": seznam}
        return self.render_template("seznam_sporocil.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        posamezno_sporocilo = PosameznoSporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": posamezno_sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)

class UrediSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
            posamezno_sporocilo = PosameznoSporocilo.get_by_id(int(sporocilo_id))
            params = {"sporocilo": posamezno_sporocilo}
            return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        if len(self.request.get("ime")) == 0:
            ime = "Neznanec"
        else:
            ime = self.request.get("ime")

        if len(self.request.get("email")) == 0:
            email = "Neznan Email"
        else:
            email = self.request.get("email")

        sporocilo = self.request.get("sporocilo")

        posamezno_sporocilo = PosameznoSporocilo.get_by_id(int(sporocilo_id))
        posamezno_sporocilo.ime = ime
        posamezno_sporocilo.email = email
        posamezno_sporocilo.sporocilo = sporocilo
        posamezno_sporocilo.put()
        return self.redirect_to("seznam_sporocil")

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        posamezno_sporocilo = PosameznoSporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": posamezno_sporocilo}
        return self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        posamezno_sporocilo = PosameznoSporocilo.get_by_id(int(sporocilo_id))
        posamezno_sporocilo.izbrisan = True
        posamezno_sporocilo.put()
        return self.redirect_to("seznam_sporocil")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnos_sporocila', VnosSporocilaHandler),
    webapp2.Route('/seznam_sporocil', SeznamSporocilHandler, name="seznam_sporocil"),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/uredi', UrediSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/izbrisi', IzbrisiSporociloHandler),
], debug=True)
