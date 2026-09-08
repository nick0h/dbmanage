from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from .email_service import get_admin_email, send_notification_email, send_test_email
import logging

logger = logging.getLogger(__name__)


def send_request_created_email(request):
    """
    Send email notification when a new request is created
    """
    try:
        admin_users = User.objects.filter(is_staff=True, is_active=True)
        admin_emails = [user.email for user in admin_users if user.email]

        recipient_emails = admin_emails.copy()
        if request.requestor.email:
            recipient_emails.append(request.requestor.email)

        if not recipient_emails:
            logger.warning("No email addresses found for request notification")
            return False

        request_url = f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}{reverse('staining_request_detail', args=[request.pk])}"
        html_content = render_to_string('requests_app/emails/request_created.html', {
            'request': request,
            'request_url': request_url
        })

        send_notification_email(
            subject=f'New Request Created - #{request.key}',
            message=(
                f'A new request has been created:\n\n'
                f'Request ID: {request.key}\n'
                f'Requestor: {request.requestor.name}\n'
                f'Description: {request.description}\n\n'
                f'View details: {request_url}'
            ),
            recipient_list=recipient_emails,
            html_message=html_content,
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
        admin_users = User.objects.filter(is_staff=True, is_active=True)
        admin_emails = [user.email for user in admin_users if user.email]

        recipient_emails = admin_emails.copy()
        if request.requestor.email:
            recipient_emails.append(request.requestor.email)

        if not recipient_emails:
            logger.warning("No email addresses found for completion notification")
            return False

        request_url = f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}{reverse('staining_request_detail', args=[request.pk])}"
        html_content = render_to_string('requests_app/emails/request_completed.html', {
            'request': request,
            'request_url': request_url
        })

        send_notification_email(
            subject=f'Request Completed - #{request.key}',
            message=(
                f'Your request has been completed:\n\n'
                f'Request ID: {request.key}\n'
                f'Requestor: {request.requestor.name}\n'
                f'Description: {request.description}\n'
                f'Status: {request.status.status}\n\n'
                f'View details: {request_url}'
            ),
            recipient_list=recipient_emails,
            html_message=html_content,
        )

        logger.info(f"Request completed email sent for request #{request.key}")
        return True

    except Exception as e:
        logger.error(f"Failed to send request completed email: {str(e)}")
        return False
