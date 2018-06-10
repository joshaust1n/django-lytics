from .models import EventModel
from .utils import get_client_ip

def register(tag, request):
    
    event = EventModel()
    event.tag = tag
    event.ip = get_client_ip(request)
    event.user = request.user if request.user.is_authenticated() else None

    event.save()

        