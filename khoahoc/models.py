from distutils.command.upload import upload
from email.mime import image
from django.db import models
from django.contrib.auth.models import AbstractUser
#import ckeditor
from ckeditor.fields import RichTextField

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50,null=False,unique=True)

    def __str__(self):
        return self.name

class ItemBase(models.Model):
    class Meta:
        abstract = True

    subject = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.subject


class Course (ItemBase):
    class Meta:
        unique_together = ['subject', 'category']
        ordering = ["-id"]
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

class Lesson(ItemBase):
    class Meta:
        unique_together = ['subject', 'course']
    content = RichTextField()
    course =  models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name="lessons", blank=True, null=True)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name