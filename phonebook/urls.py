from django.urls import path
from . import views

app_name = 'phonebook'

urlpatterns = [
    # Example: /p/fanvil/x303p.xml
    path(
        "p/<str:manufacturer>/<str:token>.xml", views.phonebook_xml, name="phonebook_xml",
    ),
    path(
        "phonebooks/fanvil/3cx.xml", views.fanvil_phonebook_xml, name="fanvil_3cx_phonebook",
    ),
    path(
        "p/<str:manufacturer>/<str:token>.xml", views.dynamic_phonebook_xml, name="dynamic_phonebook_xml",
    ),
]
