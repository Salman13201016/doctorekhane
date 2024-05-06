from app.models import SiteSettings
data = {
    'logo': None,
    'banner': None,
}
smtp_config = SiteSettings.objects.create(**data)