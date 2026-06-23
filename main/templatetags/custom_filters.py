from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    return value.split(key)

@register.filter
def format_time_ampm(value):
    """
    Converts a time string to 12-hour AM/PM format.
    Handles both:
      - 24-hour "HH:MM" (e.g. "14:00" → "2:00 PM")
      - Already formatted "HH:MM AM/PM" (e.g. "02:00 PM" → "2:00 PM")
    """
    if not value:
        return '—'
    value = str(value).strip()

    # Already has AM/PM — just clean it up
    upper = value.upper()
    if 'AM' in upper or 'PM' in upper:
        try:
            parts = value.split()
            hm = parts[0].split(':')
            h = int(hm[0])
            m = int(hm[1])
            ampm = parts[1].upper()
            return f"{h}:{m:02d} {ampm}"
        except Exception:
            return value

    # 24-hour format — convert
    try:
        hm = value.split(':')
        h = int(hm[0])
        m = int(hm[1])
        ampm = 'AM' if h < 12 else 'PM'
        h12 = h % 12 or 12
        return f"{h12}:{m:02d} {ampm}"
    except Exception:
        return value