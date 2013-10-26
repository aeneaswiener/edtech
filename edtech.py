from google.appengine.ext import ndb
from models import *

import webapp2
import datetime
import logging
import json


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Gethin!')

class ClassRoom(webapp2.RequestHandler):
    def post(self):
        logging.error(self.request.headers['Content-Type'])
        if self.request.headers['Content-Type'].startswith('application/json'):
            body = json.loads(self.request.body)

            subjects = []
            for subject in body['Subjects']:
                subjects.append(SubjectModel(Name=subject))

            average_grades = []
            for average_grade in body['AverageGrades']:
                average_grades.append(AverageGradeModel(
                    Date=datetime.datetime.strptime(average_grade['Date'],"%a %b %d %H:%M:%S %Y"),
                    Grade=average_grade['Grade']))

            class_room = ClassRoomModel(Name=body['Name'],
                                        SchoolName=body['SchoolName'],
                                        NumberOfStundents=body['NumberOfStudents'],
                                        Subjects=subjects,
                                        Location=LocationModel(Name=body['Location']['Name'],
                                                               Latitude=body['Location']['Latitude'],
                                                               Longitude=body['Location']['Longitude']),
                                        AverageGrades=average_grades,
                                        Description=body['Description'])
            class_room.put()
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(class_room.todict()))

    def get(self,class_id):
        if class_id is not None:
            class_room = ndb.Key( 'ClassRoomModel', int(class_id) ).get()
            if class_room is not None:
                if self.request.headers['Content-Type'].startswith('application/json'):
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.write(json.dumps(class_room.todict()))
                else:
                    self.response.headers['Content-Type'] = 'text/html'
                    self.response.write(class_room.tohtml())
            else:
                if self.request.headers['Content-Type'].startswith('application/json'):
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.write(json.dumps({'error': 'ClassRoom not found'}))
                else:
                    self.response.headers['Content-Type'] = 'text/html'
                    self.response.write("<html><head><title>Class Room</title></head><body><h1>ClassRoom not found</h1></body></html>")



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/classroom', ClassRoom),
    ('/api/classroom/(.*)', ClassRoom)
], debug=True)

