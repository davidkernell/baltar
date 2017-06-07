from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from settings import POLO_WAMP_URL

class MyComponent(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        print("session ready")

        try:
            res = yield self.call(POLO_WAMP_URL, 2, 3)
            print("call result: {}".format(res))
        except Exception as e:
            print("call error: {0}".format(e))