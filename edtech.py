from google.appengine.ext import ndb
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

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template_values = {
            'greetings': 'hello',
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class ClassRoomAPI(webapp2.RequestHandler):
    def get(self,class_id):
        self.response.headers['Content-Type'] = 'application/json'
        if class_id is not None:
            class_room = ndb.Key( 'ClassRoomModel', int(class_id) ).get()
            if class_room is not None:
                self.response.write(json.dumps(class_room.todict()))
            else:
                self.response.write(json.dumps({'error': 'ClassRoom not found'}))

class ClassRoom(webapp2.RequestHandler):
    def get(self,class_id):
        self.response.headers['Content-Type'] = 'text/html'
        if class_id is not None:
            class_room = ndb.Key( 'ClassRoomModel', int(class_id) ).get()
            if class_room is not None:
                self.response.write(class_room.tohtml())
            else:
                self.response.write("<html><head><title>Class Room</title></head><body><h1>ClassRoom not found</h1></body></html>")
            
class ClassRoomListAPI(webapp2.RequestHandler):
    def post(self):
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            body = json.loads(self.request.body)

            subjects = []
            for subject in body['Subjects']:
                subjects.append(SubjectModel(Name=subject))
            
            average_grades = []
            for average_grade in body['AverageGrades']:
                average_grades.append(AverageGradeModel(
                    Date=datetime.datetime.strptime(average_grade['Date'],"%Y-%m-%d"),
                    Grade=average_grade['Grade']))

            class_room = ClassRoomModel(Name=body['Name'],
                                        SchoolName=body['SchoolName'],
                                        NumberOfStudents=body['NumberOfStudents'],
                                        Subjects=subjects,
                                        Location=LocationModel(Name=body['Location']['Name'],
                                                               Latitude=body['Location']['Latitude'],
                                                               Longitude=body['Location']['Longitude']),
                                        AverageGrades=average_grades,
                                        Description=body['Description'])
            class_room.put()
            self.response.write(json.dumps(class_room.todict()))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            subjects = []
            average_grades = []
            class_room = ClassRoomModel(Name=self.request.get('Name'),
                                        SchoolName=self.request.get('SchoolName'),
                                        NumberOfStudents=int(self.request.get('NumberOfStudents')),
                                        Subjects=subjects,
                                        Location=LocationModel(Name=self.request.get('Location_Name'),
                                                               Latitude=float(self.request.get('Latitude')),
                                                               Longitude=float(self.request.get('Longitude'))),
                                        AverageGrades=average_grades,
                                        Description=self.request.get('Description'))
            class_room.put()

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        class_rooms = ClassRoomModel.query().fetch()
        return_value = []
        for class_room in class_rooms:
            return_value.append(class_room.todict())
        self.response.write(json.dumps(return_value))

class ClassRoomList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
            'greetings': 'hello',
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
                

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/classroom', ClassRoomList),
    ('/classroom/(.*)', ClassRoom),
    ('/api/classroom', ClassRoomListAPI),
    ('/api/classroom/(.*)', ClassRoomAPI)
], debug=True)

