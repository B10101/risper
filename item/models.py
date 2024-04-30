from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_item_id_generator
from django.contrib.auth.models import User
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Item(models.Model):
    DEVICE_TYPE_CHOICES = [
        ('Mobile Device', 'Mobile Device'),
        ('Non-Portable PC', 'Non-Portable PC'),
        ('Laptop', 'Laptop'),
        ('Standalone Headset', 'Standalone Headset'),
    ]

    CPU_CHOICES = [
        ('I7-7700HQ', 'I7-7700HQ'),
        ('I7-8750H', 'I7-8750H'),
        ('M2 10C', 'M2 10C'),
        ('BCM2711C0', 'BCM2711C0'),
        ('6-Core Intel Core I5', '6-Core Intel Core I5'),
    ]

    GPU_CHOICES = [
        ('GTX 1070', 'GTX 1070'),
        ('RTX 2070', 'RTX 2070'),
    ]

    RAM_CHOICES = [
        ('32', '32'),
        ('16', '16'),
    ]

    name = models.CharField(max_length=100, null=True, verbose_name="Device name")
    type = models.CharField(max_length=100, null=True, choices=DEVICE_TYPE_CHOICES, verbose_name="Device type")
    serial = models.CharField(max_length=100, null=True, verbose_name="Device Serial")
    cpu = models.CharField(max_length=100, null=True, choices=CPU_CHOICES, verbose_name="CPU")
    gpu = models.CharField(max_length=100, null=True, choices=GPU_CHOICES, verbose_name="GPU")
    ram = models.CharField(max_length=100, null=True, choices=RAM_CHOICES, verbose_name="RAM")
    item_id = models.CharField(max_length=10, verbose_name="Item ID", primary_key=True, null=False)
    
    # New fields for reservation and booking
    availability = models.BooleanField(default=True, verbose_name="Availability")
    return_date = models.DateField(null=True, blank=True, verbose_name="Return Date")
    reserved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations', verbose_name="Reserved By")
    due_date = models.DateField(null=True, blank=True, verbose_name="Due Date")
    on_site_only = models.BooleanField(default=False)  # New field to indicate if item is on-site only


    def __str__(self):
        return self.item_id  # String representation of the Item object

    

# Signal function to generate unique item ID before saving
def pre_save_create_item_id(sender, instance, *args, **kwargs):
    if not instance.item_id:
        instance.item_id = unique_item_id_generator(instance)

# Connecting the signal to the Item model's pre_save event
pre_save.connect(pre_save_create_item_id, sender=Item)
