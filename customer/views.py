from django.shortcuts import render

# Create your views here.

import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import Application, BankApplication, Bank
from .serializers import ApplicationSerializer
# from .forms import CustomerApplicationForm
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from core import settings
from django.core import serializers
from .utils import call_bank_apis, send_to_queue

BANK_URLS = settings.BANK_URLS


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Application.objects.all()
    # querset = Application.objects.prefetch_related("")
    serializer_class = ApplicationSerializer
    def list(self, request, *args, **kwargs):
        print("llllll")
        serializer = self.serializer_class(self.get_queryset(), many=True)
        response = {
            "code": 200,
            "message": "Success",
            "data":
                serializer.data
        }
        return Response(response)

    def create(self, request, *args, **kwargs):
        payload = request.data
        print("-----")
        print(payload)
        serializer = ApplicationSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        try:
            if serializer.is_valid():
                # Call bank API
                for name, url in BANK_URLS.items():
                    res = call_bank_apis(url, obj)

                    if res:
                        bank_application = BankApplication()
                        bank_application.application = obj
                        bank_application.bank = Bank.objects.get(name=name)
                        bank_application.status = res.get('status')
                        bank_application.save()
                        send_to_queue(obj.uuid, bank_application.bank.name)
                response = {
                    "code": 200,
                    "message": "Success",
                    "data":
                        serializer.data
                }

            else:
                response = {"code": 200,
                            "message": "Customer application creation failed",
                            "data": {}}
            return Response(
                response,
                # status=status.HTTP_201_CREATED,
                # headers=headers
            )
        except Exception as e:
            print(e)

    def partial_update(self, request, *args, **kwargs):
        print("in pup....")
        instance = self.get_object()
        print("==========")
        print(instance.first_name)
        print(instance.bank_apps[0].bank_id)
        print(args)
        print(request.data)
        print(kwargs)
        bank = request.data.get("bank")
        pk=kwargs.get("pk")
        print("==========")
        status = request.data.get("status")
        if status in settings.FINAL_RESPONSES:
            ba = BankApplication.objects.get(application=pk, bank__name =bank)
            ba.status = request.data.get("status")
            ba.save()
            response = {"status":"Success"}

        else:
            response = {"status": "Fail"}
        return Response(response)

    def retrieve(self, request, pk=None):
        try:
            item = get_object_or_404(self.queryset, pk=pk)
            print("000", item.bank_apps)
            serializer = self.serializer_class(item)
            print("kkk", serializer.data)
        except Exception as e:
            print(e)
        return Response(serializer.data)

    # API for getting all applications with a certain status ##
    @action(detail=False, url_path="search", methods=["get"])
    def get_status_based_apps(self, request, *args, **kwargs):
        try:
            apps = Application.objects.filter(
                bankapplication__status=request.GET.get('status'),
            )
            code = 200,
            message = True,
            data = self.serializer_class(apps, many=True).data

        except Exception as e:
            code = 200
            message = "Customer application fetch failed"
            data = {}

        return Response({"code": code,
                         "message": message,
                         "data": data, })
