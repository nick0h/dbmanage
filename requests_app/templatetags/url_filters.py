from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='make_borealis_links')
def make_borealis_links(text):
    """
    Convert URLs containing 'borealis' to clickable links.
    
    This filter will detect URLs in the text that contain the word 'borealis'
    and convert them to clickable hyperlinks that open in a new tab.
    
    Examples:
    - "Check this link: https://example.borealis.com/page" 
      becomes "Check this link: <a href='https://example.borealis.com/page' target='_blank'>https://example.borealis.com/page</a>"
    - "Visit www.borealis.org" 
      becomes "Visit <a href='http://www.borealis.org' target='_blank'>www.borealis.org</a>"
    """
    if not text:
        return text
    
    # Pattern to match URLs containing 'borealis'
    # This will match http://, https://, or just www. followed by borealis
    pattern = r'(https?://[^\s]*borealis[^\s]*|www\.[^\s]*borealis[^\s]*)'
    
    def replace_url(match):
        url = match.group(1)
        # Add http:// if the URL starts with www.
        if url.startswith('www.'):
            url = 'http://' + url
        return f'<a href="{url}" target="_blank" class="borealis-link">{match.group(1)}</a>'
    
    # Replace URLs with clickable links
    result = re.sub(pattern, replace_url, text, flags=re.IGNORECASE)
    
    return mark_safe(result) 