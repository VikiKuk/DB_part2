from django.db import models
from django.forms import BooleanField


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')
    articles = models.ManyToManyField(Article, related_name='tags', through='Scope')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes', blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_main', 'tag']
