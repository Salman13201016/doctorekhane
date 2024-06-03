import json
from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def ready(self):
        try:
            from app.models import OthersContent,SiteSettings,Districts,Divisions,Upazilas
            
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
            if Divisions.objects.count() == 0:
                with open('app/divisions.json', 'r', encoding='utf-8') as file:
                    divisions_data = json.load(file)['divisions']

                for division_data in divisions_data:
                    id = division_data['id']
                    division_name = division_data['name']
                    division_name_bn = division_data['bn_name']
                    division = Divisions.objects.create(id=id, division_name=division_name, division_name_bn=division_name_bn)

                with open('app/districts.json', 'r', encoding='utf-8') as file:
                    districts_data = json.load(file)['districts']

                for district_data in districts_data:
                    id = district_data['id']
                    division_id = district_data['division_id']
                    district_name = district_data['name']
                    district_name_bn = district_data['bn_name']
                    division = Divisions.objects.get(id=division_id)
                    district = Districts.objects.create(id=id,division=division, district_name=district_name, district_name_bn=district_name_bn)

                with open('app/upazilas.json', 'r', encoding='utf-8') as file:
                    upazilas_data = json.load(file)['upazilas']

                for upazila_data in upazilas_data:
                    id = upazila_data['id']
                    district_id  = upazila_data['district_id']
                    upazila_name = upazila_data['name']
                    upazila_name_bn = upazila_data['bn_name']
                    district = Districts.objects.get(id=district_id)
                    Upazilas.objects.create(id=id,district=district, upazila_name=upazila_name, upazila_name_bn=upazila_name_bn)
        except:
            pass
