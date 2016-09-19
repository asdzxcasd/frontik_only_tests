# coding=utf-8

import unittest

from requests.exceptions import Timeout

from .instances import frontik_test_app


class TestPreprocessors(unittest.TestCase):
    def test_preprocessors_new(self):
        response_json = frontik_test_app.get_page_json('preprocessors')
        self.assertEqual(
            response_json,
            {
                'run': ['dep1', 'dep2', 'dep3'],
                'post': True
            }
        )
