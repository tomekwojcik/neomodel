# from test._async_compat import mark_async_test
# from neomodel import StringProperty
# from neomodel.async_.core import adb
# from neomodel.async_.caching import AsyncCachableStructuredNode


# class CacheNode(AsyncCachableStructuredNode):
#     someProp = StringProperty()


# @mark_async_test
# async def test_cache_behavior():
#     # Ensure cache is clear before testing
#     adb.cache.clear()

#     # Insert a test node to ensure it's in the database
#     node = await CacheNode(someProp="something").save()

#     # Fetch node, should come from the database
#     fetched_node = await CacheNode.nodes.get(someProp="something")
#     assert not adb.cache.hit, "Expected result to come from the database"

#     # Fetch the same node, should come from the cache
#     fetched_node = await CacheNode.nodes.get(someProp="something")
#     assert adb.cache.hit, "Expected result to come from the cache"

#     # Update the node
#     fetched_node.someProp = "something else"
#     await fetched_node.save()
#     # Check property has been updated and cache is invalidated
#     fetched_node = await CacheNode.nodes.get(someProp="something else")
#     assert (
#         fetched_node.someProp == "something else"
#     ), "Expected node to be updated in database"
#     assert not adb.cache.hit, "Expected cache to be invalidated"
#     non_fetched_node = await CacheNode.nodes.get(someProp="something")
#     assert non_fetched_node is None, "Expected node to be deleted from cache"

#     # Clean up
#     await fetched_node.delete()
#     fetched_node = await CacheNode.nodes.get(someProp="something")
#     assert fetched_node is None, "Expected node to be deleted from database and cache"
