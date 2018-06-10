def get_client_ip(request):
    '''
    https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip