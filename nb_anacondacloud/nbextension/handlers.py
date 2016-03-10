import json
import logging

from tornado import web
from tornado.escape import json_decode

from notebook.base.handlers import APIHandler

from binstar_client import errors

from .uploader import Uploader, AccountManager

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class WhoAmIHandler(APIHandler):
    _am = None

    @web.authenticated
    def get(self, **args):
        if self.am.is_logged_in():
            self.finish(json.dumps({
                'user': self.am.user,
                'organizations': self.am.organizations
            }))
        else:
            self.set_status(401)

    @web.authenticated
    def post(self, **args):
        json_body = json_decode(self.request.body)
        try:
            self.am.login(json_body['username'], json_body['password'])
        except errors.Unauthorized:
            self.set_status(401)
        except errors.BinstarError as e:
            self.set_status(400, e)

    @property
    def am(self):
        if self._am is None:
            self._am = AccountManager()
        return self._am


class PublishHandler(APIHandler):
    @web.authenticated
    def post(self, **args):
        json_body = json_decode(self.request.body)
        nb = json_body['content']
        uploader = Uploader(json_body['name'], nb)
        try:
            self.finish(json.dumps(uploader.upload()))
        except errors.Unauthorized:
            self.set_status(401, "You must login first.")
        except errors.BinstarError as e:
            self.log.error(e)
            self.set_status(400, str(e))
