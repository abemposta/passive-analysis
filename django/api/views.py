from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
import json
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import api.code.helper as helper
from django.http import HttpResponse


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload(request):
    if request.method == 'POST':
        try:
            packetlist = request.data
            helper.upload_mongo(packetlist)
            return HttpResponse(status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error processing upload: ", e)
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
