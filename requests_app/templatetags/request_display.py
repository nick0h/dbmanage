from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def format_study_ids(obj):
    """Primary study ID plus any additional studies stored in data['studies']."""
    parts = []
    study = getattr(obj, 'study', None)
    if study and getattr(study, 'study_id', None):
        parts.append(str(study.study_id))

    data = getattr(obj, 'data', None) or {}
    for entry in data.get('studies') or []:
        text = str(entry).strip()
        if not text:
            continue
        study_id = text.split(' - ', 1)[0].strip()
        if study_id and study_id not in parts:
            parts.append(study_id)

    return ', '.join(parts)


@register.filter
def cell_tooltip(value, arg=25):
    """Truncate table cell text and attach full content for hover tooltip."""
    if value is None or value == '':
        return mark_safe('-')

    try:
        max_length = int(arg)
    except (TypeError, ValueError):
        max_length = 25

    text = str(value)
    if len(text) <= max_length:
        return escape(text)

    display = f'{text[:max_length - 3]}...'
    return mark_safe(
        f'<span class="cell-hover-tooltip" data-full-text="{escape(text)}">{escape(display)}</span>'
    )
