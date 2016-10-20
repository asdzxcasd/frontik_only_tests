# coding=utf-8

import unittest

from .instances import frontik_test_app

POSTPROCESS_URL = 'postprocess/?{}'


class TestPostprocessors(unittest.TestCase):
    def test_no_postprocessors(self):
        response = frontik_test_app.get_page(POSTPROCESS_URL.format(''))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'<html><h1>%%header%%</h1>%%content%%</html>')

    def test_template_postprocessors_single(self):
        response = frontik_test_app.get_page(POSTPROCESS_URL.format('header'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'<html><h1>HEADER</h1>%%content%%</html>')

    def test_template_postprocessors_multiple(self):
        response = frontik_test_app.get_page(POSTPROCESS_URL.format('header&content'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'<html><h1>HEADER</h1>CONTENT</html>')

    def test_template_postprocessors_with_json(self):
        response = frontik_test_app.get_page(POSTPROCESS_URL.format('content&notpl'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"content": "CONTENT"}')
