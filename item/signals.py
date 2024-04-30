
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item
from utils import send_overdue_alerts

@receiver(post_save, sender=Item)
def item_due_date_updated(sender, instance, created, **kwargs):
    if instance.is_overdue():
        send_overdue_alerts()
