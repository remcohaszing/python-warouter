# -*- encoding: utf-8 -*-
"""
This module contains tests for :mod:`warouter`.

"""
from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import unittest

import mock
import webapp2

import warouter


class UrlTest(unittest.TestCase):
    """
    Tests :func:`warouter.url`.

    """
    def setUp(self):
        warouter._mapping.clear()

    def test_root_handler_slash_url(self):
        """
        Test slash url decorated handler without parent decorated handler.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        self.assertEqual(RootHandler.url, '/')

    def test_root_handler_noslash_url(self):
        """
        Test no slash url decorated handler without parent decorated handler.

        """
        @warouter.url('/root')
        class RootHandler(webapp2.RequestHandler):
            pass

        self.assertEqual(RootHandler.url, '/root')

    def test_child_handler_url(self):
        """
        Test url when decorating a handler with parent slash decorated handler.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        @warouter.url('/child')
        class ChildHandler(RootHandler):
            pass

        self.assertEqual(ChildHandler.url, '/child')

    def test_child_of_noslash_handler_url(self):
        """
        Test url when decorating a handler with one parent decorated handler.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        @warouter.url('/child')
        class ChildHandler(RootHandler):
            pass

        self.assertEqual(ChildHandler.url, '/child')

    def test_nested_child_handler_url(self):
        """
        Test url when decorating with multiple ancestor decorated handlers.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        @warouter.url('/child')
        class ChildHandler(RootHandler):
            pass

        @warouter.url('/grandchild')
        class GrandChildHandler(ChildHandler):
            pass

        self.assertEqual(GrandChildHandler.url, '/child/grandchild')

    def test_method_override(self):
        """
        Test that child http methods are either overridden or set to None.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            def get(self):
                pass

            def post(self):
                pass

        @warouter.url('/child')
        class ChildHandler(RootHandler):
            def post(self):
                pass

        self.assertIsNone(ChildHandler.get)
        self.assertIsNot(ChildHandler.post.im_func, RootHandler.post.im_func)


class WSGIApplicationTest(unittest.TestCase):
    """
    Tests :class:`warouter.WSGIApplication`.

    """
    def setUp(self):
        warouter._mapping.clear()

    def test_auto_add_mapping(self):
        """
        Test that decorated handlers are automatically added to the mapping.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        app = warouter.WSGIApplication([RootHandler])
        route = app.router.match_routes[0]
        self.assertEqual('/', route.template)
        self.assertEqual('/', route.name)
        self.assertIs(RootHandler, route.handler)

    def test_logger(self):
        """
        Test that logging is called with the appropriate logging level.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        class WSGIApplication(warouter.WSGIApplication):
            warouter_logger = mock.Mock()

        WSGIApplication([RootHandler])
        WSGIApplication.warouter_logger.log.assert_called_once_with(
            logging.NOTSET, '/ → tests.test_warouter.RootHandler')

    @mock.patch('logging.log')
    def test_logging_level(self, log):
        """
        Test that logging is called with the appropriate logging level.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        warouter.WSGIApplication([RootHandler])
        log.assert_called_once_with(logging.NOTSET,
                                    '/ → tests.test_warouter.RootHandler')

        log.reset_mock()

        class InfoWSGIApplication(warouter.WSGIApplication):
            warouter_logging_level = logging.INFO

        InfoWSGIApplication([RootHandler])
        log.assert_called_once_with(logging.INFO,
                                    '/ → tests.test_warouter.RootHandler')

    @mock.patch('logging.log')
    def test_logging_format(self, log):
        """
        Test that a custom logging format is respected.

        """
        @warouter.url('/')
        class RootHandler(webapp2.RequestHandler):
            pass

        class WSGIApplication(warouter.WSGIApplication):
            warouter_logging_format = 'SPAM'

        WSGIApplication([RootHandler])
        log.assert_called_once_with(logging.NOTSET, 'SPAM')


class UriForTest(unittest.TestCase):
    """
    Tests :func:`warouter.uri_for`.

    """
    def setUp(self):
        warouter._mapping.clear()

    def test_find_for_handler(self):
        """
        Test that a url can be reconstructed for a decorated handler.

        """
        @warouter.url('/<number:(\d+)>')
        class RootHandler(webapp2.RequestHandler):
            pass

        app = warouter.WSGIApplication([RootHandler])
        request = webapp2.Request.blank('/')
        request.app = app
        app.set_globals(app=app, request=request)
        self.assertEqual('/42', warouter.uri_for(RootHandler, number=42))

    def test_find_for_string(self):
        """
        Test that a url can be reconstructed for a decorated handler using str.

        """
        from tests import handlers
        app = warouter.WSGIApplication([handlers.UriForTestHandler])
        request = webapp2.Request.blank('/')
        request.app = app
        app.set_globals(app=app, request=request)
        self.assertEqual('/wa/rio', warouter.uri_for(
            'tests.handlers.UriForTestHandler', string='rio'))
