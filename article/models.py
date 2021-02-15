
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.fields import CharField
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Yazar")
    title = models.CharField(max_length=50,verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi")
    article_image = models.FileField(blank=True,null=True,verbose_name="Makaleye Fotoğraf Ekleyin")
    rating = models.FloatField(default=0,verbose_name="rating")
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_date']
class Rating(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="Makale",related_name="Rating")
    rater = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Rater")
    rate = models.IntegerField(default=0,verbose_name="Rate")
class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="Makale",related_name="comments")
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Yazar",related_name="comments")
    title = models.CharField(max_length=50,verbose_name="Başlık")
    content = CharField(max_length=200,verbose_name="İçerik (200 karakter)")
    comment_date = models.DateTimeField(auto_now_add=True,verbose_name="Yorum Tarihi")
    class Meta:
        ordering = ['-comment_date']