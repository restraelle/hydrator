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
        levels = self.split_path(path)
        route = "/{}".format(levels[0])

        route_class = Route()

        if route in self.routes.keys():
            route_class = self.routes[route]
        elif "default" in self.routes.keys():
            route_class = self.routes["default"]

        meta = route_class.generate(levels)

        for prop, value in meta.items():
            t = self.soup.new_tag("meta", property=prop, content=value)
            self.soup.head.append(t)
    
    def get_dom(self):
        return str(self.soup)



class Route():
    @staticmethod
    def generate(levels):
        # <!-- COMMON TAGS -->
        # <meta charset="utf-8">
        # <title>Untitled</title>
        # <!-- Search Engine -->
        # <meta name="image" content="https://site_image_test.png">
        # <!-- Schema.org for Google -->
        # <meta itemprop="name" content="Untitled">
        # <meta itemprop="image" content="https://site_image_test.png">
        # <!-- Open Graph general (Facebook, Pinterest & Google+) -->
        # <meta name="og:title" content="Untitled">
        # <meta name="og:image" content="https://preview_test.png">
        # <meta name="og:url" content="https://www.full30.com">
        # <meta name="og:site_name" content="Full30">
        # <meta name="og:video" content="https://www.full30.com/video.mp4">
        # <meta name="og:type" content="website">


        # <title>Untitled - hydrator (alpha)</title>
        # <meta name="title" content="Untitled - hydrator (alpha)">
        # <meta name="description" content="Replace this rinky dink default description. Like it's real stale and funky so as soon as you can send some real data, we can get this out of the way.">

        # <!-- Open Graph / Facebook -->
        # <meta property="og:type" content="website">
        # <meta property="og:url" content="https://metatags.io/">
        # <meta property="og:title" content="Untitled - hydrator (alpha)">
        # <meta property="og:description" content="Replace this rinky dink default description. Like it's real stale and funky so as soon as you can send some real data, we can get this out of the way.">
        # <meta property="og:image" content="https://metatags.io/assets/meta-tags-16a33a6a8531e519cc0936fbba0ad904e52d35f34a46c97a2c9f6f7dd7d336f2.png">

        # <!-- Twitter -->
        # <meta property="twitter:card" content="summary_large_image">
        # <meta property="twitter:url" content="https://metatags.io/">
        # <meta property="twitter:title" content="Untitled - hydrator (alpha)">
        # <meta property="twitter:description" content="Replace this rinky dink default description. Like it's real stale and funky so as soon as you can send some real data, we can get this out of the way.">
        # <meta property="twitter:image" content="https://metatags.io/assets/meta-tags-16a33a6a8531e519cc0936fbba0ad904e52d35f34a46c97a2c9f6f7dd7d336f2.png">

        return {
            "title": "Untitled - hydrator",
            "image": "https://cdn.discordapp.com/attachments/462433010218827777/766564154705444874/Genshin-Impact_2019_11-22-19_Top.jpg",

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