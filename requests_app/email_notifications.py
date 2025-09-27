"""
Email notification utilities for request management system
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .models import NotificationSettings, Requestor, Status
import logging

logger = logging.getLogger(__name__)


def send_request_created_notification(request):
    """
    Send email notification when a new request is created
    """
    try:
        # Check if notifications are enabled for 'submitted' status
        submitted_status = Status.objects.filter(status='Submitted').first()
        if not submitted_status:
            return False
            
        # Check if notifications are enabled for this request type
        request_type = get_request_type(request)
        if not NotificationSettings.is_notification_enabled(request_type, submitted_status):
            return False
            
        # Get recipient email
        recipient_email = get_recipient_email(request)
        if not recipient_email:
            return False
            
        # Prepare email content
        subject = f"New {request_type.title()} Request Created - ID: #{request.key} | Type: {request_type.title()}"
        
        # Get request URL
        request_url = get_request_url(request)
        
        # Render HTML email template
        html_message = render_to_string('requests_app/emails/request_created.html', {
            'request': request,
            'request_type': request_type,
            'requestor': request.requestor,
            'request_url': request_url,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
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
        # Check if notifications are enabled for the new status
        request_type = get_request_type(request)
        if not NotificationSettings.is_notification_enabled(request_type, new_status):
            return False
            
        # Get recipient email
        recipient_email = get_recipient_email(request)
        if not recipient_email:
            return False
            
        # Prepare email content
        subject = f"{request_type.title()} Request Status Updated - ID: #{request.key} | Type: {request_type.title()}"
        
        # Get request URL
        request_url = get_request_url(request)
        
        # Render HTML email template
        html_message = render_to_string('requests_app/emails/status_changed.html', {
            'request': request,
            'request_type': request_type,
            'requestor': request.requestor,
            'old_status': old_status,
            'new_status': new_status,
            'request_url': request_url,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
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
        return 'staining'  # Default to staining


def get_request_url(request):
    """
    Get the URL for viewing a specific request
    """
    from django.urls import reverse
    
    # Determine the request type and generate appropriate URL
    request_type = get_request_type(request)
    
    try:
        if request_type == 'embedding':
            return f"http://localhost:8000{reverse('embedding_request_detail', args=[request.key])}"
        elif request_type == 'sectioning':
            return f"http://localhost:8000{reverse('sectioning_request_detail', args=[request.key])}"
        else:  # staining or default
            return f"http://localhost:8000{reverse('staining_request_detail', args=[request.key])}"
    except:
        # Fallback URL if reverse fails
        return f"http://localhost:8000/staining/{request.key}/"


def get_recipient_email(request):
    """
    Get the recipient email address for notifications
    """
    # Try to get email from requestor
    if hasattr(request, 'requestor') and request.requestor and request.requestor.email:
        return request.requestor.email
    
    # Try to get email from assigned_to if available
    if hasattr(request, 'assigned_to') and request.assigned_to and request.assigned_to.email:
        return request.assigned_to.email
    
    # Fallback to admin email
    return getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')


def send_test_email(recipient_email):
    """
    Send a test email to verify email configuration
    """
    try:
        subject = "Test Email - Histopathology Requests System"
        message = "This is a test email to verify email configuration is working correctly."
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        logger.info(f"Test email sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send test email: {str(e)}")
        return False
