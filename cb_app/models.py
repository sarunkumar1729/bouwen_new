from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UsersProfile(models.Model):
    fullname=models.CharField(max_length=255)
    profile_user=models.ForeignKey(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='profile_photos/', blank=True)
    email=models.EmailField(null=True)
    phone1=models.CharField(max_length=255,null=True)
    phone2=models.CharField(max_length=255,null=True)
    phone1_verified=models.BooleanField(default=False)
    phone2_verified=models.BooleanField(default=False)
    current_address=models.CharField(max_length=255)
    permanant_address=models.CharField(max_length=255)
    Education=models.CharField(max_length=255)
    skills=models.CharField(max_length=255)
    certifications=models.CharField(max_length=255)
    resume=models.FileField(upload_to='resume/',blank=True)

class Jobs(models.Model):
    job_title=models.CharField(max_length=255)
    company_name=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    mode=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    experience_required=models.IntegerField()
    skills_required=models.CharField(max_length=255)
    starting_salary=models.IntegerField()
    ending_salary=models.IntegerField()
    languages=models.CharField(max_length=255)
    # resume=models.FileField(upload_to='resume')

class Applications(models.Model):
    candidate=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    applied_date=models.DateTimeField(auto_now=True)
    

