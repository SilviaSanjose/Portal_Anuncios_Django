#para sacar la Ip del usuario
def obtener_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDER_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get('REMOTE_ADDR')