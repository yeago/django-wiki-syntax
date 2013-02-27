import re

from django.core.cache import cache
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from .exceptions import WikiException
from .fix_unicode import fix_unicode
from .helpers import get_wiki_objects


def make_cache_key(token):
    return "wiki::%s" % slugify(token)


class WikiParse(object):
    WIKIBRACKETS = '\[\[([^\]]+?)\]\]'

    def __init__(self, fail_silently=True):
        self.fail_silently = fail_silently
        self.cache_updates = {}

    def parse(self, string):
        string = string or ''
        string = fix_unicode(string)
        if not self.fail_silently:
            len_lbrack = len([i for i in string.split('[[')])
            len_rbrack = len([i for i in string.split(']]')])
            if len_lbrack != len_rbrack:
                raise WikiException("Left bracket count doesn't match right bracket count")
        brackets = map(make_cache_key, re.findall(self.WIKIBRACKETS, string))
        self.cache_map = cache.get_many(brackets)
        content = re.sub('%s(.*?)' % self.WIKIBRACKETS, self.callback, string)
        if self.cache_updates:
            cache.set_many(dict((
                make_cache_key(k), v) for k, v in self.cache_updates.items()), 60 * 5)
        return content

    def callback(self, match):
        token, train = match.groups()
        if make_cache_key(token) in self.cache_map:
            return self.cache_map[make_cache_key(token)]
        try:
            """
            Of course none of this shit is useful if you're using the
            Caching wiki object
            """
            wiki_obj, token, trail, explicit = get_wiki(match)
            rendering = wiki_obj.render(token, trail=trail, explicit=explicit)
            token_key = '%s%s' % (token, trail or '')
            self.cache_updates[slugify(token)] = rendering
            return rendering

        except WikiException:
            if not self.fail_silently:
                raise
            return match.groups()[0]


def get_wiki(match):  # Excepts a regexp match
    token, trail = match.groups()  # we track the 'trail' because it may be a plural 's' or something useful
    """
    First we're checking if the text is attempting to find a specific type of object.

    [[user:Subsume]]
    [[card:Jack of Hearts]]
    """
    wikis = get_wiki_objects()
    if ':' in token:
        name, subtoken = token.split(':', 1)
        for wiki in wikis:
            if name == wiki.name:
                content = wiki.render(subtoken, trail=trail, explicit=True)
                if content:
                    return wiki, subtoken, trail, True
                raise WikiException("Type %s didn't return anything for '%s'" %
                                                            (name, subtoken))

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
            return wiki, token, trail, False
    raise WikiException("No item found for '%s'" % (token))
