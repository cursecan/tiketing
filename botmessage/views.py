from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import (
    Message
)


def tbotMessage(request, parse):
    message_obj = get_object_or_404(Message, parse_url=parse)
    return JsonResponse({'title': message_obj.title, 'body': message_obj.body})