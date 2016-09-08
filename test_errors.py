# coding=utf-8

import unittest

from .instances import frontik_test_app


class TestHttpError(unittest.TestCase):
    def test_raise_200(self):
        response = frontik_test_app.get_page('http_error')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'success')

    def test_raise_401(self):
        response = frontik_test_app.get_page('http_error?code=401')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.raw.reason, 'Unauthorized')
        self.assertEqual(response.headers['X-Foo'], 'Bar')
        self.assertEqual(response.headers['Content-Type'], 'text/html; charset=UTF-8')
        self.assertEqual(
            response.content,
            b'<html><title>401: Unauthorized</title><body>401: Unauthorized</body></html>'
        )

    def test_raise_extended_code(self):
        response = frontik_test_app.get_page('http_error?code=429')
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.headers['X-Foo'], 'Bar')
        self.assertEqual(response.headers['Content-Type'], 'text/html; charset=UTF-8')
        self.assertEqual(
            response.content,
            b'<html><title>429: Too Many Requests</title><body>429: Too Many Requests</body></html>'
        )

    def test_raise_with_unknown_code(self):
        response = frontik_test_app.get_page('http_error?code=599')
        self.assertEqual(response.status_code, 503)

    def test_finish_with_unknown_code(self):
        response = frontik_test_app.get_page('http_error?code=599&throw=false')
        self.assertEqual(response.status_code, 503)

    def test_http_error_xml(self):
        response = frontik_test_app.get_page('xsl/simple?raise=true')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'<html><body>\n<h1>ok</h1>\n<h1>not ok</h1>\n</body></html>\n')

    def test_http_error_text(self):
        response = frontik_test_app.get_page('http_error/text_kwarg')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'This is just a plain text')

    def test_http_error_json(self):
        response = frontik_test_app.get_page('http_error/json_kwarg')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"reason": "bad argument"}')

    def test_http_error_in_prepare(self):
        response = frontik_test_app.get_page('http_error/in_prepare')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.headers['X-Foo'], 'Bar')

    def test_http_error_with_content(self):
        content = {
            'xml': b'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<doc><ok xml="true"/></doc>',
            'json': b'{"content": "json"}',
            'text': b'Text content',
            'xslt': b'<html><body><h1>ok</h1></body></html>\n',
            'jinja': b'<html><h1>%%header%%</h1>json</html>'
        }

        for mode in ('xml', 'json', 'text', 'xslt', 'jinja'):
            for reason in (None, 'Custom reason'):
                for code in (200, 400, 503):
                    reason_param = 'reason={}&'.format(reason) if reason is not None else ''
                    response = frontik_test_app.get_page(
                        'http_error/with_content?{}code={}&mode={}'.format(reason_param, code, mode)
                    )

                    self.assertEqual(response.status_code, code)
                    self.assertEqual(response.headers['X-Custom-Header'], 'value')
                    if reason is not None:
                        self.assertEqual(response.reason, reason)

                    self.assertEqual(response.content, content[mode])

    def test_write_error(self):
        response = frontik_test_app.get_page('write_error')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, b'{"write_error": true}')

    def test_write_error_exception(self):
        response = frontik_test_app.get_page('write_error?fail_write_error=true')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content, b'')
