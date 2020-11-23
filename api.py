#!/usr/bin/env python

import logging
import os

import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options

import hoss_agent.middleware.tornado as HossMiddleware


define("port", default="8000", help="Listening port", type=str)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("https://postman-echo.com/get?foo1=bar1&foo2=bar2")
        self.write(response.body)


def get_user(handler):
    return {
        "userId": handler.request.query_arguments.get('userId', ['uuid'])[0],
        "email": handler.request.query_arguments.get('email', ['sample@example.com'])[0],
        "username": handler.request.query_arguments.get('userName', ['userName'])[0]
    }


def should_skip(handler):
    return False


def make_app():
    app = tornado.web.Application([
        (r"/get", MainHandler)
    ])
    return app


def main():
    tornado.options.parse_command_line()
    print "Server listening on port: " + str(options.port)
    logging.getLogger().setLevel(logging.INFO)
    http_server = tornado.httpserver.HTTPServer(make_app())

    # initialize Hoss middleware before starting IOLoop
    HossMiddleware.init(os.environ.get('HOSS_API_KEY'), {
        "USER_DATA_FN": get_user,
        "SHOULD_SKIP_FN": should_skip
    })

    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
