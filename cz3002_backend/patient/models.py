from authentication.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey
# Create your views here.
# API Test ID:
#     Game 1 and Game 2 (each set):
#     Test ID 
#     Score (int)
#     Errors (int)
#     Time taken to complete (long - milliseconds)
#     Date time complete


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


#user will connect this class
class GameTest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)


#this class for inidividual test
class Game(models.Model):
    score=models.IntegerField()
    errors=models.IntegerField()
    time_taken=models.IntegerField()
    date_time_completed=models.DateTimeField()
    game_test=models.ForeignKey(GameTest,on_delete=models.CASCADE)
    class Meta:
        abstract = True

class TrailMakingTest(Game):
    pass
class PictureObjectMatchingTest(Game):
    pass
