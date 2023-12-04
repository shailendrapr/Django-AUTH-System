from django.core.mail import EmailMessage,send_mail
from tokenize import generate_tokens
from django import template
from django.http import HttpRequest
from django.shortcuts import render,redirect
import authentication
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.template.loader import render_to_string 
from django.utils.encoding import force_bytes,force_str
from . tokens import generate_token

from hello import settings

def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        Fname=request.POST['Fname']
        Lname=request.POST['Lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request,"Username already exists! Please choose another username")
            return redirect("home")
        
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered! Please choose another email")
            return redirect("home")
        
        if len(username)>10:
            messages.error(request,"Username must be less than 10 characters")
            return redirect("home")
        
        if pass1!=pass2:
            messages.error(request,"Passwords do not match")
            return redirect("home")
        
        if not username.isalnum():
              messages.error(request,"Username must be alphanumeric")
              return redirect("home")

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=Fname
        myuser.last_name=Lname
        myuser.is_active=False
        myuser.save()
        messages.success(request,"Your account has been successfully created. we've sent you a confirmation email please click on the link in the email to activate your account1")

        #welcome email
        subject="Shailendra Project login"
        message="Hello"+myuser.first_name+"!!\n"+"Welcome to my Project\n"+"Thank you for visiting my website\n"+"I've also sent you a confirmation mail please open it to activate your account\n"+"Thank You"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        #return redirect('signin')
    
        #confirmation email
        current_site=get_current_site(request)
        email_subject="Confirm you email@Shailendra Project login!!"
        message2=render_to_string('email_confirmation.html',
        {
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)

        })
        email=EmailMessage(email_subject,message2,settings.EMAIL_HOST_USER,[myuser.email],)
        email.fail_silently=True
        email.send()


    return render(request,"authentication/signup.html")

def signin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        pass1=request.POST.get('Pass1')
        user=authenticate(request,username=username,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            context={'fname':fname}
            return render(request,"authentication/index.html",context)
        else:
            messages.error(request,"bad credentials")
            return redirect("signin")


    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("home")


def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')



