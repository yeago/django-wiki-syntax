from django.template.defaultfilters import slugify
from django.core.cache import cache

class CachingWikiMixin(object):
    content = None
    cache_timeout = 60 * 60 * 5
    def get_cache_key(self, token, explicit):
        return "%s-%s-%s" % (self.name, slugify(token), explicit)

    def attempt(self,token,explicit=False):
        self.content = self.cache_attempt(token, explicit=explicit)
        if self.content is None:
            attempt_inner = self.attempt_inner(toke, explicit=explicit)
            if attempt_inner:
                return True
            self.set_cache(token, explicit, False)
            return False
        return content == True

    def cache_attempt(self, token, explicit=False):
        """
        If this returns None, children can proceed.
        If True (the found content) or False, they won't.
        """
        return cache.get(self.get_cache_key(token, explicit))

    def set_cache(self, token, value, explicit=False):
        cache_key = self.get_cache_key(token, explicit=explicit)
        cache.set(cache_key, value, self.cache_timeout)

    def render(self, token, **kwargs):
        if self.content is not None:
            return self.content
        render_value = self.render_inner(token, **kwargs)
        self.set_cache(token, render_value, explicit=kwargs.get('explicit'))

class ModelWikiMixin(object):
    def attempt_inner(self, token, explicit=explicit):
        try:
            get_kwargs = self.get_kwargs(token, explicit=explicit)
            self._obj = self.get_query_set().get(**get_kwargs)
            return True
        except self.model.DoesNotExist:
            return False
        except self.model.MultipleObjectsReturned:
            return False

    def get_query_set(self):
        return self.model.all()

    def get_kwargs(self, token):
        raise NotImplementedError

class SlugWikiMixin(ModelWikiMixin):
    def get_kwargs(self, token):
        return {'slug': slugify(token)}
