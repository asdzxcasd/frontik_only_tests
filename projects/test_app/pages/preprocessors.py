# coding=utf-8

from tornado.concurrent import Future

from frontik.handler import PageHandler, preprocessor


@preprocessor
def dep1(handler):
    handler.run.append('dep1')

    f = Future()
    f.set_result('dep1')
    return f


@preprocessor
def dep2(handler):
    future = handler.post_url(handler.request.host + handler.request.path)
    handler.run.append('dep2')
    handler.json.put(future)
    return future


@preprocessor
def dep3(handler):
    handler.run.append('dep3')


class Page(PageHandler):
    def __init__(self, application, request, logger, **kwargs):
        super(Page, self).__init__(application, request, logger, **kwargs)
        self.run = []

    @dep1
    @preprocessor([dep2, dep3])
    def get_page(self):
        self.json.put({
            'run': self.run
        })

    def post_page(self):
        self.json.put({
            'post': True
        })
