from django.db import models
from django.contrib.auth.models import User


from uuid import uuid4

# Create your models here.
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)

class CourseJoinCode(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class UserCourseSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)