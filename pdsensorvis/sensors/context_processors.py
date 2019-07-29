from django.conf import settings


def extra_context(request):
    return {'media_url': settings.MEDIA_URL}
