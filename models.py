from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.api import images
import math

class SubjectsModel(ndb.Model):
    Name = ndb.StringProperty()

class LocationModel(ndb.Model):
    Name = ndb.StringProperty()
    Latitude = ndb.FloatProperty()
    Longitude = ndb.FloatProperty()

class ClassRoomModel(ndb.Model):
    Name = ndb.StringProperty()
    SchoolName = ndb.StringProperty()
    NumberOfStundents = ndb.IntegerProperty()
    Subjects = ndb.StructuredProperty(SubjectsModel, repeated=True)
    Location = ndb.StructuredProperty(LocationModel, repeated=False)
    
    
        
    
