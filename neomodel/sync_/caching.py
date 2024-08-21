from cachetools import LRUCache, cached

from neomodel.sync_.core import StructuredNode, db
from neomodel.sync_.match import NodeSet
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


class CachableNodeSet(NodeSet):
    @cached(db.cache)
    def get(self, lazy=False, **kwargs):
        return super(CachableNodeSet, self).get(lazy=lazy, **kwargs)

    @cached(db.cache)
    def get_or_none(self, **kwargs):
        return super(CachableNodeSet, self).get_or_none(**kwargs)

    @cached(db.cache)
    def first(self, **kwargs):
        return super(CachableNodeSet, self).first(**kwargs)

    @cached(db.cache)
    def first_or_none(self, **kwargs):
        return super(CachableNodeSet, self).first_or_none(**kwargs)


class CachableStructuredNode(StructuredNode):
    @classproperty
    def nodes(cls):
        """
        Returns a cachable NodeSet object representing all nodes of the classes label
        :return: CachableNodeSet
        :rtype: CachableNodeSet
        """

        return CachableNodeSet(cls)

    def save(self):
        # Invalidate cache when the node is updated
        db.cache.pop(self.element_id, None)
        super(CachableStructuredNode, self).save()

    def delete(self):
        # Invalidate cache when the node is deleted
        db.cache.pop(self.element_id, None)
        super(CachableStructuredNode, self).delete()
