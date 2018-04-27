from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def room(request, room_id):
    context = {'room_id': room_id}
    return render(request, 'room.html', context)	


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")