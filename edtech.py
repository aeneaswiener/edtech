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

class ClassRoom(webapp2.RequestHandler):
    def put(self):
        logging.error(self.request.headers['Content-Type'])
        if self.request.headers['Content-Type'].startswith('application/json'):
            body = json.loads(self.request.body)

            subjects = []
            for subject in body['Subjects']:
                subjects.append(SubjectModel(id=subject))

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



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/classroom', ClassRoom)
], debug=True)

