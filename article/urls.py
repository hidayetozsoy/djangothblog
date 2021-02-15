from article import views
from django.urls import path
app_name="article"
urlpatterns = [
    path("",views.articles,name="articles"),
    path("addarticle/",views.addArticle,name="addarticle"),
    path("article/<int:id>/",views.showArticle,name="showarticle"),
    path("edit/<int:id>",views.editArticle,name="editarticle"),
    path("delete/<int:id>",views.deleteArticle,name="deletearticle"),
    path("search/",views.search,name="search"),
    path("ratearticle/<int:id>/<int:newrate>/",views.rateArticle,name="ratearticle"),
    path("addcomment/<int:article_id>/",views.addComment,name="addcomment"),
]