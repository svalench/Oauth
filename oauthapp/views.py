
import datetime
import time

import jwt
import pytz
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Oauth import settings
from oauthapp.models import Client, ClientsCodes
from oauthapp.utils import generate_jwt_token


def auth(request):
    client_id = request.GET.get('client_id')
    redirect_url = request.GET.get('redirect_uri', None)

    if None in [client_id, redirect_url]:
        return JsonResponse({
            "error": "Не верные параметры запроса"
        }, status=400)

    if not Client().client_exist(client_id):
        return JsonResponse({
            "error": "Клиент не найден"
        }, status=400)
    context = {
        "client_id": client_id,
        "redirect_url": redirect_url,
    }
    return render(request, 'grant_access.html',
                  context=context)

@csrf_exempt
def tokenauth(request):
    code_post = request.POST.get('code')
    cl_code = ClientsCodes.objects.filter(token=code_post).first()
    decode_code = jwt.decode(code_post, settings.SECRET_KEY, algorithms=[settings.TOKEN_ENCODE_ALGORITM])
    userid = cl_code.user.id
    utc = pytz.UTC
    if not cl_code or cl_code.date_add > (datetime.datetime.now() - datetime.timedelta(minutes=10)).replace(tzinfo=utc):
        return JsonResponse({
            "error": "Code устарел"
        }, status=400)
    context = {
        "access_token": generate_jwt_token(cl_code.user),
        "token_type": "bearer",
        "refresh_token": jwt.encode({"id": userid, 'client': cl_code.id}, settings.SECRET_KEY, algorithm=settings.TOKEN_ENCODE_ALGORITM),
        "expires_in": settings.TOKEN_TIME_LIFE,
        "created_at": time.time()
    }
    return JsonResponse(context)

@csrf_exempt
def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    client_id = request.POST.get('client_id')
    redirect_url = request.POST.get('redirect_url')

    if None in [username, password, client_id, redirect_url]:
        return JsonResponse({
            "error": "Не верный запрос"
        }, status=400)

    if not Client().client_exist(client_id):
        return JsonResponse({
            "error": "Такого клиента не существует"
        }, status=400)
    client = Client.objects.get(client_id=client_id)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        return JsonResponse({
            'error': 'пользователя не существует'
        }, status=401)

    context = {}
    code_token = generate_jwt_token(user)
    response = HttpResponse(context, status=302)
    response['Location'] = f'{redirect_url}?code={code_token}'
    cl_code = ClientsCodes(client=client, user=user, token=code_token)
    cl_code.save()
    return response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my(request):
    if request.user.is_anonymous:
        return JsonResponse({
            'error': 'Вы не авторизованы'
        }, status=401)
    context = {
        "username": request.user.username
    }
    return Response(context, status=211)
