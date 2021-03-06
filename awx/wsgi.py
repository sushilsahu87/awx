# Copyright (c) 2015 Ansible, Inc.
# All Rights Reserved.

import logging
from awx import __version__ as tower_version

# Prepare the AWX environment.
from awx import prepare_env, MODE
prepare_env()

import django  # NOQA
from django.conf import settings  # NOQA
from django.urls import resolve  # NOQA
from django.core.wsgi import get_wsgi_application # NOQA
import social_django  # NOQA


"""
WSGI config for AWX project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

if MODE == 'production':
    logger = logging.getLogger('awx.main.models.jobs')
    try:
        fd = open("/var/lib/awx/.tower_version", "r")
        if fd.read().strip() != tower_version:
            raise Exception()
    except Exception:
        logger.error("Missing or incorrect metadata for Tower version.  Ensure Tower was installed using the setup playbook.")
        raise Exception("Missing or incorrect metadata for Tower version.  Ensure Tower was installed using the setup playbook.")

if social_django.__version__ != '2.1.0':
    raise RuntimeError("social_django version other than 2.1.0 detected {}. \
            Confirm that per-request social_django.utils.BACKENDS override \
            still works".format(social_django.__version__))


if not django.__version__.startswith('1.'):
    raise RuntimeError("Django version other than 1.XX detected {}. \
            Inherit from WSGIHandler to support short-circuit Django Middleware. \
            This is known to work for Django 1.XX and may not work with other, \
            even minor, versions.".format(django.__version__))


# Return the default Django WSGI application.
application = get_wsgi_application()
