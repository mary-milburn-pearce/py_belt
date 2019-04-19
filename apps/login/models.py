
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['fname'] = "First name must be at least two characters long"
        if len(postData['lname']) < 2:
            errors['lname'] = "Last name must be at least two characters long"
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address"
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters long"
        else:
            if len(postData['pwconf'])<1:
                errors['pwconf'] = "Please confirm password"
            else:
                #hashed_pw=bcrypt.generate_password_hash(postData['pw'])
                hashed_pw = bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
                #if not bcrypt.check_password_hash(hashed_pw, postData['pwconf']):
                if not bcrypt.checkpw(postData['pwconf'].encode(), hashed_pw):
                    errors['pwconf'] = "Passwords do not match"
        return errors


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

    def __repr__(self):
        return f"First: {self.first_name}, Last: {self.last_name}, \
            Released: {self.email_address}, Birthday: {self.birth_date}"
