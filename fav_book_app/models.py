from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters long'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters long'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters long'
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = 'Passwords do not match'
        
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['email']) == 0:
            errors['email'] = 'Please enter an email address'
        elif not email_regex.match(postData['email']):
            errors['email'] = 'Please enter a valid email address'
        
        user = User.objects.filter(email=postData['email'])

        if len(user) > 0:
            errors['eamil'] = 'Email address already in user. Please enter another one'
        
        return errors

    def login_validator(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['email'])

        if len(user) != 1:
            errors['user'] = 'User has not ben registered'
        if len(postData['email']) == 0:
            errors['email'] = 'Please enter a valid email address'
        if len(postData['password']) < 8:
            errors['password'] = 'Please enter a valid password'
        elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) != True:
            errors['password'] = 'Email address and Password do not match. Please try again'

        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = 'Please enter the book title'
        if len(postData['desc']) < 5:
            errors['desc'] = 'Description should be at least 5 characters'
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
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name='uploaded_books', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()