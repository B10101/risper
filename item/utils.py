# utils.py

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone


# Function to generate a random string
def random_string_generator():
    return get_random_string(length=10, allowed_chars="ABCDEF0123456789")

# Function to generate a unique item ID
def unique_item_id_generator(instance):
    # Generate a random string
    item_new_id = random_string_generator()

    # Get the class of the instance
    Item = instance.__class__

    # Check if any other item with the same ID exists
    qs_exists = Item.objects.filter(item_id=item_new_id).exists()

    # If another item with the same ID exists, generate a new ID
    if qs_exists:
        return unique_item_id_generator(instance)
    
    # Return the unique item ID
    return item_new_id

# Function to send overdue alerts
def send_overdue_alerts():
    from .models import Item  # Import Item locally inside the function
    overdue_items = Item.objects.filter(due_date__lt=timezone.now().date())
    for item in overdue_items:
        user = item.reserved_by
        if user:
            subject = f"Alert: Equipment '{item.name}' is overdue"
            message = f"The equipment '{item.name}' is overdue for return. Please return it as soon as possible."
            send_mail(subject, message, 'admin@example.com', [user.email])
