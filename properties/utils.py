from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Fetch all properties, using Redis cache for 1 hour (3600 seconds)
    """
    properties = cache.get("all_properties")

    if properties is None:
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        cache.set("all_properties", properties, timeout=3600)

    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    try:
        # Get Redis connection from django-redis
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        # Extract hits and misses
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        # Calculate hit ratio safely
        total_requests = hits + misses
        hit_ratio = round((hits / total_requests) * 100, 2) if total_requests > 0 else 0

        # Log metrics for debugging
        logger.info(f"Redis Cache Metrics → Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio}%")

        return {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0
        }
