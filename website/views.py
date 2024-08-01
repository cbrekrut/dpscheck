from django.shortcuts import render
import telebot
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
import json

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

from django.http import JsonResponse
from .models import Marker

def add_marker(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')
    Marker.objects.create(
            latitude=float(latitude),
            longitude=float(longitude),
            user=request.user
        )
    return JsonResponse({'status': 'success'})

def get_markers(request):
    active_markers = [marker for marker in Marker.objects.all() if marker.is_active()]
    Marker.objects.filter(id__in=[marker.id for marker in Marker.objects.all() if not marker.is_active()]).delete()
    data = {
        'markers': [
            {
                'lat': marker.latitude,
                'lon': marker.longitude,
                'id': marker.id,
                'created_at': marker.created_at,
                'username': marker.user.first_name  # Add username to the response
            }
            for marker in active_markers
        ],
        'active_markers_count': len(active_markers)
    }
    return JsonResponse(data, safe=False)

@require_POST
def extend_marker(request, id):
    try:
        marker = Marker.objects.get(pk=id)
        marker.created_at = timezone.now()
        marker.save()
        return JsonResponse({'status': 'success'})
    except Marker.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Marker not found'}, status=404)

@require_http_methods(["DELETE"])
def delete_marker(request, id):
    try:
        marker = Marker.objects.get(pk=id)
        marker.delete()
        return JsonResponse({'status': 'success'})
    except Marker.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Marker not found'}, status=404)

def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request, 'home.html')    
    
def login(request): 
    return render(request, 'login.html')

def telegram_auth(request):
    tg_user = request.GET.get('tg_user')
    if tg_user:
        tg_user_data = json.loads(tg_user)
        username = tg_user_data['username']
        first_name = tg_user_data['first_name']
        last_name = tg_user_data['last_name']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name)
            user.set_unusable_password()
            user.save()

        user = authenticate(username=username)
        if user:
            login(request, user)

        return redirect('home')
    return redirect('login')