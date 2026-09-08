"""
Central email delivery using database-stored SMTP settings or Django settings fallback.
"""
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
import logging

logger = logging.getLogger(__name__)


def get_email_configuration():
    from .models import EmailConfiguration

    config = EmailConfiguration.load()
    if config.is_configured():
        return config
    return None


def get_admin_email():
    config = get_email_configuration()
    if config and config.admin_email:
        return config.admin_email
    return getattr(settings, 'ADMIN_EMAIL', '') or None


def get_from_email():
    config = get_email_configuration()
    if config and config.from_email:
        return config.from_email
    if config and config.email_address:
        return config.email_address
    return getattr(settings, 'DEFAULT_FROM_EMAIL', None)


def get_smtp_connection():
    config = get_email_configuration()
    if config:
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=config.smtp_host,
            port=config.smtp_port,
            username=config.email_address,
            password=config.get_password(),
            use_tls=config.use_tls,
            use_ssl=config.use_ssl,
        )
    return get_connection()


def send_notification_email(subject, message, recipient_list, html_message=None, from_email=None):
    recipients = [email for email in recipient_list if email]
    if not recipients:
        logger.warning('No recipient emails provided for notification')
        return False

    from_addr = from_email or get_from_email()
    if not from_addr:
        logger.error('No from email configured for notifications')
        return False

    connection = get_smtp_connection()
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_addr,
        to=recipients,
        connection=connection,
    )
    if html_message:
        email.attach_alternative(html_message, 'text/html')

    email.send(fail_silently=False)
    return True


def send_test_email(recipient_email):
    subject = 'Test Email - Histopathology Requests System'
    message = (
        'This is a test email to verify that your Outlook/SMTP configuration '
        'is working correctly.'
    )
    send_notification_email(subject, message, [recipient_email])
    logger.info('Test email sent to %s', recipient_email)
    return True


def format_smtp_error(error):
    """Return a user-friendly explanation for common SMTP failures."""
    message = str(error)
    lowered = message.lower()

    if 'smtpclientauthentication is disabled' in lowered or 'smtp_auth_disabled' in lowered:
        return (
            'Microsoft has SMTP authentication disabled for this mailbox. '
            'A Microsoft 365 admin must enable "Authenticated SMTP" for your account '
            'in the Exchange admin center, or run: '
            'Set-CASMailbox -Identity <your-email> -SmtpClientAuthenticationDisabled $false. '
            'See https://aka.ms/smtp_auth_disabled'
        )

    if 'authentication unsuccessful' in lowered or '535' in message:
        return (
            'SMTP login failed. For Outlook/Microsoft 365, confirm SMTP AUTH is enabled '
            'for the mailbox, use your full email as the username, and use an app password '
            'if multi-factor authentication is required.'
        )

    return message
