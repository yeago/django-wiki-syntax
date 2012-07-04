import re
import importlib

from django.contrib.markup.templatetags.markup import markdown
from django.conf import settings
from django.db.models.loading import get_model
from django.utils.safestring import mark_safe
from wikisyntax import fix_unicode

def wikisafe_markdown(value):
    LSAFETY = 'LBRACK666' # Some unlikely nonsense
    RSAFETY = 'RBRACK666' # Some unlikely nonsense
    value = value.replace('[[', LSAFETY).replace(']]', RSAFETY)
    value = markdown(value)
    value = value.replace(LSAFETY,'[[').replace(RSAFETY,']]')
    return mark_safe(value)

class WikiException(Exception): # Raised when a particular string is not found in any of the models.
    pass

def wikify(match): # Excepts a regexp match
    wikis = [] # Here we store our wiki model info
    for name, modstring in settings.WIKISYNTAX:
        modstring = modstring.split('.')
        klass = modstring.pop()
        package = ".".join(modstring)
        module = importlib.import_module(package)
        wiki = getattr(module, klass)()
        wiki.name = name
        wikis.append(wiki)

    token, trail = match.groups() # we track the 'trail' because it may be a plural 's' or something useful
    """
    First we're checking if the text is attempting to find a specific type of object.

    [[user:Subsume]]
    [[card:Jack of Hearts]]
    """
    if ':' in token:
        name, token = token.split(':',1)
        for wiki in wikis:
            if prefix == wiki.name:
                content = wiki.render(name, trail=trail, explicit=True)
                if content:
                    return content
                raise WikiException

    """
    Now we're going to try a generic match across all our wiki objects.

    [[Christopher Walken]]
    [[Beverly Hills: 90210]] <-- notice ':' was confused earlier as a wiki prefix name
    [[Cat]]s <-- will try to match 'Cat' but will pass the 'trail' on 
    [[Cats]] <-- will try to match 'Cats' then 'Cat'

    """
    for wiki in wikis:
        content = wiki.render(token, trail=trail)
        if content:
            return content
    raise WikiException("No item found for '%s'"% (token))

class wikify_string(object):
    def __call__(self, string, fail_silently=True):
        self.fail_silently = fail_silently
        WIKIBRACKETS = '\[\[([^\]]+?)\]\]'
        if not string:
            return ''

        string = fix_unicode.fix_unicode(string)
        content = re.sub('%s(.*?)' % WIKIBRACKETS,self.markup_to_links,string)
        return content

    def __new__(cls, string, **kwargs):
        obj = super(wikify_string, cls).__new__(cls)
        return obj(string, **kwargs)

    def markup_to_links(self,match):
        string = match.groups()[0].lower().replace(' ','-')
        try:
            return wikify(match)
        except WikiException:
            if not self.fail_silently:
                raise
            return string
