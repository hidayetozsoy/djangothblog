from django.contrib.auth.decorators import login_required
from django.http import request
from article.models import Article
from django.shortcuts import get_list_or_404, get_object_or_404, render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            name = register_form.cleaned_data.get("name")
            surname = register_form.cleaned_data.get("surname")
            username = register_form.cleaned_data.get("username")
            email = register_form.cleaned_data.get("email")
            password = register_form.cleaned_data.get("password")
            newUser = User(username=username,first_name=name,last_name=surname,email=email)
            newUser.set_password(password)
            newUser.save()
            login(request,newUser)
            messages.success(request,"Tebrikler, başarıyla kayıt oldunuz")
            return redirect("index")
        else:
            context = {
                "form" : register_form,
            }
            return render(request,"register.html",context=context)    
    else:
        register_form = RegisterForm()
        context = {
            "form" : register_form,
        }
        return render(request,"register.html",context=context)

def loginUser(request):
    login_form = LoginForm(request.POST or None)
    print(request.path)
    context = {
        "form":login_form,
    }
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        if user is None:
            messages.info(request,"Kullanıcı adı veya parola hatalı")
            return render(request,"login.html",context=context)
        messages.success(request,"Tebrikler, başarıyla giriş yaptınız")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context=context) 
@login_required(login_url="user:login")
def logoutUser(request):
        logout(request)
        messages.success(request,"Başarıyla çıkış yaptınız.")
        return redirect("index")
@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = { 
        "articles" : articles,
    }
    return render(request,"dashboard.html",context=context)
def showUser(request,id):
    user = get_object_or_404(User,id=id)
    articles = Article.objects.filter(author=user)
    context = {
        "articles" : articles, 
        "user" : user,
    }
    return render(request,"user.html",context=context)
    
    