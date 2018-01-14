from django.db import models
from django.contrib.auth.models import Permission, User
# Create your models here.
from .choices import *


class Announcement(models.Model):
    info=models.CharField(max_length=3000)
    title = models.CharField(max_length=250)
    date=models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Award(models.Model):
    detail=models.CharField(max_length=3000)
    position = models.CharField(max_length=250)
    year=models.CharField(max_length=100)
    def __str__(self):
        return self.detail

class About(models.Model):
    user = models.ForeignKey(User, default=1)
    name=models.CharField(max_length=200)
    birth_date = models.DateField()
    position = models.CharField(max_length=250)
    dept = models.CharField(max_length=500)
    image = models.FileField()
    email = models.EmailField(max_length=100)
    telephone = models.IntegerField()
    roomnumber = models.CharField(max_length=500)
    authentication_key = models.CharField(max_length=500)
    votes=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Doctake(models.Model):
    user = models.ForeignKey(User,default=1)
    doc = models.FileField(upload_to="docs/")
    title = models.CharField(max_length=200)
    hostel = models.CharField(max_length=100,choices=HOSTEL_CHOICES)
    paid = models.CharField(max_length=5,default="no")


    def __str__(self):
        return self.title

class Filler(models.Model):
    user=models.ForeignKey(User,default=1)
    name=models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=100)
    hostel=models.CharField(max_length=100,choices=HOSTEL_CHOICES)

    def __str__(self):
        return self.name

class Boarder(models.Model):
    name = models.CharField(max_length=200)
    roomnumber = models.CharField(max_length=500)
    rollnumber=models.IntegerField()
    dept = models.CharField(max_length=500)
    telephone = models.IntegerField()


class Note(models.Model):
    class Meta:
        ordering=['-year','-votes']
    user=models.ForeignKey(User,default=1)
    title = models.CharField(max_length=200)
    material=models.FileField(upload_to="notes/")
    votes=models.IntegerField(default=0)
    year=models.IntegerField()
    Course_code=models.CharField(max_length=100)


class Messmenu(models.Model):
    user=models.ForeignKey(User,default=1)
    image=models.FileField(null=True,blank=True)
    date=models.CharField(max_length=500)

class Canteenmenu(models.Model):
    user=models.ForeignKey(User,default=1)
    image=models.FileField(null=True,blank=True)
    date=models.CharField(max_length=500)
