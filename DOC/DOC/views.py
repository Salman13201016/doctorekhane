from django.http import JsonResponse
from hospital.models import Hospital
from geopy.distance import geodesic
import requests

def index(request):
    return JsonResponse({'api': "daktar_ekhane"}, safe=False)

def nearby_hospitals(request):
    try:
        # Get user's location
        try:
            response = requests.get('https://ipinfo.io')
            data = response.json()
            location = data.get('loc')
            if location:
                user_latitude, user_longitude = map(float, location.split(','))
            else:
                return JsonResponse({'message': 'Location data not found.'}, status=404)
        except Exception as e:
            error_message = f"Error: Unable to detect your location. {str(e)}"
            # Log the error for debugging
            return JsonResponse({'message': error_message}, status=500)
        
        # Fetch hospitals from the database
        hospitals = Hospital.objects.all()
        hospital_data = []
        for hospital in hospitals:
            # Calculate distance between user and hospital
            hospital_distance = geodesic((user_latitude, user_longitude), (hospital.latitude, hospital.longitude)).kilometers
            hospital_data.append({
                'id': hospital.id,
                'hospital_image': request.build_absolute_uri(hospital.hospital_image.url) if hospital.hospital_image else None ,
                'name': hospital.name,
                'distance': hospital_distance
            })
        
        # Sort hospitals by distance
        hospital_data.sort(key=lambda x: x['distance'])
        
        return JsonResponse({'nearby_hospitals': hospital_data})
    
    except Exception as e:
        error_message = f"Error: Unable to fetch nearby hospitals. {str(e)}"
        # Log the error for debugging
        return JsonResponse({'message': error_message}, status=500)