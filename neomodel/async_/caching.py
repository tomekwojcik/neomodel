from cachetools import LRUCache, cached

from neomodel.async_.core import AsyncStructuredNode, adb
from neomodel.async_.match import AsyncNodeSet
from neomodel.util import classproperty


class TrackableLRUCache(LRUCache):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hit = False

    def __getitem__(self, key):
        try:
            value = super().__getitem__(key)
            self.hit = True
            return value
        except KeyError:
            self.hit = False
            raise

    def __contains__(self, key):
        contained = super().__contains__(key)
        self.hit = contained
        return contained


class AsyncCachableNodeSet(AsyncNodeSet):
    @cached(adb.cache)
    async def get(self, lazy=False, **kwargs):
        return await super(AsyncCachableNodeSet, self).get(lazy=lazy, **kwargs)

    @cached(adb.cache)
    async def get_or_none(self, **kwargs):
        return await super(AsyncCachableNodeSet, self).get_or_none(**kwargs)

    @cached(adb.cache)
    async def first(self, **kwargs):
        return await super(AsyncCachableNodeSet, self).first(**kwargs)

    @cached(adb.cache)
    async def first_or_none(self, **kwargs):
        return await super(AsyncCachableNodeSet, self).first_or_none(**kwargs)


class AsyncCachableStructuredNode(AsyncStructuredNode):
    @classproperty
    def nodes(cls):
        """
        Returns a cachable NodeSet object representing all nodes of the classes label
        :return: AsyncCachableNodeSet
        :rtype: AsyncCachableNodeSet
        """

        return AsyncCachableNodeSet(cls)

    async def save(self):
        # Invalidate cache when the node is updated
        adb.cache.pop(self.element_id, None)
        await super(AsyncCachableStructuredNode, self).save()

    async def delete(self):
        # Invalidate cache when the node is deleted
        adb.cache.pop(self.element_id, None)
        await super(AsyncCachableStructuredNode, self).delete()
