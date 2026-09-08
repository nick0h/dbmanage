"""
Email notification utilities for request management system
"""
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import NotificationSettings, Status
from .email_service import get_admin_email, send_notification_email, send_test_email
import logging

logger = logging.getLogger(__name__)


def send_request_created_notification(request):
    """
    Send email notification when a new request is created
    """
    try:
        submitted_status = Status.objects.filter(status='Submitted').first()
        if not submitted_status:
            return False

        request_type = get_request_type(request)
        if not NotificationSettings.is_notification_enabled(request_type, submitted_status):
            return False

        recipient_email = get_recipient_email(request)
        if not recipient_email:
            return False

        subject = f"New {request_type.title()} Request Created - ID: #{request.key} | Type: {request_type.title()}"
        request_url = get_request_url(request)
        html_message = render_to_string('requests_app/emails/request_created.html', {
            'request': request,
            'request_type': request_type,
            'requestor': request.requestor,
            'request_url': request_url,
        })
        plain_message = strip_tags(html_message)

        send_notification_email(
            subject=subject,
            message=plain_message,
            recipient_list=[recipient_email],
            html_message=html_message,
        )

        logger.info(f"Request creation notification sent to {recipient_email} for request #{request.key}")
        return True

    except Exception as e:
        logger.error(f"Failed to send request creation notification: {str(e)}")
        return False


def send_status_change_notification(request, old_status, new_status):
    """
    Send email notification when request status changes
    """
    try:
        request_type = get_request_type(request)
        if not NotificationSettings.is_notification_enabled(request_type, new_status):
            return False

        recipient_email = get_recipient_email(request)
        if not recipient_email:
            return False

        subject = f"{request_type.title()} Request Status Updated - ID: #{request.key} | Type: {request_type.title()}"
        request_url = get_request_url(request)
        html_message = render_to_string('requests_app/emails/status_changed.html', {
            'request': request,
            'request_type': request_type,
            'requestor': request.requestor,
            'old_status': old_status,
            'new_status': new_status,
            'request_url': request_url,
        })
        plain_message = strip_tags(html_message)

        send_notification_email(
            subject=subject,
            message=plain_message,
            recipient_list=[recipient_email],
            html_message=html_message,
        )

        logger.info(f"Status change notification sent to {recipient_email} for request #{request.key}")
        return True

    except Exception as e:
        logger.error(f"Failed to send status change notification: {str(e)}")
        return False


def get_request_type(request):
    """
    Determine the request type based on the request object
    """
    if hasattr(request, 'request_type'):
        return request.request_type
    elif hasattr(request, '_meta') and 'embedding' in request._meta.model_name.lower():
        return 'embedding'
    elif hasattr(request, '_meta') and 'sectioning' in request._meta.model_name.lower():
        return 'sectioning'
    else:
        return 'staining'


def get_request_url(request):
    """
    Get the URL for viewing a specific request
    """
    from django.urls import reverse

    request_type = get_request_type(request)

    try:
        if request_type == 'embedding':
            return f"http://localhost:8000{reverse('embedding_request_detail', args=[request.key])}"
        elif request_type == 'sectioning':
            return f"http://localhost:8000{reverse('sectioning_request_detail', args=[request.key])}"
        else:
            return f"http://localhost:8000{reverse('staining_request_detail', args=[request.key])}"
    except Exception:
        return f"http://localhost:8000/staining/{request.key}/"


def get_recipient_email(request):
    """
    Get the recipient email address for notifications
    """
    if hasattr(request, 'requestor') and request.requestor and request.requestor.email:
        return request.requestor.email

    if hasattr(request, 'assigned_to') and request.assigned_to and request.assigned_to.email:
        return request.assigned_to.email

    return get_admin_email()
