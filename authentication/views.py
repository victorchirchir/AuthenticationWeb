from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from metaverse import settings


# Create your views here.
def home(request):
    return render(request,'authentication/index.html')

def signup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        gender=request.POST['gender']
        dob=request.POST['dob']
        favColour=request.POST['favColour']
        favColour=request.POST['favColour']

        if User.objects.filter(username=username):
            messages.error(request,'Username already Exists!')
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,'Email Already Registered!')
            return redirect('home')

        if password!=confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('home')

        if len(username)>15:
            messages.error(request,'Usernames should not have more than 15 characters')
            return redirect('home')

        if not username.isalnum():
            messages.error(request,'The username should only contain alpahnumerics')
            return redirect('home')



        

        myUser=User.objects.create_user(username,email,password)
        myUser.first_name=fname
        myUser.last_name=lname

        myUser.save()

        messages.success(request,'Your Account has been created successfully')

        #Welcome Email
        subject='Welcome to Metaverse'
        message='Hello '+myUser.first_name+'Welcome to Metaverse \n Thank you for Visiting our Website \n We have also sent you a confirmation email, kindly confirm your email \n Than you!! '
        from_email= settings.EMAIL_HOST_USER
        to_list=[myUser.email]
        

        return redirect('signin')

    return render(request,'authentication/signup.html')
    




def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,'authentication/index.html',{'fname':fname})
        else:
            messages.error(request,'Wrong Username or Password')
            return redirect('home')

    return render(request,'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request,'You have been logged out Successfully')
    return redirect('home')


