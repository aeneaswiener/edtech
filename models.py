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
            return obj.strftime('%Y-%m-%d')
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

class ResponseModel(EdTechModel):
    ResponeDate = ndb.DateProperty()
    Response = ndb.StringProperty()

class QuestionModel(EdTechModel):
    DateAsked = ndb.DateProperty()
    Qustion = ndb.StringProperty()

class AverageGradeModel(EdTechModel):
    Date = ndb.DateProperty()
    Grade = ndb.FloatProperty()
    def __init__(self, **kwds):
        if 'Date' in kwds:
            if not isinstance(kwds['Date'],datetime.date):
                kwds['Date']=datetime.datetime.strptime(kwds['Date'],"%Y-%m-%d") 
        super(AverageGradeModel,self).__init__(**kwds)

class PledgeModel(EdTechModel):
    HoursPledged = ndb.IntegerProperty()
    Student = ndb.KeyProperty(kind='StudentModel')
    def __init__(self, **kwds):
        if 'Student' in kwds:
            if not isinstance(kwds['Student'],ndb.Key):
                kwds['Student'] = ndb.Key( 'StudentModel', int(kwds['Student']) )
        super(PledgeModel, self).__init__(**kwds)

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
            


