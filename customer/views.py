from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import Application, BankApplication, Bank
from .serializers import ApplicationSerializer, BankApplicationSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from core import settings
from .utils import call_bank_apis, send_to_queue
import logging

logger = logging.getLogger(__name__)

BANK_URLS = settings.BANK_URLS
BANK_INITIAL_RESPONSE = settings.BANK_INITIAL_RESPONSE


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Fetching all application objects")
        serializer = self.serializer_class(self.get_queryset(), many=True)
        response = {
            "message": "Success",
            "data":
                serializer.data
        }
        return Response(response)

    def create(self, request, *args, **kwargs):
        logger.info("Creating application object")
        payload = request.data
        serializer = ApplicationSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        try:
            if serializer.is_valid():
                for name, url in BANK_URLS.items():
                    logger.info("Calling Bank APIs")
                    # Call bank API
                    res = call_bank_apis(url, obj)
                    if res:
                        logger.info("Saving Bank API status for applications")
                        bank_application = BankApplication()
                        bank_application.application = obj
                        bank_application.bank = Bank.objects.get(name=name)
                        bank_application.status = res.get('status', BANK_INITIAL_RESPONSE)
                        bank_application.save()
                        logger.info("Sending application to queue")
                        send_to_queue(obj.uuid, bank_application.bank.name, bank_application.bank.id)

                response = {
                    "message": "Success",
                    "data":
                        serializer.data
                }

            else:
                response = {
                            "message": "Customer application creation failed",
                            "data": {}}
                Response.status_code = 424
            return Response(response, )
        except Exception as e:
            print(e)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        bank = request.data.get("bank")
        pk=kwargs.get("pk")
        status = request.data.get("status")
        if status in settings.FINAL_RESPONSES:
            ba = BankApplication.objects.get(application=pk, bank__name =bank)
            ba.status = request.data.get("status")
            ba.save()
            response = {"status": "Success"}

        else:
            response = {"status": "Fail"}
        return Response(response)

    def retrieve(self, request, pk=None):
        logger.info("Retrieving application " + str(pk))
        try:
            item = get_object_or_404(self.queryset, pk=pk)
            serializer = self.serializer_class(item)
            response = {
                "message": "Success",
                "data":
                    serializer.data
            }
        except Exception as e:
            logger.error(e)
            response = {
                "message": "Failure",
                "data": {}
            }
            Response.status_code = 400
        return Response(response)

    # API for getting all applications with a certain status ##
    @action(detail=False, url_path="search", methods=["get"])
    def get_status_based_apps(self, request, *args, **kwargs):
        status = request.GET.get('status')
        logger.info("Fetching all applications in status" + str(status))

        if status not in [x[0] for x in BankApplication.STATUS_CHOICES]:
            response = {
                "message": "Invalid status",
                "data": {}
            }
            Response.status_code = 400
        else:
            try:
                apps = BankApplication.objects.filter(
                    status=status,
                )
                data = BankApplicationSerializer(apps, many=True).data
                response = {
                    "message": "Success",
                    "data": data
                }
            except Exception as e:
                logger.error(e)
                response = {
                    "message": "Customer application fetch failed",
                    "data": {}
                }
                Response.status_code = 400

        return Response(response)
