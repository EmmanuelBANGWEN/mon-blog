from django.contrib import admin
from .models import Category, Comment , Post
# Register your models here.
#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'statut', 'created', 'published', 'update', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    ordering = ('author', 'statut', 'published')
    list_filter = ('author', 'created', 'published', 'update')


@admin.register(Comment)
class Comments(admin.ModelAdmin):
    # list_display = ['username', 'created', 'email']
    list_display = ['created']



admin.site.register(Category)
    