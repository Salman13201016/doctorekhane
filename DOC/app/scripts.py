import json
from app.models import Divisions, Districts, Upazilas , Unions
with open('app/divisions.json', 'r', encoding='utf-8') as file:
    divisions_data = json.load(file)['divisions']

for division_data in divisions_data:
    id = division_data['id']
    division_name = division_data['name']
    division = Divisions.objects.create(id=id, division_name=division_name)

with open('app/districts.json', 'r', encoding='utf-8') as file:
    districts_data = json.load(file)['districts']

for district_data in districts_data:
    id = district_data['id']
    division_id = district_data['division_id']
    district_name = district_data['name']
    division = Divisions.objects.get(id=division_id)
    district = Districts.objects.create(id=id,division=division, district_name=district_name)

with open('app/upazilas.json', 'r', encoding='utf-8') as file:
    upazilas_data = json.load(file)['upazilas']

for upazila_data in upazilas_data:
    id = upazila_data['id']
    district_id  = upazila_data['district_id']
    upazila_name = upazila_data['name']
    district = Districts.objects.get(id=district_id)
    Upazilas.objects.create(id=id,district=district, upazila_name=upazila_name)

with open('app/unions.json', 'r', encoding='utf-8') as file:
    unions_data = json.load(file)['Unions']

for union_data in unions_data:
    id = union_data['id']
    upazilla_id=union_data['upazilla_id']
    upazila=Upazilas.objects.get(id=upazilla_id)
    union_name = union_data['name']
    Unions.objects.create(id=id,upazila=upazila, union_name=union_name)