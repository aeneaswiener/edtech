from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.api import images
import math

class SubjectModel(ndb.Model):
    Name = ndb.StringProperty()

class LocationModel(ndb.Model):
    Name = ndb.StringProperty()
    Latitude = ndb.FloatProperty()
    Longitude = ndb.FloatProperty()

class AverageGradeModel(ndb.Model):
    Date = ndb.DateProperty()
    Grade = ndb.FloatProperty()

class ClassRoomModel(ndb.Model):
    Name = ndb.StringProperty()
    SchoolName = ndb.StringProperty()
    NumberOfStudents = ndb.IntegerProperty()
    Subjects = ndb.StructuredProperty(SubjectModel, repeated=True)
    Location = ndb.StructuredProperty(LocationModel, repeated=False)
    AverageGrades = ndb.StructuredProperty(AverageGradeModel, repeated=True)
    Description = ndb.StringProperty()
    Image = ndb.BlobKeyProperty()
    def tohtml(self):
        return "<html><head><title>Class Room</title></head><body>" + self.Name + "</body></html>"

    def todict(self):
        subjects = []
        for subject in self.Subjects:
            subjects.append(subject.Name)

        average_grades = []
        for average_grade in self.AverageGrades:
            average_grades.append({ 'Date': str(average_grade.Date), 'Grade': average_grade.Grade})

        image_key = None
        if self.Image is not None:
            image_key = self.Image.urlsafe()

        return { 'id': self.key.id(),
                 'Name': self.Name,
                 'SchoolName': self.SchoolName,
                 'Subjects': subjects,
                 'Location': { 'Name': self.Location.Name,
                               'Latitude': self.Location.Latitude,
                               'Longitude': self.Location.Longitude },
                 'NumberOfStundents': self.NumberOfStundents,
                 'AverageGrades': average_grades,
                 'Description': self.Description,
                 'Image': image_key }

