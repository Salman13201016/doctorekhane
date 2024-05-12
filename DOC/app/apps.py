from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        try:
            from app.models import OthersContent,SiteSettings
            
            if OthersContent.objects.count() == 0:
                OthersContent.objects.create(
                    about_us_content="Default about us content",
                    about_us_content_bn="ডিফল্ট আমাদের সম্পর্কে বিষয়ক বিষয়",
                    termsncondition_content="Default terms and conditions content",
                    termsncondition_content_bn="ডিফল্ট শর্তাবলী এবং শর্তগুলির বিষয়ক বিষয়",
                    privacy_policy_content="Default privacy policy content",
                    privacy_policy_content_bn="ডিফল্ট গোপনীয়তা নীতি বিষয়ক বিষয়"
                )

            if SiteSettings.objects.count() == 0:
                SiteSettings.objects.create(
                )
        except:
            pass
