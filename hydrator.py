import os, os.path
from bs4 import BeautifulSoup

class Hydrator():
    index = ""
    routes = {}

    def __init__(self, raw_index, routes):
        self.index = str(raw_index)
        self.soup = BeautifulSoup(self.index, 'html.parser')

        for route in routes:
            self.routes[route[0]] = route[1]

    @staticmethod
    def split_path(path):
        l = path.split("/")
        l.pop(0)
        return l

    def hydrate_dom(self, path):
        paths = self.split_path(path)
        route = "/{}".format(paths[0])

        route_class = Route()

        if route in self.routes.keys():
            route_class = self.routes[route]
        elif "default" in self.routes.keys():
            route_class = self.routes["default"]

        meta = route_class.generate(paths)

        for prop, value in meta.items():
            t = self.soup.new_tag("meta", property=prop, content=value)
            self.soup.head.append(t)
    
    def get_dom(self):
        return str(self.soup)



class Route():
    @staticmethod
    def generate(paths):
        # <title>Untitled - hydrator (alpha)</title>
        # <meta itemprop="name" content="Untitled">
        # <meta itemprop="image" content="https://site_image_test.png">
        
        return {
            "title": "Untitled - hydrator",
            "image": "https://cdn.discordapp.com/attachments/462433010218827777/766564154705444874/Genshin-Impact_2019_11-22-19_Top.jpg",
            "description": "A simple & quenchy React DOM hydrator.",

            "og:title": "Untitled - hydrator",
            "og:description": "A simple & quenchy React DOM hydrator.",
            "og:site_name": "hydrator",
            "og:url": "https://hydrator.restraelle.com",
            "og:type": "website",
            "og:image": "https://cdn.discordapp.com/attachments/462433010218827777/766564154705444874/Genshin-Impact_2019_11-22-19_Top.jpg",

            "twitter:title": "Untitled - hydrator",
            "twitter:description": "A simple & quenchy React DOM hydrator.",
            "twitter:url": "https://hydrator.restraelle.com",
            "twitter:card": "summary_large_image",
            "twitter:image": "https://cdn.discordapp.com/attachments/462433010218827777/766564154705444874/Genshin-Impact_2019_11-22-19_Top.jpg"
        }