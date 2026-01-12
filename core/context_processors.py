from .models import SiteSettings

def site_settings(request):
    """
    Context processor to make SiteSettings available in all templates
    """
    try:
        settings = SiteSettings.objects.first()
    except Exception:
        settings = None
        
    return {'site_settings': settings}
