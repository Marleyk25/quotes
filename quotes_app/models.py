from django.db import models
import re
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        userswithEmail = User.objects.filter(email= postData['email'])


        if len(postData['fname']) <3:
            errors['fnamerequired'] = "First name is required"
        if len(postData['lname']) <3:
            errors['lnamereq'] = "Last name is required"
        if len(postData['email']) <3:
            errors['emailreq'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['emailformat'] = "Email is in invalid format"
        elif len(userswithEmail)>0:
            errors['emailtaken'] = "Email already used"
        if len(postData['pw']) < 5:
            errors['pwreq'] = "Password is required"
        if postData['pw'] != postData['cpw']:
            errors['cpwreq'] = "password's must match!"
        print(errors)
        return errors

    def loginValidator(self, postData):
        errors = {}
        userswithEmail = User.objects.filter(email= postData['email'])
        print("in login printing users with email")
        if len(userswithEmail) == 0:
            errors['emailNotFound'] = "Email Doesn't Exist. Please register first"
        else:
            user = userswithEmail[0]
            if bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                print('password match')
            else:
                errors['pw'] = "invalid password"
        return errors

    def quoteValidator(self, postData):
        errors = {}
        if len(postData['form_by']) < 2:
            errors['quotereq'] = "You must enter something longer and more interesting" 
        return errors
# class QuoteManager(models.Manager):

#     def quoteValidator(self, postData):
#         errors = {}  
#         if len(postData['form_by']) < 2:
#             errors['quotereq'] = "You must enter something longer and more interesting"  
    


class User(models.Model):
    firstName= models.CharField(max_length=255)
    lastName= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    quotedBy = models.CharField(max_length= 255)
    quoteDesc = models.TextField()
    postedBy = models.ForeignKey(User, related_name = "poster", on_delete =models.CASCADE)
    favQuote = models.ManyToManyField(User, related_name = "fav")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    # objects = QuoteManager()
