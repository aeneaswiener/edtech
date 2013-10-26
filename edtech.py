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

class StudentAPI(webapp2.RequestHandler):
    def get(self,class_id):
        self.response.headers['Content-Type'] = 'application/json'
        if class_id is not None:
            student = ndb.Key( 'StudentModel', int(class_id) ).get()
            if student is not None:
                self.response.write(json.dumps(student.todict()))
            else:
                self.response.write(json.dumps({'error': 'Student not found'}))

class Student(webapp2.RequestHandler):
    def get(self,class_id):
        self.response.headers['Content-Type'] = 'text/html'
        if class_id is not None:
            student = ndb.Key( 'StudentModel', int(class_id) ).get()
            if student is not None:
                self.response.write(student.tohtml())
            else:
                self.response.write("<html><head><title>Class Room</title></head><body><h1>Student not found</h1></body></html>")
            
class StudentListAPI(webapp2.RequestHandler):
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

            location=LocationModel(**body['SchoolLocation'])

            student = StudentModel(Name=body['Name'],
                                        SchoolName=body['SchoolName'],
                                        Subjects=subjects,
                                        SchoolLocation=location,
                                        AverageGrades=average_grades,
                                        Description=body['Description'])
            student.put()
            self.response.write(json.dumps(student.todict()))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            subjects = []
            average_grades = []
            student = StudentModel(Name=self.request.get('Name'),
                                        SchoolName=self.request.get('SchoolName'),
                                        Subjects=subjects,
                                        SchoolLocation=LocationModel(Name=self.request.get('Location_Name'),
                                                               Latitude=float(self.request.get('Latitude')),
                                                               Longitude=float(self.request.get('Longitude'))),
                                        AverageGrades=average_grades,
                                        Description=self.request.get('Description'))
            student.put()

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        students = StudentModel.query().fetch()
        return_value = []
        for student in students:
            return_value.append(student.todict())
        self.response.write(json.dumps(return_value))

class StudentList(webapp2.RequestHandler):
    def get(self):
        class_rooms = ClassRoomModel.query().fetch()

        print class_rooms
        self.response.headers['Content-Type'] = 'text/html'

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(class_rooms))
                
class StudentAdd(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {
            'greetings': 'hello',
        }
        template = JINJA_ENVIRONMENT.get_template('student_add.html')
        self.response.write(template.render(template_values))

class StudentSubjectListAPI(webapp2.RequestHandler):
    def get(self,class_id):        
        self.response.headers['Content-Type'] = 'application/json'
        student = ndb.Key( 'StudentModel', int(class_id) ).get()
        subjects = []
        for subject in student.Subjects:
            subjects.append(subject.Name)
        self.response.write(json.dumps(subjects))

    def post(self,class_id):
        subject_name = ""
        if self.request.content_type.startswith('application/json'):
            subject_name = json.loads(self.request.body)
        else:
            subject_name = self.request.get("Name")
        student = ndb.Key( 'StudentModel', int(class_id) ).get()
        subject_already_there = False
        for subject in student.Subjects:
            if subject.Name == subject_name:
                subject_already_there = True
                break
        if subject_already_there == False:
            student.Subjects.append(SubjectModel(Name=subject_name))
            student.put()
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            subjects = []
            for subject in student.Subjects:
                subjects.append(subject.Name)
            self.response.write(json.dumps(subjects))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write("<html><body>This is for aeneas</body></html>")

class StudentAverageGradeListAPI(webapp2.RequestHandler):
    def get(self,class_id):        
        self.response.headers['Content-Type'] = 'application/json'
        student = ndb.Key( 'StudentModel', int(class_id) ).get()
        average_grades = []
        for average_grade in student.AverageGrades:
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
        student = ndb.Key( 'StudentModel', int(class_id) ).get()
        student.AverageGrades.append(AverageGradeModel(Date=datetime.datetime.strptime(average_grade_date,"%Y-%m-%d"),Grade=average_grade_grade))
        student.put()
        if self.request.content_type.startswith('application/json'):
            self.response.headers['Content-Type'] = 'application/json'
            average_grades = []
            for average_grade in student.AverageGrades:
                average_grades.append({ 'Date': str(average_grade.Date), 'Grade': average_grade.Grade})
            self.response.write(json.dumps(average_grades))
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write("<html><body>This is for aeneas</body></html>")

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup.html', SignUpPage),
    ('/signin.html', SignInPage),
    ('/students', StudentList),
    ('/students/add', StudentAdd),
    ('/students/(.*)', Student),
    ('/api/students', StudentListAPI),
    ('/api/students/(.*)/subjects', StudentSubjectListAPI),
    ('/api/students/(.*)/grades', StudentAverageGradeListAPI),
    ('/api/students/(.*)', StudentAPI)
], debug=True)

