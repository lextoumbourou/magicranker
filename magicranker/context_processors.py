def google_analytics(request):
    from django.conf import settings
    return {'GA_TRACKING_ID': settings.GA_TRACKING_ID}
