# 3CX SIP Phonebook Sync

A Django-based platform for synchronizing **3CX contacts with SIP/IP phones** using vendor-specific Cloud Phonebook formats.

## Architecture

```text
3CX
 │
 │ Contacts
 ▼
PhoneSync
 │
 │ Vendor-specific XML
 ▼
SIP Phones
 │
 ├── Fanvil
 ├── Grandstream
 ├── FlyVoice
 └── Panasonic
```

## Features

* 3CX contact integration
* Centralized phonebook management
* Vendor-specific XML generation
* Cloud Phonebook URLs
* Multi-vendor SIP phone support
* Django Admin interface
* PostgreSQL support

## Example

A Fanvil phone can be configured with:

```text
http://10.20.12.10:8000/phonebooks/fanvil/x303p.xml
```

The phone retrieves the phonebook from PhoneSync through the configured Cloud Phonebook URL.

## Tech Stack

* Python
* Django
* PostgreSQL
* XML
* Gunicorn
* Nginx
* Ubuntu Server

## Project Structure

```text
3cx-sip-phonebook-sync/
├── manage.py
├── config/
├── phonebook/
├── requirements.txt
├── .env.example
└── README.md
```

## Roadmap

* [x] Django phonebook management
* [x] Fanvil phonebook support
* [ ] Automated 3CX synchronization
* [ ] Grandstream support
* [ ] FlyVoice support
* [ ] Panasonic support
* [ ] Sync monitoring and logging

## Purpose

The goal is to provide a centralized solution for managing and distributing phonebooks across different SIP phone manufacturers from a single system.
