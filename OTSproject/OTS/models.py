from django.db import models

# Create your models here.
class Candidate(models.Model):
    username=models.CharField(primary_key=True,max_length=20)
    password=models.CharField(null=False,max_length=20)
    name=models.CharField(null=False,max_length=30)
    test_attempted=models.IntegerField(default=0)
    points=models.FloatField(default=0)


class Question(models.Model):
    qid=models.BigAutoField(primary_key=True,auto_created=True)
    que=models.TextField()  
    a=models.CharField(max_length=255)  
    b=models.CharField(max_length=255)    
    c=models.CharField(max_length=255)
    d=models.CharField(max_length=255)  
    ans=models.CharField(max_length=2)    

class Result(models.Model):
    resultid=models.BigAutoField(primary_key=True,auto_created=True)
    username=models.ForeignKey(Candidate,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    time=models.TimeField(auto_now=True)
    attempt=models.IntegerField()
    right=models.IntegerField()
    wrong=models.IntegerField()
    points=models.FloatField()

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name