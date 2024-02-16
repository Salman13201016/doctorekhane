from django.http import JsonResponse

def index(request):
    return JsonResponse({'api': "daktar_ekhane"}, safe=False)