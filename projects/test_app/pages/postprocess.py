# coding=utf-8

import frontik.handler


class ContentPostprocessor(object):
    def __call__(self, handler, tpl, callback):
        callback(tpl.replace(b'%%content%%', b'CONTENT'))


class Page(frontik.handler.PageHandler):
    def get_page(self):
        self.set_template('postprocess.html')
        self.json.put({'content': '%%content%%'})

        if self.get_argument('header', None) is not None:
            self.add_template_postprocessor(Page._header_pp)

        if self.get_argument('content', None) is not None:
            self.add_template_postprocessor(ContentPostprocessor())

    def _header_pp(self, tpl, callback):
        callback(tpl.replace(b'%%header%%', b'HEADER'))
