from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.api import images
import math
import json
import time
import datetime

class NDBJSONEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,ndb.Key):
            return obj.get().to_dict()
        elif isinstance(obj,datetime.date):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(NDBJSONEncoder,self).default(obj)

class EdTechModel(ndb.Model):
    def to_dict(self):
        result = super(EdTechModel,self).to_dict()
        result['id'] = self.key.id()
        return result

class LocationModel(EdTechModel):
    Name = ndb.StringProperty()
    Latitude = ndb.FloatProperty()
    Longitude = ndb.FloatProperty()

class AverageGradeModel(EdTechModel):
    Date = ndb.DateProperty()
    Grade = ndb.FloatProperty()

class PledgeModel(EdTechModel):
    HoursPledged = ndb.IntegerProperty()
    Student = ndb.KeyProperty(kind='StudentModel')

class TutorModel(EdTechModel):
    Name = ndb.StringProperty()
    def to_dict(self):
        result = super(TutorModel,self).to_dict()
        result['Pledges'] = []
        pledges = PledgeModel.query(ancestor=self.key).fetch()
        for pledge in pledges:
            result['Pledges'].append(pledge.to_dict())
        return result

class StudentModel(EdTechModel):
    Name = ndb.StringProperty()
    SchoolName = ndb.StringProperty()
    Subject = ndb.StringProperty()
    SchoolLocation = ndb.StructuredProperty(LocationModel, repeated=False)
    AverageGrades = ndb.StructuredProperty(AverageGradeModel, repeated=True)
    Description = ndb.StringProperty()
    Image = ndb.BlobKeyProperty()
    def tohtml(self):
        return "<html><head><title>Class Room</title></head><body>" + self.Name + "</body></html>"

