# from datetime import timezone
from django.utils import timezone
from django.db import models
import uuid


class Application(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField("first name", max_length=50, null=True, blank=True)
    last_name = models.CharField("last name", max_length=50, null=True, blank=True)
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=20, verbose_name="phone number")
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)

    @property
    def bank_apps(self):
        return self.bankapplication_set.all()

    def get_pending_apps(self):
        """Get all pending applications"""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class Bank(models.Model):
    name = models.CharField("Bank Name", max_length=50)
    address = models.TextField(blank=True, null=True)


class BankApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", 'pending'),
        ("processing", 'processing'),
        ("completed", 'completed'),
        ("rejected", "rejected")
    ]
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="Pending",
    )