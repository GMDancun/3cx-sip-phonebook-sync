from xml.etree.ElementTree import Element, SubElement, tostring

from integrations.models import ThreeCXUser


def generate_fanvil_phonebook():
    root = Element("phonebook")

    users = (
        ThreeCXUser.objects
        .filter(enabled=True)
        .order_by("extension")
    )

    for user in users:
        row = SubElement(root, "row")

        name = SubElement(row, "name")
        name.text = user.display_name or user.extension

        office_number = SubElement(row, "office_number")
        office_number.text = user.extension

        mobile_number = SubElement(row, "mobile_number")
        mobile_number.text = ""

        other_number = SubElement(row, "other_number")
        other_number.text = ""

        line = SubElement(row, "line")
        line.text = "0"

        ring = SubElement(row, "ring")
        ring.text = "1"

        group_name = SubElement(row, "group_name")
        group_name.text = ""

        photo = SubElement(row, "photo")
        photo.text = ""

        auto_divert = SubElement(row, "auto_divert")
        auto_divert.text = ""

    return tostring(
        root,
        encoding="utf-8",
        xml_declaration=True,
    )