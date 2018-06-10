from .models import EventModel
from .utils import get_client_ip

def register(tag, request):
    
    if not request:
        raise ValueError("A request object is required")
    
    if not tag:
        raise ValueError("A tag is needed")
    
    event = EventModel()
    event.tag = tag
    event.ip = get_client_ip(request)
    event.user = request.user if request.user.is_authenticated() else None

    event.save()

        