from django.contrib import admin
from .models import Blog
# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ('title',)}
    list_display = (
        'id',
        "author",
        'title',
        'time',
        'published',
    )
    search_fields = ('title',)
admin.site.register(Blog,BlogAdmin)
