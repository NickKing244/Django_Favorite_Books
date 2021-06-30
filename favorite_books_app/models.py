from django.db import models
import re

from django.db.models.fields import DateTimeField, TextField

class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name is too short"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name is too short"
        if len(postData['email']) < 4:
            errors['email'] = "Email is too short"
        if len(postData['password']) < 8:
            errors['password'] = "Password is too short"
        if postData['password'] != postData['password_conf']:
            errors['match'] = "Password and password confirmation do not match!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['regex'] = "Invalid Email Address"
        users_with_email = User.objects.filter(email=postData['email'])
        if len(users_with_email) >= 1:
            errors['dupe'] = "Email taken, use another"
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['desc']) < 5:
            errors['desc'] = "Description Length is too short!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    objects = BookManager()
