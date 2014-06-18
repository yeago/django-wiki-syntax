from django.core.cache import cache
from django.template.defaultfilters import slugify


class CachingWikiMixin(object):
    cache_timeout = 60 * 60 * 5

    def get_cache_key(self, token, explicit=False):
        return "%s-%s-%s" % (self.name, slugify(token), explicit)

    def render(self, token, explicit=False, trail=None):
        cache_key = self.get_cache_key(token, explicit)
        content = None
        if cache_key and len(cache_key) < 250:
            content = cache.get(cache_key) or None

        if content is None:
            content = super(CachingWikiMixin, self).render(token, explicit=explicit, trail=trail)
            if content:
                self.set_cache(token, content, explicit=explicit, trail=trail)
        return content

    def set_cache(self, token, value, explicit=False, **kwargs):
        cache_key = self.get_cache_key(token, explicit=explicit)
        cache.set(cache_key, value, self.cache_timeout)


class ModelWikiMixin(object):
    def render(self, token, explicit=False, trail=None):
        try:
            get_kwargs = self.get_kwargs(token, explicit=explicit)
            instance = self.get_query_set().get(**get_kwargs)
            self.instance = instance
            return self.render_model(token, instance, explicit=explicit, trail=trail)
        except self.model.DoesNotExist:
            return False
        except self.model.MultipleObjectsReturned:
            return False

    def get_query_set(self):
        return self.model.objects.all()

    def get_kwargs(self, token, explicit=False):
        raise NotImplementedError


class SlugWikiMixin(ModelWikiMixin):
    def get_kwargs(self, token, **kwargs):
        return {'slug': slugify(token)}
