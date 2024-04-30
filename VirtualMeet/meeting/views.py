from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import RoomMember
import random
import time
import json
# Create your views here.

def getToken(request):
    appId = '2ffbd1e241654475aff11decdf928552'
    appCertificate = 'e2a70b4406d044dfb7f42bc74c0e8b01'
    # channelName = 'virtualmeet'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({
        'token': token,
        'uid': uid
    }, safe=False)

def lobby(request):
    return render(request, 'lobby.html')


def room(request):
    return render(request, 'chatroom.html')

@csrf_exempt
def createUser(request):
    data = json.loads(request.body)


    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room']
    )
    return JsonResponse({ 'name' : data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)

@csrf_exempt
def scheduleMeeting(request):
    data = json.loads(request.body)
    print(data['date'])
    print(data['subject'])
    print(request.user)

    return JsonResponse({ 'status': 'success'})