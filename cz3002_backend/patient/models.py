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
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)

    @property
    def trail_making_date_time_completed(self):
        trail_making_test = self.trailmakingtest_set.first()
        return trail_making_test.date_time_completed


#this class for inidividual test
class Game(models.Model):
    score=models.IntegerField()
    errors=models.IntegerField()
    time_taken=models.IntegerField()
    date_time_completed=models.IntegerField()
    game_test=models.ForeignKey(GameTest,on_delete=models.CASCADE)
    class Meta:
        abstract = True

class TrailMakingTest(Game):
    pass
class PictureObjectMatchingTest(Game):
    pass
