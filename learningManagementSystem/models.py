from django.db import models
from accounts.models import MyUser

# Create your models here.

class Course(models.Model):
    instructor = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="/courses/thumbnail")
    duration = models.IntegerField()
    rating = models.DecimalField()
    is_published = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # module name
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    order = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Content(models.Model):
    RESOURCE_TYPES = [
        ("video", "video"),
        ("image", "image"),
        ("blog", "blog"),
    ]
    section = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    resource = models.FileField(upload_to="/courses/content")
    order = models.IntegerField()
    resource_type = models.CharField(choices=RESOURCE_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Enrollment(models.Model):
    PROGRESS_STATUS = [
        ("in_progress", "in_progress"),
        ("completed", "completed"),
        ("cancelled", "cancelled"),
    ]
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(choices=PROGRESS_STATUS)
    progress_percentage = models.DecimalField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SectionProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    # this is to track if the specific moculel is completed ot not
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    progress = models.DecimalField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

