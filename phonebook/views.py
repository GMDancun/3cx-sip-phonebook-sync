from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .generators import get_generator
from .models import PhonebookXML, PhonebookAccessLog

# How long a generated phonebook is cached before being rebuilt from
# PostgreSQL. Devices poll on their own schedule (typically every 30-60
# minutes) so this just protects the DB from a stampede of phones fetching
# at the same moment (e.g. right after a power outage) without meaningfully
# delaying propagation of 3CX changes, which land on the next sync cycle
# anyway.
PHONEBOOK_CACHE_SECONDS = 60


def _client_ip(request):
    """Best-effort real client IP, accounting for a reverse proxy (nginx/etc)."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _log_access(entry, request):
    # Wrapped so a logging failure never breaks the actual phonebook
    # response the device is waiting on.
    try:
        PhonebookAccessLog.objects.create(
            phonebook=entry,
            ip_address=_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
        )
    except Exception:
        pass


def phonebook_xml(request, manufacturer, token):
    """
    Serves the phonebook a device fetches, at /p/<manufacturer>/<token>.xml.

    The token+manufacturer combination on the PhonebookXML row is what
    authorizes the request (there's no separate login) and controls which
    device family gets which content.

    If a dynamic generator is registered for this manufacturer (see
    phonebook.generators), the XML is built live from PostgreSQL and the
    result is cached briefly. Otherwise this falls back to serving whatever
    file was manually uploaded to xml_file, for manufacturers that don't
    have a generator yet.
    """
    entry = get_object_or_404(
        PhonebookXML,
        manufacturer__iexact=manufacturer,
        token=token,
    )

    generator = get_generator(entry.manufacturer)

    if generator is not None:
        cache_key = f"phonebook_xml:{entry.manufacturer.lower()}:{entry.model.lower()}"
        content = cache.get(cache_key)
        if content is None:
            content = generator()
            cache.set(cache_key, content, PHONEBOOK_CACHE_SECONDS)
    elif entry.xml_file:
        with entry.xml_file.open("rb") as f:
            content = f.read()
    else:
        return HttpResponse(
            "No dynamic generator registered for this manufacturer and no "
            "file has been uploaded for it.",
            status=404,
        )

    _log_access(entry, request)

    return HttpResponse(content, content_type="application/xml")
