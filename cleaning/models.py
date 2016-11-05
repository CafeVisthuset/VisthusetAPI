from django.db import models

class CleanDay(models.Model):
    day = models.DateField('Clean_day')
    describtion = models.CharField(max_length = 100, null = True)
    signature = models.CharField(max_length = 50, null = True)
    
class CleanTask(models.Model):
    cleanday = models.ForeignKey(
        CleanDay,
        on_delete=models.CASCADE
        )
    taskType = models.CharField(max_length = 50)
    numberTimes = models.IntegerField(default = 0)
    
class CleanType(models.Model):
    cleanID = models.CharField(max_length = 50, primary_key = True)
    taskDone = models.BooleanField(default = False)
