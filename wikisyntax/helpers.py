import importlib

from django.conf import settings

def get_wiki_objects(prefix=None):
    wikis = [] # Here we store our wiki model info
    for name, modstring in settings.WIKISYNTAX:
        modstring = modstring.split('.')
        klass = modstring.pop()
        package = ".".join(modstring)
        module = importlib.import_module(package)
        wiki = getattr(module, klass)()
        wiki.name = name
        wikis.append(wiki)
    return wikis

