from google.appengine.ext import ndb
from util import *
from models import *

import webapp2
import jinja2
import datetime
import logging
import json
import os

templates_folder = os.path.join(os.path.dirname(__file__),'templates')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(templates_folder),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Ignore(webapp2.RequestHandler):
    def get(self):
        self.error(404)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect('/students')

url_model_mapping = { 
    'students': StudentModel, 
    'tutors': TutorModel, 
    'pledges': PledgeModel, 
    'questions': QuestionModel,
    'responses': ResponseModel
}

def getObjectKeyFromPath(path):
    components = path.split('/')
    object_id = None
    if ( len(components) % 2 ) == 0:
        object_id = int(components.pop())
            
    template_name = components.pop()
    list_kind = url_model_mapping[template_name]
    if object_id is not None:
        template_name = template_name[:-1]
        
    if list_kind is None:
        return None
    key_path = []
    key = None
    for i in range(0,(len(components)/2)):
        kind = url_model_mapping[components[(2*i)]]
        if kind is None:
            return None
        key_path.append(components[(2*i)])
        key_path.append(int(components[(2*i)+1]))

    key = None
    if len(key_path) != 0:
        key = ndb.Key(*key_path)
    return key, list_kind, object_id, template_name

def getObjectFromPath(path):
    key, kind, object_id, template_name = getObjectKeyFromPath(path)
    if object_id is not None:
        key = ndb.Key(kind, object_id, parent=key)
        retval = key.get()
        if retval is None:
            return None
        return retval.to_dict(), template_name
    else:
        objects = kind.query(ancestor=key).fetch()
        retval = []
        for obj in objects:
            retval.append(obj.to_dict())
        return retval, template_name

class Controller(webapp2.RequestHandler):
    def display(self,path,content_type):
        obj, template_name = getObjectFromPath(path)
        if obj is None:
            self.error(404)
        if content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(obj,cls=NDBJSONEncoder))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template(template_name + '.html')
            self.response.write(template.render({"obj": obj}))

    def get(self,path):
        self.display(path,GetAcceptType(self.request))

    def post(self,path):
        key, kind, object_id, template_name = getObjectKeyFromPath(path)
        if object_id is not None:
            self.error(403)
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            data = json.loads(self.request.body)
        else:
            self.response.headers['Content-Type'] = 'text/html'
            data = self.request.arguments()
        obj = kind(parent=key,**data)
        obj.put()
        self.display(path,self.request.content_type)

class Graph(webapp2.RequestHandler):
    def get(self,path):
        obj, template_name = getObjectFromPath(path)
        if obj is None:
            self.error(404)
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template(template_name + '_webview.html')
        self.response.write(template.render({"obj": obj}))



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/favicon.ico', Ignore),
    ('/graph/(.*)', Graph),
    ('/(.*)', Controller),
], debug=True)

