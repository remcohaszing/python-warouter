# -*- encoding: utf-8 -*-
"""
This module contains helper handlers for unittests.

"""
from __future__ import absolute_import
from __future__ import unicode_literals

import warouter
import webapp2


@warouter.url('/wa/<string:([a-z]+)>')
class UriForTestHandler(webapp2.RequestHandler):
    """
    This handler is used by :class:`UriForTest`.

    """
