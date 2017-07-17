import pickle

from django.core.cache.backends.memcached import BaseMemcachedCache


class GoogleMemcacheCache(BaseMemcachedCache):
    "An implementation of a cache binding using app-engine memcache"
    def __init__(self, server, params):
        from google.appengine.api import memcache
        super(GoogleMemcacheCache, self).__init__(server, params,
                                             library=memcache,
                                             value_not_found_exception=ValueError)

    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = self._lib.Client(self._servers, pickleProtocol=pickle.HIGHEST_PROTOCOL)
        return self._client

