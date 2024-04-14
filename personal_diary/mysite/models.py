from django.db import models
from django.contrib import auth
# Create your models here.
#自定義User 表單
class User(models.Model):
    name = models.CharField(max_length=20,null=False)
    email = models.EmailField()
    password = models.CharField(max_length=20,null=False)
    enaabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(auth.models.User,on_delete=models.CASCADE)
    height = models.PositiveIntegerField(default=160)
    male = models.BooleanField(default=False)
    website = models.URLField(null=True)

    def __str__(self):
        return self.user.username

class Diary(models.Model):
    user = models.ForeignKey(auth.models.User,on_delete=models.CASCADE)
    budget = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    note = models.TextField()
    ddate = models.DateField()

    def __str__(self):
        return f"{self.ddate}({self.user})"


class Vote(models.Model):
    name = models.CharField(max_length=20)
    no = models.IntegerField()
    sex = models.BooleanField(default=False)
    byear = models.IntegerField()
    party = models.CharField(max_length=20)
    votes = models.IntegerField()

    def __str__(self):
        return self.name