import cherrypy
import os, os.path
from bs4 import BeautifulSoup
import requests
import random

from hydrator import Hydrator, Route

session = requests.Session()
session.headers.update({
    "Accept": "application/json",
    "User-Agent": "hydrator/0.1"
})

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
    def generate(paths):
        r = session.get("https://www.reddit.com/.json")
        data = r.json()["data"]["children"]

        index = random.randint(0, len(data)-1)

        print(data[index])

        return {
            "og:title": data[index]["data"]["title"],
            "og:image": data[index]["data"]["thumbnail"],
            "og:description": data[index]["data"]["subreddit"]
        }


class DefaultRoute(Route):
    def generate(paths):
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