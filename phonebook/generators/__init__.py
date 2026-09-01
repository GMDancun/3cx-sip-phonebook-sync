"""
Registry of manufacturer -> XML generator functions.

To support a new phone manufacturer, write a `generate_<name>_phonebook()`
function (see fanvil.py for the reference implementation) and register it
here. The dynamic phonebook view (phonebook.views.phonebook_xml) looks a
manufacturer up in this dict; if it's not registered, the view falls back
to serving a manually-uploaded PhonebookXML.xml_file instead.
"""

from .fanvil import generate_fanvil_phonebook

GENERATORS = {
    "fanvil": generate_fanvil_phonebook,
}


def get_generator(manufacturer: str):
    """Return the generator function for a manufacturer, or None."""
    return GENERATORS.get(manufacturer.lower())
