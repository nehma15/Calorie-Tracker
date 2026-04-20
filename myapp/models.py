from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Food(models.Model):
    name=models.CharField(max_length=100)
    carbs=models.FloatField()
    protein=models.FloatField()
    fats=models.FloatField()
    calories=models.IntegerField()

    def __str__(self):
        return self.name
    

class Consume(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    food_consumed=models.ForeignKey(Food, on_delete=models.CASCADE)


class DailyLog(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default= timezone.now)
    total_carbs = models.FloatField()
    total_protein = models.FloatField()
    total_fats = models.FloatField()
    total_calories = models.FloatField()
    

    def __str__(self):
        return f"{self.user.username} - {self.date}" 
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.FloatField()         # in cm
    weight = models.FloatField()         # in kg
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    bmi = models.FloatField(default=0)
    calorie_goal = models.IntegerField(default=2000)

    def __str__(self):
        return f"{self.user.username}'s profile"
