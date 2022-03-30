# import json
#
# import memcache
#
# from web_aggregator import mongo, app
#
#
# def json_serializer(key, value):
#     if type(value) == str:
#         return value, 1
#     return json.dumps(value), 2
#
#
# def json_deserializer(key, value, flags):
#     if flags == 1:
#         return value
#     if flags == 2:
#         return json.loads(value)
#     raise Exception("Unknown serialization format")
#
#
# memcached_client = memcache.Client(['memcached:11211'], debug=0)
# print('memcached connected')
#
# memcached_client.set('JWT_BLACKLIST', set())
#
#
# def load_blacklisted_tokens():
#     blacklisted_tokens = mongo.db.blacklisted_tokens.find({}, {'_id': 0})
#     blacklisted_tokens = list(blacklisted_tokens)
#     blacklisted_tokens = set([doc['jti'] for doc in blacklisted_tokens])
#     return blacklisted_tokens
#
#
# blacklisted_tokens = load_blacklisted_tokens()
# app.logger.debug(blacklisted_tokens)
#
#
# def get_global_vars():
#     blacklisted_tokens = load_blacklisted_tokens()
#     return blacklisted_tokens
#
#
# def set_memcache(blacklisted_tokens):
#     print(memcached_client)
#     memcached_client.set('JWT_BLACKLIST', blacklisted_tokens)
#     memcached_client.set('STATUS', 'SET')
#
#
# def replace_memcache(blacklisted_tokens):
#     print(memcached_client)
#     memcached_client.replace('JWT_BLACKLIST', blacklisted_tokens)
#     memcached_client.replace('STATUS', 'SET')
#
#
# def set_blacklisted_tokens(tokens):
#     memcached_client.replace('JWT_BLACKLIST', tokens)
#
#
# def get_blacklisted_tokens():
#     blacklisted_tokens = memcached_client.get('JWT_BLACKLIST')
#     if blacklisted_tokens:
#         return blacklisted_tokens
#     else:
#         blacklisted_tokens = load_blacklisted_tokens()
#         memcached_client.replace('JWT_BLACKLIST', blacklisted_tokens)
#         return blacklisted_tokens
