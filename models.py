from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.api import images
import math

class SubjectModel(ndb.Model):
    pass

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
    NumberOfStundents = ndb.IntegerProperty()
    Subjects = ndb.StructuredProperty(SubjectModel, repeated=True)
    Location = ndb.StructuredProperty(LocationModel, repeated=False)
    AverageGrades = ndb.StructuredProperty(AverageGradeModel, repeated=True)
    Description = ndb.StringProperty()
    Image = ndb.BlobKeyProperty()

