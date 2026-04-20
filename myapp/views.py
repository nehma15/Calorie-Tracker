from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

# Create your views here.



#HOMEPAGE
def home(request):
    return render(request,'homepage.html')



# REGISTRATION
def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('register')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect("login")

    return render(request,"register.html")



# LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # check if user already has a profile
            if UserProfile.objects.filter(user=user).exists():
                return redirect('index_page')   # already set up → go to index
            else:
                return redirect('bmi')          # first time → go to BMI page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


@login_required
def bmi(request):
    if request.method == "POST":
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')

        # calculate BMI
        height_m = height / 100
        bmi_value = round(weight / (height_m ** 2), 1)

        # calculate calorie goal
        if gender == 'male':
            calorie_goal = int(88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age))
        else:
            calorie_goal = int(447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age))

        UserProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'height': height,
                'weight': weight,
                'age': age,
                'gender': gender,
                'bmi': bmi_value,
                'calorie_goal': calorie_goal
            }
        )

        return redirect('index_page')

    profile = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'bmi.html', {'profile': profile})



# INDEX
@login_required
def index(request):
    # get user's calorie goal
    profile = UserProfile.objects.filter(user=request.user).first()
    calorie_goal = profile.calorie_goal if profile else 2000

    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')
        if food_consumed:
            consume = Food.objects.get(name=food_consumed)
            user = request.user
            consume = Consume(user=user, food_consumed=consume)
            consume.save()
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()

    consumed_food = Consume.objects.filter(user=request.user)
    return render(request, 'index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'calorie_goal': calorie_goal    
    })



# DELETE FOOD

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    consumed_food.delete()
    return redirect('index_page')



# DAYS-NEW
@login_required
def save_day(request):
    if request.method == 'POST':
        total_carbs = float(request.POST.get('total_carbs',0))
        total_protein = float(request.POST.get('total_protein',0))
        total_fats = float(request.POST.get('total_fats',0))
        total_calories = float(request.POST.get('total_calories',0))


        DailyLog.objects.create(
            user=request.user,
            total_carbs=total_carbs,
            total_protein=total_protein,
            total_fats=total_fats,
            total_calories=total_calories
        )

        # clear today's consumed food after saving

        Consume.objects.filter(user=request.user).delete()

        return redirect('history')
    return redirect('index_page'),


# NEW HISTORY

@login_required
def history(request):
    logs = DailyLog.objects.filter(user=request.user).order_by('-date')
    return render(request,'history.html',{'logs':logs})

# DELETE DAILY LOG ✅
@login_required
def delete_log(request, id):
    log = DailyLog.objects.get(id=id)
    log.delete()
    return redirect('history')