import user
from django.contrib.auth import REDIRECT_FIELD_NAME, login
import article
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render,HttpResponse,get_object_or_404
from .models import Article,Rating,Comment
from .forms import ArticleForm,CommentForm
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,"index.html")
def about(request):
    return render(request,"about.html")
def articles(request):
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})
def showArticle(request,id):
    # article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article,id = id)
    rates = Rating.objects.filter(article=article)
    user_rate=0
    if request.user.is_authenticated:
        user_rate = Rating.objects.filter(rater=request.user).filter(article=article).first()
        if user_rate:
            user_rate=user_rate.rate
    comments = Comment.objects.filter(article=article)
    context = {
        "article" : article,
        "len_rates" : len(rates),
        "user_rate" : user_rate,
        "rates" : range(1,6),
        "comment_form" : CommentForm(),
        "comments" : comments,

    }
    return render(request,"showarticle.html",context = context) 
@login_required(login_url="user:login")
def addArticle(request):
    article_form = ArticleForm(request.POST or None,request.FILES or None)
    if article_form.is_valid():
        # title = article_form.cleaned_data.get("title")
        # content = article_form.cleaned_data.get("content")
        # author = request.user
        # newArticle = Article(title=title,content = content,author=author)
        # newArticle.save() 
        new_article = article_form.save(commit=False)
        new_article.author=request.user
        new_article.save()
        messages.success(request,"Makale başarıyla kaydedildi")
        return redirect("/user/dashboard")
    context = {
        "form" : article_form
    }
    return render(request,"addarticle.html",context=context)
@login_required(login_url="user:login")
def editArticle(request,id):
    article = get_object_or_404(Article,id=id)
    if article.author.username != request.user.username:
        messages.info(request,"Bu işlemi yapma yetkiniz yok!")
        return redirect("index")
    edit_form = ArticleForm(request.POST or None,request.FILES or None,instance=article)
    if edit_form.is_valid():
        new_article = edit_form.save(commit=False)
        new_article.author=request.user
        new_article.save()
        messages.success(request,"Makale başarıyla kaydedildi")
        return redirect("user:dashboard")
    
    return render(request,"editarticle.html",{"form":edit_form})
@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article, id=id)
    if article.author != request.user:
        messages.info(request,"Bu işlemi yapma yetkiniz yok!")
        return redirect("index")
    article.delete()
    messages.success(request,"Makale başarıyla silindi")
    return redirect("user:dashboard")
def search(request):
    keyword = request.GET.get("keyword")
    articles = Article.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
    context = {
        "articles" : articles,
        "keyword" : keyword,
    }
    return render(request,"search.html",context=context)
@login_required(login_url="user:login")
def rateArticle(request,id,newrate):
    article = get_object_or_404(Article,id=id)
    given_rate = Rating.objects.filter(article=article,rater=request.user).first()
    if given_rate:
        if given_rate.rate == newrate:
            given_rate.delete()
            messages.info(request,"Değerlendirmeniz kaldırıldı.")
        else:
            given_rate.rate=newrate
            given_rate.save()
            messages.success(request,"Değerlendirmeniz kaydedildi.")

    else:
        given_rate = Rating(article=article,rater=request.user,rate=newrate)
        given_rate.save()
        messages.success(request,"Değerlendirmeniz kaydedildi.")
    article_rates = Rating.objects.filter(article=article)
    total_rate = 0
    rates_len = 0
    for i in article_rates:
        total_rate+=i.rate
        rates_len+=1
    if rates_len != 0:
        total_rate=float("{:.1f}".format(total_rate/rates_len))
    article.rating = total_rate
    article.save()
    return redirect("article:showarticle",id=id)
@login_required(login_url="user:login")
def addComment(request,article_id):
    article = get_object_or_404(Article,id=article_id)
    comment = Comment(title = request.POST.get("title"),content = request.POST.get("content") or None) 
    if comment:
        comment.article = article
        comment.author = request.user
        comment.save()
        messages.success(request,"Yorumunuz başarıyla kaydedildi")
        return redirect("article:showarticle", id=article_id)
    else:
        messages.info(request,"Bir hata oluştu")  
        return redirect("article:showarticle", id=article_id)


