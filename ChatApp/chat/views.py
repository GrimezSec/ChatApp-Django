from django.shortcuts import render, redirect, reverse
from chat.models import Room, Message
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return HttpResponseRedirect(reverse('room', args=(room,)) + f'?username={username}')
    else:
        new_room = Room.objects.create(name=room)
        return HttpResponseRedirect(reverse('room', args=(room,)) + f'?username={username}')

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    room = Room.objects.get(id=room_id)  # room_id'yi Room nesnesine dönüştür
    new_message = Message.objects.create(value=message, user=username, room=room)
    new_message.save()
    return HttpResponse('Message sent successfully')




def getMessages(request, room):
    try:
        room_obj = Room.objects.get(name=room)
        messages = Message.objects.filter(room=room_obj)
        return JsonResponse({"messages":list(messages.values())})
    except ObjectDoesNotExist:
        return JsonResponse({"messages": []})  # Odanın bulunamaması durumunda boş bir JSON yanıtı döndür

