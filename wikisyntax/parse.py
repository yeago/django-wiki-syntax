import regex
from django.core.cache import caches
from django.template.defaultfilters import slugify
from wikisyntax.exceptions import WikiException
from wikisyntax.helpers import get_wiki_objects
from wikisyntax.constants import WIKIBRACKETS
from wikisyntax.constants import LEFTBRACKET, RIGHTBRACKET


def make_cache_key(token, wiki_label=''):
    return "%s" % slugify(wiki_label + token)


class WikiParse(object):
    WIKIBRACKETS = WIKIBRACKETS

    def __init__(self, fail_silently=True, use_cache=True, **kwargs):
        self.fail_silently = fail_silently
        self.use_cache = use_cache
        self.cache_map = {}
        self.cache_updates = {}
        self.strikes = []

    def parse(self, string):
        string = string or u''
        brackets = map(make_cache_key, regex.findall(self.WIKIBRACKETS, string))
        if not brackets:
            return string
        if not self.fail_silently and len(string.split(LEFTBRACKET)) != len(string.split(RIGHTBRACKET)):
            raise WikiException("Left bracket count doesn't match right bracket count")
        if self.use_cache:
            self.cache_map = caches['wikisyntax'].get_many(brackets)
        content = regex.sub(u'%s(.*?)' % self.WIKIBRACKETS, self.callback, string)
        if self.cache_updates and self.use_cache:
            caches['wikisyntax'].set_many(dict((
                make_cache_key(k, v[3]), v[0]) for k, v in self.cache_updates.items()))
        return content

    def callback(self, match):
        token, trail = match.groups()
        if make_cache_key(token) in self.cache_map:
            val = self.cache_map[make_cache_key(token)]
            if isinstance(val, str):
                result = val
            else:
                result = str(val, errors='ignore')
            self.strikes.append({
                'from_cache': True,
                'match_obj': match,
                'token': token,
                'trail': trail,
                'result': result})
            return result
        try:
            """
            Of course none of this shit is useful if you're using the
            Caching wiki object
            """
            wiki_obj, token, trail, explicit, label = get_wiki(match)
            rendering = wiki_obj.render(token, trail=trail, explicit=explicit)
            if not isinstance(rendering, str):
                rendering = str(rendering, errors='ignore')
            self.cache_updates[slugify(token)] = (rendering, wiki_obj, match, label)
            self.strikes.append({
                'from_cache': False,
                'explicit': explicit,
                'match_obj': match,
                'wiki_obj': wiki_obj,
                'token': token,
                'trail': trail,
                'result': rendering})
            return rendering
        except WikiException:
            if not self.fail_silently:
                raise
            result = match.groups()[0]
            if not isinstance(result, str):
                result = str(result, errors='ignore')
            return result


def get_wiki(match):  # Excepts a regexp match
    token, trail = match.groups()  # we track the 'trail' because it may be a plural 's' or something useful

    """
    First we're checking if the text is attempting to find a specific type of object.
    [[user:Subsume]]
    [[card:Jack of Hearts]]
    """
    wikis = get_wiki_objects()
    if ':' in token:
        namespace, subtoken = token.split(':', 1)
        for wiki in wikis:
            if namespace and wiki.name and namespace.lower() == wiki.name.lower():
                content = wiki.render(subtoken.strip(), trail=trail, explicit=True)
                if content:
                    return wiki, subtoken.strip(), trail, True, wiki.name
                raise WikiException("Type %s didn't return anything for '%s'" % (namespace, subtoken))

    """
    Now we're going to try a generic match across all our wiki objects.
    [[Christopher Walken]]
    [[Beverly Hills: 90210]] <-- notice ':' was confused earlier as a wiki prefix name
    [[Cat]]s <-- will try to match 'Cat' but will pass the 'trail' on
    [[Cats]] <-- will try to match 'Cats' then 'Cat'
    """
    for wiki in wikis:
        content = wiki.render(token, trail=trail)
        if content and token:
            return wiki, token, trail, False, ''
    raise WikiException("No item found for '%s'" % (token))
