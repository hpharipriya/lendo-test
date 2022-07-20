import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from user_app.models import CustomerApplication
# from .serializers import CustomerApplicationSerializer
# from .forms import CustomerApplicationForm
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from core import settings
BANK_URL = settings.BANK_URL

# class customerApplicationViewSet(viewsets.ModelViewSet):
#     pass
    # """
    # API endpoint that allows users to be viewed or edited.
    # """
    # queryset = CustomerApplication.objects.all()
    # serializer_class = CustomerApplicationSerializer
    #
    # def create(self, request, *args, **kwargs):
    #     payload = request.data
    #     serializer = CustomerApplicationSerializer(data=payload)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     try:
    #         if serializer.is_valid():
    #             # headers = self.get_success_headers(serializer.data)
    #             response = {
    #                 "code": 200,
    #                 "message": "Success",
    #                 "data":
    #                     serializer.data
    #             }
    #             # Submit to bank API
    #
    #         else:
    #             response = {"code": 200,
    #                         "message": "Customer application creation failed",
    #                         "data": {}}
    #         return Response(
    #             response,
    #             # status=status.HTTP_201_CREATED,
    #             # headers=headers
    #         )
    #     except Exception as e:
    #         print(e)

    # permission_classes = [permissions.IsAuthenticated]

# class CustomerApplicationView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'application_list.html'
#
#     def get(self, request):
#         cust_app = get_object_or_404(CustomerApplication, pk=pk)
#         serializer = CustomerApplicationSerializer(cust_app)
#         return Response({'serializer': serializer, 'cust_app': cust_app})

# def get(self, request):
#     queryset = CustomerApplication.objects.all()
#     # serializer = CustomerApllicationSerializer()
#     return Response({'applications': queryset})

#
# @api_view(['GET'])
# def get_application(request):
#     # applications = CustomerApplication.objects.all()
#     # serializer = CustomerApplicationSerializer(applications, many=True)
#     return Response({"hi": "hi"})s
#
#
# @api_view(['POST'])
# def add_application(request):
#     serializer = CustomerApllicationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

# @api_view(['GET'])
# def fill_application(request):
#     print("hhh")
#     cust_form = CustomerApplicationForm()
#     customers = CustomerApplication.objects.all()
#     context =  {
#         'cust_form': cust_form,
#         'customers': customers
#     }
#     print("returnii..llll")
#     # return Response({"test":123})
#     return render(request=request, template_name='templates/core/fill_form.html', context=context)
