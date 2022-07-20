from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Application, BankApplication


class BankApplicationSerializer(serializers.ModelSerializer):
    bank_apps = SerializerMethodField()

    class Meta:
        model = BankApplication
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    bank_apps = SerializerMethodField()

    class Meta:
        model = Application
        fields = "__all__"

    def get_bank_apps(self, obj):
        return list(obj.bank_apps.values())