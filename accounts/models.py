from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    gender_choice = [
        ('M','Male'),('F','Female'),
    ]
    age = models.CharField(max_length = 2)
    email = models.EmailField(unique = True)
    contact = models.CharField(max_length = 10,blank=True)
    gender = models.CharField(choices = gender_choice,max_length = 10)
    address = models.CharField(max_length = 255,blank = True)
    image = models.ImageField(upload_to = 'profile/',blank = True)
    is_elder = models.BooleanField(default = False)
    slug = models.SlugField(blank = True)


    def save(self,*args,**kwargs):
        self.slug = slugify(self.get_first_name()+self.get_last_name())
        return super().save(*args,**kwargs)

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name



class CareSeeker(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    funds = models.IntegerField()
    is_available = models.BooleanField(default = True)


    def __str__(self):
        return self.user.username
    
    def allocate_fund(self,amount):
        self.funds+=amount

    def deduct_fund(self,amount):
        self.funds-=amount

    def get_funds(self):
        return self.funds

    def set_is_available_false(self):
        self.is_available = False

    def set_is_available_true(self):
        self.is_available = True

    def get_careseeker_obj(self):
        return self.user

    def care_seeker_status(self):
        return self.is_available


class CareGiver(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    earning = models.IntegerField()
    active_care_count = models.IntegerField()
    rate_per_month = models.IntegerField()

    def __str__(self):
        return self.user.username

    def add_earning(self,amount):
        self.earning+=amount

    def get_earning(self):
        return self.earning

    def increment_care_count(self):
        self.active_care_count+=1
    
    def decrement_care_count(self):
        if self.active_care_count > 0:
            self.active_care_count-=1

    def get_active_care_count(self):
        return self.active_care_count

    def get_caregiver_obj(self):
        return self.user




