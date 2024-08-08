from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article
from .models import Tag
from .models import Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        tag_count = 0
        search_tag_duplicates = set()
        for form in self.forms:
            if form.cleaned_data.get('tag') is not None:
                tag_count = tag_count + 1
                search_tag_duplicates.add(form.cleaned_data.get('tag'))

            if form.cleaned_data.get('is_main') == True:
                is_main_count = is_main_count + 1

        if tag_count == 0:
            raise ValidationError('Необходимо указать хотя бы один тэг')
        if is_main_count < 1:
            raise ValidationError('Необходимо указать основной тэг')
        elif is_main_count > 1:
            raise ValidationError('Основной тэг должен быть только один')
        if tag_count != len(search_tag_duplicates):
            raise ValidationError('Не должно быть повторяющихся тегов')
        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['article', 'tag', 'is_main']
    ordering = ['is_main', 'tag']



