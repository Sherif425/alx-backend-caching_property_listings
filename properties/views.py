from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache entire response for 15 minutes
def property_list(request):
    """Return a list of all properties"""
    properties = get_all_properties()
    return JsonResponse({
        "data": properties  
    }, safe=False)
