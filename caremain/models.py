from django.db import models
from accounts.models import User
from datetime import datetime

class CareRequests(models.Model):

    statuses = [
        ('approved','a'),('rejected','r'),('pending','p'),('completed','c'),('active','A'),
    ]

    caregiver = models.ForeignKey(User,models.CASCADE,related_name = 'givers')
    careseeker = models.ForeignKey(User,models.CASCADE,related_name = 'seekers')
    status = models.CharField(max_length = 50,choices = statuses)
    timestamp = models.DateTimeField(auto_now_add=True)
    start_service = models.DateTimeField(blank = True,null = True)
    end_service = models.DateTimeField(blank = True,null = True)

    def __str__(self):
        return "{}-{}".format(self.caregiver.username,self.careseeker.username)

    def get_request_status(self):
        return self.status

    def set_request_status(self,state):
        self.status = state


class Transaction(models.Model):
    caregiver = models.ForeignKey(User,models.CASCADE,related_name = 'tgiver')
    careseeker = models.ForeignKey(User,models.CASCADE,related_name = 'tseeker')
    tamount = models.IntegerField()
    timestamp = models.DateTimeField(default = datetime.now())

