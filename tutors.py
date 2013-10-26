from google.appengine.ext import ndb
from models import *

import webapp2
import jinja2
import datetime
import logging
import json
import os

def GetAcceptType(request):
    try:
        accept_header = request.headers['Accept']
    except KeyError:
        accept_header = None
    if accept_header is not None:
        return accept_header
    else:
        return "text/plain"

class TutorAPI(webapp2.RequestHandler):
    def get(self,tutor_id):
        key = ndb.Key( 'TutorModel', int(tutor_id))
        tutor = key.get()
        if GetAcceptType(self.request).startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(tutor.to_dict()))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(tutor.Name)
            

class TutorListAPI(webapp2.RequestHandler):
    def post(self):
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            tutor_dir = json.loads(self.request.body)
            tutor = TutorModel(**tutor_dir)
            tutor.put()
            self.response.write(json.dumps(tutor.to_dict()))
        
    def get(self):
        tutors = TutorModel.query().fetch()
        if GetAcceptType(self.request).startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            return_value = []
            for tutor in tutors:
                return_value.append(tutor.to_dict())
            self.response.write(json.dumps(return_value))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            for tutor in tutors:
                self.response.write(tutor.Name + "\n")
        
