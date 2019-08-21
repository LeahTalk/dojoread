from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import Users

class Authors(models.Model):
    name = models.CharField(max_length = 255)
    
class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "The book must have a title!"
        return errors

class Books(models.Model):
    title = models.CharField(max_length = 255)
    uploaded_by = models.ForeignKey(Users, related_name = 'books')
    written_by = models.ForeignKey(Authors, related_name = 'books')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class Reviews(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    book = models.ForeignKey(Books, related_name = 'reviews')
    created_by = models.ForeignKey(Users, related_name = 'reviews')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)