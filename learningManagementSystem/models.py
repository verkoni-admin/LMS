from django.db import models
from accounts.models import MyUser
from validators import validate_lecture_attachment_size


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

class Lecture(models.Model):
    RESOURCE_TYPES = [
        ("video", "video"),
        ("blog", "blog"),
    ]
    # which section does this lecture belong to?
    section = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.IntegerField()
    order = models.IntegerField()
    # what is the content type odf the lecrture??
    resource_type = models.CharField(choices=RESOURCE_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BlogLecture(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE)
    content_text = models.TextField()

class VideoLecture(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE)
    content_url = models.FileField(upload_to="/courses/video-content")

class FileAttachment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    content_file = models.FileField(upload_to="/courses/attachments", validators=[validate_lecture_attachment_size])

class LinkAttachment(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    link = models.URLField(max_length=800)

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

class LectureProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    # this is to track if the specific module is completed ot not
    module = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    progress = models.DecimalField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

