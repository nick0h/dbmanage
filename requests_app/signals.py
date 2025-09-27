from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Request, EmbeddingRequest, SectioningRequest, Status
from .email_notifications import send_request_created_notification, send_status_change_notification
import logging

logger = logging.getLogger(__name__)

# Store original status for comparison
_original_status = {}

@receiver(pre_save, sender=Request)
def store_original_status_request(sender, instance, **kwargs):
    """Store the original status before saving"""
    if instance.pk:
        try:
            original = Request.objects.get(pk=instance.pk)
            _original_status[instance.pk] = original.status
        except Request.DoesNotExist:
            _original_status[instance.pk] = None

@receiver(post_save, sender=Request)
def request_created_handler(sender, instance, created, **kwargs):
    """
    Send email notification when a new request is created
    """
    if created:
        logger.info(f"New request created: #{instance.key}")
        try:
            send_request_created_notification(instance)
        except Exception as e:
            logger.error(f"Failed to send creation email for request #{instance.key}: {str(e)}")

@receiver(post_save, sender=Request)
def request_status_changed_handler(sender, instance, **kwargs):
    """
    Send email notification when a request status changes
    """
    if instance.pk in _original_status:
        old_status = _original_status[instance.pk]
        new_status = instance.status
        
        # Only send notification if status actually changed
        if old_status != new_status and old_status is not None:
            logger.info(f"Request #{instance.key} status changed from {old_status} to {new_status}")
            try:
                send_status_change_notification(instance, old_status, new_status)
            except Exception as e:
                logger.error(f"Failed to send status change email for request #{instance.key}: {str(e)}")
        
        # Clean up
        del _original_status[instance.pk]

# Embedding Request Signals
@receiver(pre_save, sender=EmbeddingRequest)
def store_original_status_embedding(sender, instance, **kwargs):
    """Store the original status before saving"""
    if instance.pk:
        try:
            original = EmbeddingRequest.objects.get(pk=instance.pk)
            _original_status[instance.pk] = original.status
        except EmbeddingRequest.DoesNotExist:
            _original_status[instance.pk] = None

@receiver(post_save, sender=EmbeddingRequest)
def embedding_request_created_handler(sender, instance, created, **kwargs):
    """Send email notification when a new embedding request is created"""
    if created:
        logger.info(f"New embedding request created: #{instance.key}")
        try:
            send_request_created_notification(instance)
        except Exception as e:
            logger.error(f"Failed to send creation email for embedding request #{instance.key}: {str(e)}")

@receiver(post_save, sender=EmbeddingRequest)
def embedding_request_status_changed_handler(sender, instance, **kwargs):
    """Send email notification when embedding request status changes"""
    if instance.pk in _original_status:
        old_status = _original_status[instance.pk]
        new_status = instance.status
        
        if old_status != new_status and old_status is not None:
            logger.info(f"Embedding request #{instance.key} status changed from {old_status} to {new_status}")
            try:
                send_status_change_notification(instance, old_status, new_status)
            except Exception as e:
                logger.error(f"Failed to send status change email for embedding request #{instance.key}: {str(e)}")
        
        del _original_status[instance.pk]

# Sectioning Request Signals
@receiver(pre_save, sender=SectioningRequest)
def store_original_status_sectioning(sender, instance, **kwargs):
    """Store the original status before saving"""
    if instance.pk:
        try:
            original = SectioningRequest.objects.get(pk=instance.pk)
            _original_status[instance.pk] = original.status
        except SectioningRequest.DoesNotExist:
            _original_status[instance.pk] = None

@receiver(post_save, sender=SectioningRequest)
def sectioning_request_created_handler(sender, instance, created, **kwargs):
    """Send email notification when a new sectioning request is created"""
    if created:
        logger.info(f"New sectioning request created: #{instance.key}")
        try:
            send_request_created_notification(instance)
        except Exception as e:
            logger.error(f"Failed to send creation email for sectioning request #{instance.key}: {str(e)}")

@receiver(post_save, sender=SectioningRequest)
def sectioning_request_status_changed_handler(sender, instance, **kwargs):
    """Send email notification when sectioning request status changes"""
    if instance.pk in _original_status:
        old_status = _original_status[instance.pk]
        new_status = instance.status
        
        if old_status != new_status and old_status is not None:
            logger.info(f"Sectioning request #{instance.key} status changed from {old_status} to {new_status}")
            try:
                send_status_change_notification(instance, old_status, new_status)
            except Exception as e:
                logger.error(f"Failed to send status change email for sectioning request #{instance.key}: {str(e)}")
        
        del _original_status[instance.pk]

def send_test_notification():
    """
    Send a test notification to verify email system is working
    """
    try:
        from .email_notifications import send_test_email
        return send_test_email('admin@example.com')
    except Exception as e:
        logger.error(f"Failed to send test notification: {str(e)}")
        return False

