import cherrypy
import os, os.path
from bs4 import BeautifulSoup

from hydrator import Hydrator, Route

class Root(object):
    @cherrypy.expose
    def default(self, *args, **kwargs):
        # loading index.html into memory
        raw_index = ""
        with open("./www/index.html") as t:
            raw_index = str(t.read())

        # initializing hydrator object
        h = Hydrator(raw_index, [
            ["/", Route],
            ["/testing", TestingRoute],
            ["default", DefaultRoute]
        ])

        # gets path from request object
        path = cherrypy.request.path_info

        # generates meta and puts into DOM
        h.hydrate_dom(path)

        # gets new DOM with meta
        dom = h.get_dom()

        return dom

class TestingRoute(Route):
    def generate(levels):
        return {
            "og:title": "eggs"
        }


class DefaultRoute(Route):
    def generate(levels):
        return {
            "og:title": "throwback to default"
        }

conf = {
    '/': {
        'tools.staticdir.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.staticdir.dir': './www'
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './www/static'
    }
}

if __name__ == "__main__":
    cherrypy.quickstart(Root(), '/', conf)


wsgi_app = cherrypy.Application(Root(), '/', config=conf)