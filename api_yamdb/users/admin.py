from django.contrib import admin

from reviews.models import Categories, Genres, Title, Review, Comment
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        'confirmation_code'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('username', 'role')
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description')
    search_fields = ("name", "year")
    list_filter = ('name', "year")
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', 'author', 'score', 'pub_date')
    list_filter = ('title', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'review', 'text', 'pub_date')
    search_fields = ('author', 'review', 'pub_date')
    list_filter = ('author', 'review', 'pub_date')
    empty_value_display = '-пусто-'
