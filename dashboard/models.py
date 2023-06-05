from django.db import models
from django.conf import settings

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Standard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=10)
    long_name = models.TextField(null=True)

class MCQuestion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField()
    image_url = models.URLField(null=True)
    standards = models.ManyToManyField(Standard)

class MCOption(models.Model):
    mcquestion = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField()
