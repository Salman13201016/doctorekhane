import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from DOC.settings import DEFAULT_FROM_EMAIL
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def contact_view(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
        
            subject = 'Inquiries from ' + data['name']
            message = f'Name: {data["name"]}\nEmail: {data["email"]}\nPhone: {data["phone"]}\nMessage: {data["message"]}'
            from_email = DEFAULT_FROM_EMAIL
            to_email = DEFAULT_FROM_EMAIL
            send_mail(subject, message, from_email, [to_email], fail_silently=True)

            return JsonResponse({"message":"send mail successfully"},status=200) 
    except:
            return JsonResponse({"message":"there is something wrong"},status=500) 


