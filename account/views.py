from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth 
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from .models import register_table
from django.core.mail import EmailMessage
from django.db import IntegrityError




def register(request):
    if "user_id"in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User,id=uid)
        login(request,usr)
        if usr.is_superuser:
            return HttpResponseRedirect("/admin")
        if usr.is_active:
            return HttpResponseRedirect("/my_account")
    if request.method=="POST":
        fname = request.POST["first"]
        last = request.POST["last"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        
        try:
            usr = User.objects.create_user(username,email,password)
            usr.first_name = fname
            usr.last_name = last
        
            usr.is_staff = True
            usr.save()
            reg = register_table(user=usr)
            reg.save()
            return render(request,"account/sign_up.html",{"status":"Mr/Miss. {} your Account created Successfully".format(fname)})
        except IntegrityError as e: 
            return render(request,"account/sign_up.html",{"status":"Mr/Miss. {} already ".format(username)})
    return render(request,"account/sign_up.html")


	

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


@login_required
def user_logout(request):
    logout(request)
    res =  HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    messages.success(request,"Successfull Logged Out")
    return res



def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/entry")
            else:
                messages.success(request," Successfully Logged in ")
                res = HttpResponseRedirect("/show")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now())
                return res
        else:
            messages.success(request,"Incorrect username or Password")
            return render(request,"account/login.html")

    return render(request,"account/login.html")



def edit_profile(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"]=data    
    if request.method=="POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["contact"]
        age = request.POST["age"]
        ct = request.POST["city"]
        gen = request.POST["gender"]
        occ = request.POST["occ"]
        abt = request.POST["about"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.age = age
        data.city = ct
        data.gender = gen
        data.occupation = occ
        data.about = abt
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_pic = img
            data.save()


        context["status"] = ""
        messages.success(request, ' Successfully Update Profile ')
    return render(request,"account/edit_profile.html",context)


def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            messages.success(request," Password Changed Successfully!!! ")
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            messages.success(request," Incorrect Current Password!!! ")
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"account/change_password.html",context)


# def forgotpass(request):
#     context = {}
#     if request.method=="POST":
#         un = request.POST["username"]
#         pwd = request.POST["npass"]

#         user = get_object_or_404(User,username=un)
#         user.set_password(pwd)
#         user.save()

#         login(request,user)
#         if user.is_superuser:
#             return HttpResponseRedirect("/account/forgotpass")
#         else:
#             return HttpResponseRedirect("/account/forgotpass")
#         # context["status"] = "Password Changed Successfully!!!"

#     return render(request,"account/forgot_pass.html",context)



# import random

# def reset_password(request):
#     un = request.GET["username"]
#     try:
#         user = get_object_or_404(User,username=un)
#         otp = random.randint(1000,9999)
#         msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \nMyWebsite".format(user.username, otp)
#         try:
#             email = EmailMessage("Account Verification",msz,to=[user.email])
#             email.send()
#             return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
#         except:
#             return JsonResponse({"status":"error","email":user.email})
#     except:
#         return JsonResponse({"status":"failed"})    