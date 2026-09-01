from django.urls import path
from . import views

app_name = 'phonebook'

urlpatterns = [
    # Device-facing phonebook endpoint, e.g. /p/fanvil/aBc123XyZ.xml
    #
    # manufacturer + token together select a PhonebookXML row, which
    # authorizes the request. Content is generated live from PostgreSQL
    # when a generator is registered for the manufacturer (see
    # phonebook.generators), otherwise it falls back to a manually
    # uploaded file.
    path(
        "p/<str:manufacturer>/<str:token>.xml",
        views.phonebook_xml,
        name="phonebook_xml",
    ),
]
