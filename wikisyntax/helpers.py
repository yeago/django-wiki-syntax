import re

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
        module = __import__(".".join(modstring.split(".")[:-1]))
        for count, string in enumerate(modstring.split('.')):
            if count == 0:
                continue

            module = getattr(module,string)
        module.name = name
        wikis.append(module())

    token, trail = match.groups() # we track the 'trail' because it may be a plural 's' or something useful

    if ':' in token:
        """
        First we're checking if the text is attempting to find a specific type of object.

        Exmaples:

        [[user:Subsume]]

        [[card:Jack of Hearts]]

        """
        prefix, name = token.split(':',1)
        for wiki in wikis:
            if prefix == wiki.name:
                if wiki.attempt(name,explicit=True):
                    """
                    We still check attempt() because maybe
                    work is done in attempt that render relies on,
                    or maybe this is a false positive.
                    """
                    return wiki.render(name,trail=trail,explicit=True)
                else:
                    raise WikiException

    """
    Now we're going to try a generic match across all our wiki objects.

    Example:

    [[Christopher Walken]]

    [[Studio 54]]
    [[Beverly Hills: 90210]] <-- notice ':' was confused earlier as a wiki prefix name

    [[Cat]]s <-- will try to match 'Cat' but will include the plural 

    [[Cats]] <-- will try to match 'Cats' then 'Cat'

    """
    for wiki in wikis:
        if getattr(wiki,'prefix_only',None):
            continue

        if wiki.attempt(token):
            return wiki.render(token,trail=trail)

    """
    We tried everything we could and didn't find anything.
    """

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
