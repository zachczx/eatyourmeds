from django.utils.cache import patch_response_headers
from django.views.decorators.cache import cache_page, never_cache

class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)

class CacheControlMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        response = super(CacheControlMixin, self).dispatch(*args, **kwargs)
        patch_response_headers(response, self.get_cache_timeout())
        return response


class JitterCacheMixin(CacheControlMixin):
    cache_range = [40, 80]

    def get_cache_range(self):
        return self.cache_range

    def get_cache_timeout(self):
        return random.randint(*self.get_cache_range())