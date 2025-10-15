from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

def send_request_created_email(request):
    """
    Send email notification when a new request is created
    """
    try:
        # Get admin users to notify
        admin_users = User.objects.filter(is_staff=True, is_active=True)
        admin_emails = [user.email for user in admin_users if user.email]
        
        # Add the requestor email if available
        recipient_emails = admin_emails.copy()
        if request.requestor.email:
            recipient_emails.append(request.requestor.email)
        
        if not recipient_emails:
            logger.warning("No email addresses found for request notification")
            return False
        
        # Build the request URL
        request_url = f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}{reverse('staining_request_detail', args=[request.pk])}"
        
        # Render email template
        html_content = render_to_string('requests_app/emails/request_created.html', {
            'request': request,
            'request_url': request_url
        })
        
        # Send email
        send_mail(
            subject=f'New Request Created - #{request.key}',
            message=f'A new request has been created:\n\nRequest ID: {request.key}\nRequestor: {request.requestor.name}\nDescription: {request.description}\n\nView details: {request_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_emails,
            html_message=html_content,
            fail_silently=False
        )
        
        logger.info(f"Request created email sent for request #{request.key}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send request created email: {str(e)}")
        return False

def send_request_completed_email(request):
    """
    Send email notification when a request is completed
    """
    try:
        # Get admin users to notify
        admin_users = User.objects.filter(is_staff=True, is_active=True)
        admin_emails = [user.email for user in admin_users if user.email]
        
        # Add the requestor email if available
        recipient_emails = admin_emails.copy()
        if request.requestor.email:
            recipient_emails.append(request.requestor.email)
        
        if not recipient_emails:
            logger.warning("No email addresses found for completion notification")
            return False
        
        # Build the request URL
        request_url = f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}{reverse('staining_request_detail', args=[request.pk])}"
        
        # Render email template
        html_content = render_to_string('requests_app/emails/request_completed.html', {
            'request': request,
            'request_url': request_url
        })
        
        # Send email
        send_mail(
            subject=f'Request Completed - #{request.key}',
            message=f'Your request has been completed:\n\nRequest ID: {request.key}\nRequestor: {request.requestor.name}\nDescription: {request.description}\nStatus: {request.status.status}\n\nView details: {request_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_emails,
            html_message=html_content,
            fail_silently=False
        )
        
        logger.info(f"Request completed email sent for request #{request.key}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send request completed email: {str(e)}")
        return False

def send_test_email():
    """
    Send a test email to verify email configuration
    """
    try:
        send_mail(
            subject='Test Email from Antibody Requests System',
            message='This is a test email to verify that email notifications are working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False
        )
        logger.info("Test email sent successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to send test email: {str(e)}")
        return False








