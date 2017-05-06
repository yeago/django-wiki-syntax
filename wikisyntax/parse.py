import regex
from django.db import transaction

from django.template.defaultfilters import slugify
from .exceptions import WikiException
from .fix_unicode import fix_unicode
from .helpers import get_wiki_objects
from .constants import WIKIBRACKETS
from .utils import balanced_brackets
from wikisyntax.models import Blob


def make_cache_key(token, wiki_label=''):
    return "wiki::%s" % slugify(wiki_label + token)


def update_or_not(use_cache, token, content):
    try:
        assert(use_cache)
        assert(content)
        assert(token)
        assert(len(token) <= 35)
        assert(content.lower() != token.lower())
        Blob.objects.update_or_create(
            defaults={'blob': unicode(content)},
            string=unicode(token.lower()))
    except AssertionError:
        pass


class WikiParse(object):
    WIKIBRACKETS = WIKIBRACKETS
    model_backed = True

    def __init__(self, fail_silently=True, use_cache=True, **kwargs):
        self.model_backed = kwargs.pop('model_backed', self.model_backed)
        self.fail_silently = fail_silently
        self.use_cache = use_cache
        self.strikes = []

    def parse(self, string):
        string = string or u''
        string = fix_unicode(string)

        if not self.fail_silently and not balanced_brackets(string):
            raise WikiException("Left bracket count doesn't match right bracket count")

        brackets = map(make_cache_key, regex.findall(self.WIKIBRACKETS, string))
        if not brackets:
            return string

        with transaction.atomic():
            content = regex.sub(u'%s(.*?)' % self.WIKIBRACKETS, self.wrap_callback, string)
        return content

    def wrap_callback(self, match):  # sorry
        token, trail = match.groups()
        if self.use_cache and token and len(token) <= 35:
            try:
                return Blob.objects.access(token).blob
            except Blob.DoesNotExist:
                pass
        content = self.callback(match)
        update_or_not(self.use_cache, token, content)
        return content

    def callback(self, match):
        token, trail = match.groups()
        try:
            """
            Of course none of this shit is useful if you're using the
            Caching wiki object
            """
            wiki_obj, token, trail, explicit, label = get_wiki(match)
            rendering = wiki_obj.render(token, trail=trail, explicit=explicit)
            if not isinstance(rendering, unicode):
                rendering = unicode(rendering, errors='ignore')
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
            if not isinstance(result, unicode):
                result = unicode(result, errors='ignore')
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
            if namespace == wiki.name:
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
            update_or_not(True, token, content)
            return wiki, token, trail, False, ''
    raise WikiException("No item found for '%s'" % (token))
