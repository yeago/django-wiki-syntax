import re

from .exceptions import WikiException
from .fix_unicode import fix_unicode
from .helpers import get_wiki_objects

class WikiParse(object):
    WIKIBRACKETS = '\[\[([^\]]+?)\]\]'
    def __init__(self, fail_silently=True):
        self.fail_silently = fail_silently

    def parse(self, string):
        string = string or ''
        string = fix_unicode(string)
        if not self.fail_silently:
            len_lbrack = len([i for i in string.split('[[')])
            len_rbrack = len([i for i in string.split(']]')])
            if len_lbrack != len_rbrack:
                raise WikiException("Left bracket count doesn't match right bracket count")
        content = re.sub('%s(.*?)' % self.WIKIBRACKETS, self.callback, string)
        return content

    def callback(self, match):
        try:
            return wikify(match)
        except WikiException:
            if not self.fail_silently:
                raise
            return match.groups()[0]

def wikify(match): # Excepts a regexp match
    token, trail = match.groups() # we track the 'trail' because it may be a plural 's' or something useful
    """
    First we're checking if the text is attempting to find a specific type of object.

    [[user:Subsume]]
    [[card:Jack of Hearts]]
    """
    wikis = get_wiki_objects()
    if ':' in token:
        name, subtoken = token.split(':',1)
        for wiki in wikis:
            if name == wiki.name:
                content = wiki.render(subtoken, trail=trail, explicit=True)
                if content:
                    return content
                raise WikiException("Type %s didn't return anything for '%s'" % (name, subtoken))

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
