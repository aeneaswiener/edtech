from google.appengine.ext import ndb
import webapp2

def GetAcceptType(request):
    try:
        accept_header = request.headers['Accept']
    except KeyError:
        accept_header = None
    if accept_header is not None:
        return accept_header
    else:
        return "text/plain"

