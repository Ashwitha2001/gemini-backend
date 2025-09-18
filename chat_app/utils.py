import json
from core.redis_client import r

CACHE_TTL = 600  # 10 minutes

def cache_chatrooms(user_id, chatrooms):
    r.set(f"chatrooms:{user_id}", json.dumps(chatrooms), ex=CACHE_TTL)

def get_cached_chatrooms(user_id):
    cached = r.get(f"chatrooms:{user_id}")
    if cached:
        return json.loads(cached)
    return None