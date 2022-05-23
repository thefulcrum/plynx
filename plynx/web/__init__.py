"""
Service endpoints.
"""
# flake8: noqa
from gevent.pywsgi import WSGIServer

import plynx.web.health
import plynx.web.node
import plynx.web.resource
import plynx.web.state
import plynx.web.user
from plynx.web.common import app, authenticate, make_fail_response, register_user, requires_auth, run_api, verify_password

# make cdp routes available when run the api
from plynx.cdp.src.web import *
