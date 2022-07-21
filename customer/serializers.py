from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Application, BankApplication


class SimpleApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class BankApplicationSerializer(serializers.ModelSerializer):
    # application_details = SimpleApplicationSerializer(many=False, read_only=True)

    class Meta:
        model = BankApplication
        fields = ['bank','application','status']
        depth = 1


class ApplicationSerializer(serializers.ModelSerializer):
    bank_apps = SerializerMethodField()

    class Meta:
        model = Application
        fields = "__all__"

    def get_bank_apps(self, obj):
        return list(obj.bank_apps.values())