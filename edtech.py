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
        class_rooms_object = ClassRoomModel.query().fetch()

        class_rooms = []
        for class_room in class_rooms_object:
            class_rooms.append( class_room.todict() )
        template_values = {
            'class_rooms': class_rooms,
        }

        self.response.headers['Content-Type'] = 'text/html'

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class SignUpPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template_values = {
            'greetings': 'hello',
        }

        template = JINJA_ENVIRONMENT.get_template('signup.html')
        self.response.write(template.render(template_values))

class SignInPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        template_values = {
            'greetings': 'hello',
        }

        template = JINJA_ENVIRONMENT.get_template('signin.html')
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

            location=LocationModel(**body['Location'])

            class_room = ClassRoomModel(Name=body['Name'],
                                        SchoolName=body['SchoolName'],
                                        NumberOfStudents=body['NumberOfStudents'],
                                        Subjects=subjects,
                                        Location=location,
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
        class_rooms = ClassRoomModel.query().fetch()

        print class_rooms
        self.response.headers['Content-Type'] = 'text/html'

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(class_rooms))
                
class ClassRoomAdd(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
            'greetings': 'hello',
        }
        template = JINJA_ENVIRONMENT.get_template('classroom_add.html')
        self.response.write(template.render(template_values))

class ClassRoomSubjectListAPI(webapp2.RequestHandler):
    def get(self,class_id):        
        self.response.headers['Content-Type'] = 'application/json'
        class_room = ndb.Key( 'ClassRoomModel', int(class_id) ).get()
        subjects = []
        for subject in class_room.Subjects:
            subjects.append(subject.Name)
        self.response.write(json.dumps(subjects))

    def post(self,class_id):
        subject_name = ""
        if self.request.content_type.startswith('application/json'):
            subject_name = json.loads(self.request.body)
        else:
            subject_name = self.request.get("Name")
        class_room = ndb.Key( 'ClassRoomModel', int(class_id) ).get()
        subject_already_there = False
        for subject in class_room.Subjects:
            if subject.Name == subject_name:
                subject_already_there = True
                break
        if subject_already_there == False:
            class_room.Subjects.append(SubjectModel(Name=subject_name))
            class_room.put()
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            subjects = []
            for subject in class_room.Subjects:
                subjects.append(subject.Name)
            self.response.write(json.dumps(subjects))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write("<html><body>This is for aeneas</body></html>")

class ClassRoomAverageGradeListAPI(webapp2.RequestHandler):
    def get(self,class_id):        
        self.response.headers['Content-Type'] = 'application/json'
        class_room = ndb.Key( 'ClassRoomModel', int(class_id) ).get()
        average_grades = []
        for average_grade in class_room.AverageGrades:
            average_grades.append({ 'Date': str(average_grade.Date), 'Grade': average_grade.Grade})
        self.response.write(json.dumps(average_grades))

    def post(self,class_id):
        average_grade_date = ""
        average_grade_grade = ""
        if self.request.content_type.startswith('application/json'):
            json_body = json.loads(self.request.body)
            average_grade_date = json_body['Date']
            average_grade_grade = json_body['Grade']
        else:
            average_grade_date = self.request.get("Date")
            average_grade_grade = float(self.request.get("Grade"))
        class_room = ndb.Key( 'ClassRoomModel', int(class_id) ).get()
        class_room.AverageGrades.append(AverageGradeModel(Date=datetime.datetime.strptime(average_grade_date,"%Y-%m-%d"),Grade=average_grade_grade))
        class_room.put()
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            average_grades = []
            for average_grade in class_room.AverageGrades:
                average_grades.append({ 'Date': str(average_grade.Date), 'Grade': average_grade.Grade})
            self.response.write(json.dumps(average_grades))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write("<html><body>This is for aeneas</body></html>")

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup.html', SignUpPage),
    ('/signin.html', SignInPage),
    ('/classroom', ClassRoomList),
    ('/classroom/add', ClassRoomAdd),
    ('/classroom/(.*)', ClassRoom),
    ('/api/classroom', ClassRoomListAPI),
    ('/api/classroom/(.*)/subjects', ClassRoomSubjectListAPI),
    ('/api/classroom/(.*)/grades', ClassRoomAverageGradeListAPI),
    ('/api/classroom/(.*)', ClassRoomAPI)
], debug=True)

