from google.appengine.ext import ndb
from models import *
from util import *

import webapp2
import jinja2
import datetime
import logging
import json
import os

class PledgesAPI(webapp2.RequestHandler):
    def get(self,tutor_id,pledge_id):
        key = ndb.Key( 'TutorModel', int(tutor_id), 'PledgeModel', int(pledge_id))
        pledge_dict = key.get().to_dict()        
        if GetAcceptType(self.request).startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(tutor_dict,cls=NDBJSONEncoder))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write(pledge_dict['HoursPledged'])
            

class PledgesListAPI(webapp2.RequestHandler):
    def post(self,tutor_id):
        tutor=ndb.Key('TutorModel', int(tutor_id)).get()
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            pledge_dir = json.loads(self.request.body)
            pledge = PledgeModel(parent=tutor.key,
                                 HoursPledged=pledge_dir['HoursPledged'],
                                 Student=ndb.Key( 'StudentModel', pledge_dir['Student'] ))
            pledge.put()
            self.response.write(json.dumps(pledge.to_dict(),cls=NDBJSONEncoder))
        
    def get(self,tutor_id):
        tutor_key = ndb.Key( 'TutorModel', int(tutor_id))
        pledges = PledgeModel.query(ancestor=tutor_key).fetch()
        if GetAcceptType(self.request).startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            return_value = []
            for pledge in pledges:
                return_value.append(pledge.to_dict())
            self.response.write(json.dumps(return_value,cls=NDBJSONEncoder))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            for pledge in pledges:
                self.response.write(pledge.HoursPledged + "\n")
        
