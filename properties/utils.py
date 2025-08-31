from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Fetch all properties, using Redis cache for 1 hour (3600 seconds)
    """
    # Check if properties exist in cache
    properties = cache.get("all_properties")

    if properties is None:
        # If not cached, fetch from DB
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        # Store queryset in Redis for 1 hour (3600 seconds)
        cache.set("all_properties", properties, timeout=3600)

    return properties
