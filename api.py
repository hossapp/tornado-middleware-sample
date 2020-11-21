import os

import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

import hoss_agent.middleware.tornado as HossMiddleware


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("https://postman-echo.com/get?foo1=bar1&foo2=bar2")
        self.write(response.body)


def get_user(handler):
    return {
        "userId": 'uuid',
        "email": 'sample@example.com',
        "username": "Name"
    }


def should_skip(handler):
    return False


def make_app():
    app = tornado.web.Application([
        (r"/get", MainHandler)
    ])
    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(os.environ.get('PORT'))

    # initialize Hoss middleware before starting IOLoop
    HossMiddleware.init(os.environ.get('HOSS_API_KEY'), {
        "USER_DATA_FN": get_user,
        "SHOULD_SKIP_FN": should_skip
    })
    tornado.ioloop.IOLoop.current().start()
